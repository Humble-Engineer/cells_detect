# -*- coding: utf-8 -*-
"""
摄像头录像 / 调试 Demo（独立版）

界面：左侧一块大画布（实时预览，初始为黑屏），右侧两个按钮。
- 「打开摄像头」（摄像头调试）：只打开摄像头做实时预览，不写任何文件；
  再点一次「关闭摄像头」→ 释放摄像头，画布回到黑屏。
- 「开始录制」：打开摄像头，实时预览并把画面写入视频文件；
  再点一次「结束录制」→ 停止录制、保存文件、释放摄像头，画布保留最后一帧；
  保存完成后弹窗问一句要不要打开视频所在文件夹（用 `--no-open` 可关掉）。

两种取流方式互斥：一种在跑时另一个按钮会被禁用，避免两个线程抢同一个摄像头。

本文件不依赖主程序的 MainWindow.ui / modules，可单独拷走运行。

用法：
    python capture_demo.py                      # 自动探测摄像头（0/1/2/3）
    python capture_demo.py --camera 1           # 指定摄像头序号
    python capture_demo.py --width 1920 --height 1080   # 指定分辨率（默认用摄像头自身的）
    python capture_demo.py --camera test.mp4    # 用视频文件当信号源（无摄像头时自测）
    python capture_demo.py --no-open            # 录制结束后不再询问是否打开保存文件夹

视频默认保存在本文件同级的 videos/ 目录下；录制帧率按实测帧率写入，保证播放速度正常。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
import time
from datetime import datetime

import cv2
from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtGui import QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

if getattr(sys, "frozen", False):
    # 打包成 exe 之后 __file__ 指向 PyInstaller 解压出来的临时目录（退出就删），
    # 必须改用 exe 自己所在的目录，否则录下来的视频会跟着临时目录一起消失。
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_OUT_DIR = os.path.join(BASE_DIR, "videos")

# Windows 上 DSHOW 比默认的 MSMF 可靠：部分 USB 相机会出现
# "MSMF 打开成功但一帧都读不出" 的情况，所以优先 DSHOW。
BACKENDS = ((cv2.CAP_DSHOW, "DSHOW"), (cv2.CAP_MSMF, "MSMF")) if sys.platform == "win32" \
    else ((cv2.CAP_ANY, "ANY"),)

# 依次尝试的编码器，第一个能打开的就用
CODEC_CANDIDATES = (("mp4v", ".mp4"), ("XVID", ".avi"), ("MJPG", ".avi"))

# 采样多少帧/多长时间后，用实测帧率创建视频文件
MIN_SAMPLES = 3
SAMPLE_SPAN = 0.3      # 秒
MAX_SAMPLES = 20       # 兜底上限，避免缓冲占内存

STATS_INTERVAL = 1.0   # 每隔多少秒向界面汇报一次「实测帧率 + 分辨率」

# 录制按钮的两种外观
STYLE_IDLE = """
QPushButton {
    background-color: #d93025; color: #ffffff;
    border: none; border-radius: 8px;
    padding: 16px 12px; font-size: 16px; font-weight: bold;
}
QPushButton:hover { background-color: #e8453a; }
QPushButton:pressed { background-color: #b3261c; }
QPushButton:disabled { background-color: #e8eaed; color: #9aa0a6; }
"""
STYLE_RECORDING = """
QPushButton {
    background-color: #3c4043; color: #ffffff;
    border: none; border-radius: 8px;
    padding: 16px 12px; font-size: 16px; font-weight: bold;
}
QPushButton:hover { background-color: #4a4e52; }
QPushButton:pressed { background-color: #2b2e31; }
QPushButton:disabled { background-color: #e8eaed; color: #9aa0a6; }
"""

# 摄像头调试按钮（只预览、不写盘）的两种外观
STYLE_PREVIEW_IDLE = """
QPushButton {
    background-color: #1a73e8; color: #ffffff;
    border: none; border-radius: 8px;
    padding: 12px; font-size: 15px; font-weight: bold;
}
QPushButton:hover { background-color: #2b7de9; }
QPushButton:pressed { background-color: #1662c4; }
QPushButton:disabled { background-color: #e8eaed; color: #9aa0a6; }
"""
STYLE_PREVIEW_ACTIVE = """
QPushButton {
    background-color: #3c4043; color: #ffffff;
    border: none; border-radius: 8px;
    padding: 12px; font-size: 15px; font-weight: bold;
}
QPushButton:hover { background-color: #4a4e52; }
QPushButton:pressed { background-color: #2b2e31; }
QPushButton:disabled { background-color: #e8eaed; color: #9aa0a6; }
"""

# 画布（黑屏）与计时数字的两种外观
STYLE_CANVAS = "background-color: #000000; color: #9aa0a6; font-size: 15px;"
STYLE_CANVAS_ERROR = "background-color: #000000; color: #e8453a; font-size: 15px;"
STYLE_TIME = "font-size: 34px; font-weight: bold; color: #202124;"
STYLE_TIME_IDLE = "font-size: 34px; font-weight: bold; color: #bdc1c6;"


def now_stamp() -> str:
    """生成文件名用的时间戳。"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def fmt_duration(seconds: float) -> str:
    """把秒数格式化成 mm:ss。"""
    total = int(round(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


def open_folder(path: str) -> bool:
    """在系统文件管理器里打开 path 所在目录（Windows 上顺带选中该文件）。

    纯尽力而为：弹不出来也不该影响录制结果，所以失败只返回 False，不抛异常。
    注意 explorer.exe 即使成功也可能返回退出码 1，所以这里不检查退出码。
    """
    target = os.path.abspath(path)
    folder = os.path.dirname(target) or "."
    try:
        if sys.platform == "win32":
            subprocess.Popen(["explorer", "/select,", target])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])
        return True
    except OSError:
        pass

    # 兜底：只打开目录、不选中文件。os.startfile 是 Windows 专有 API，
    # 其它平台在上面那一步已经试过了，这里没有更好的办法，直接认输。
    if sys.platform != "win32":
        return False
    try:
        os.startfile(folder)            # noqa: S606 - Windows 专用
        return True
    except OSError:
        return False


class CaptureWorker(QThread):
    """采集线程：读摄像头 → 发预览帧 →（录制中）写入视频文件。

    - 跨线程状态用 _lock 保护，界面只通过信号回主线程刷新；
    - 不调用 start_recording() 时就是纯预览模式：帧只发 frame_ready、不落盘，
      所以「摄像头调试」和「录制」可以共用这一个线程类；
    - 真正写盘前先采样几帧测实际帧率，避免"相机上报 30fps 实际只有 1fps"
      导致录出来的视频播放速度不对。
    """

    frame_ready = Signal(QImage)                      # 预览帧
    stats_ready = Signal(int, int, float)             # 宽, 高, 实测帧率（约每秒一次，供调试显示）
    recording_started = Signal(str)                   # 实际写盘的文件路径
    recording_finished = Signal(str, float, int)      # 路径, 时长(秒), 帧数
    failed = Signal(str)                              # 错误信息

    def __init__(self, source, size=(0, 0), fps=25.0,
                 out_dir=DEFAULT_OUT_DIR, parent=None):
        super().__init__(parent)
        self._source = source
        self._size = size
        self._fallback_fps = float(fps)
        self._out_dir = out_dir
        self._is_file = isinstance(source, str) and os.path.isfile(source)

        self._lock = threading.Lock()
        self._stop_flag = False
        self._pending_path = None    # GUI 请求录制的目标路径
        self._buffer = []            # 尚未确定帧率的待写帧
        self._stamps = []            # 对应的时间戳
        self._writer = None
        self._path = None
        self._recording = False
        self._frames = 0
        self._start_time = 0.0
        self._stat_frames = 0        # 统计窗口内已收到的帧数
        self._stat_start = 0.0       # 统计窗口起点

    # ---------------- 供 GUI 线程调用 ----------------

    def start_recording(self, path: str) -> None:
        with self._lock:
            if self._writer is None and self._pending_path is None:
                self._pending_path = path

    def request_stop(self) -> None:
        with self._lock:
            self._stop_flag = True

    def is_recording(self) -> bool:
        with self._lock:
            return self._recording

    def elapsed_seconds(self) -> float:
        """已录制时长（秒），供界面刷新计时用。"""
        with self._lock:
            started = self._start_time
        return time.time() - started if started else 0.0

    def _stopping(self) -> bool:
        with self._lock:
            return self._stop_flag

    # ---------------- 线程主体 ----------------

    def run(self) -> None:
        cap = self._open_capture()
        if cap is None:
            self.failed.emit("未检测到可用的摄像头，请检查设备连接。")
            return

        reported_fps = cap.get(cv2.CAP_PROP_FPS)
        if not (1.0 < reported_fps <= 240.0):
            reported_fps = self._fallback_fps

        misses = 0
        deadline = time.time()
        self._stat_start = deadline
        while not self._stopping():
            ok, frame = cap.read()
            if not ok:
                if self._is_file:
                    break                       # 视频文件播完
                misses += 1
                if misses > 60:                 # 摄像头掉线，别死循环
                    self.failed.emit("摄像头读取失败，已停止。")
                    break
                self.msleep(20)
                continue
            misses = 0

            stamp = time.time()
            self._process_frame(frame, stamp, reported_fps)
            self._emit_frame(frame)
            self._emit_stats(frame, stamp)

            if self._is_file:                   # 文件源按原帧率播放，便于无硬件自测
                period = 1.0 / reported_fps
                deadline += period
                if deadline < time.time():
                    deadline = time.time()      # 落后了，重新对齐
                else:
                    self.msleep(int((deadline - time.time()) * 1000))

        self._finalize()
        cap.release()

    def _open_capture(self):
        """打开信号源；整数序号时在 0~3 之间探测，并逐个后端验证能否真的出帧。"""
        if self._is_file:
            cap = cv2.VideoCapture(self._source)
            return cap if cap.isOpened() else None

        indexes = range(4) if self._source == 0 else (self._source,)
        for index in indexes:
            for api, _name in BACKENDS:
                cap = cv2.VideoCapture(index, api)
                if not cap.isOpened():
                    cap.release()
                    continue
                if self._size[0] > 0 and self._size[1] > 0:
                    # 只在显式指定分辨率时才设置：部分驱动对不支持的模式
                    # 会"接受但只吐黑帧"，所以默认沿用摄像头自身的模式。
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._size[0])
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._size[1])
                ok, frame = cap.read()          # 探针：有些后端"打开成功却读不出帧"
                if ok and frame is not None:
                    return cap
                cap.release()
        return None

    def _process_frame(self, frame, stamp: float, reported_fps: float) -> None:
        """录制状态下把帧交给 writer；还没定帧率就先缓冲。"""
        with self._lock:
            writer, pending = self._writer, self._pending_path

        if writer is not None:
            writer.write(frame)
            self._frames += 1
            return
        if pending is None:
            return

        self._buffer.append(frame)
        self._stamps.append(stamp)
        span = self._stamps[-1] - self._stamps[0]
        if len(self._buffer) >= MAX_SAMPLES or (
                len(self._buffer) >= MIN_SAMPLES and span >= SAMPLE_SPAN):
            self._create_writer(reported_fps)

    def _create_writer(self, fallback_fps: float) -> None:
        """按实测帧率创建 VideoWriter，并把缓冲的帧补写进去。"""
        with self._lock:
            path = self._pending_path
            frames, stamps = list(self._buffer), list(self._stamps)
            self._buffer.clear()
            self._stamps.clear()
            self._pending_path = None
            if path is None or not frames:
                return

        fps = self._measure_fps(stamps, fallback_fps)
        height, width = frames[0].shape[:2]
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        writer = None
        for fourcc_name, ext in CODEC_CANDIDATES:
            candidate = os.path.splitext(path)[0] + ext
            probe = cv2.VideoWriter(candidate, cv2.VideoWriter_fourcc(*fourcc_name),
                                    fps, (width, height))
            if probe.isOpened():
                writer, path = probe, candidate
                break
            probe.release()

        if writer is None:
            self.failed.emit("无法创建视频文件（编码器不可用）。")
            return

        for frame in frames:
            writer.write(frame)

        with self._lock:
            self._writer = writer
            self._path = path
            self._recording = True
            self._frames = len(frames)
            self._start_time = stamps[0]
        self.recording_started.emit(path)

    def _finalize(self) -> None:
        """收尾：缓冲里的帧也要写成文件，然后关闭 writer。"""
        with self._lock:
            has_writer = self._writer is not None
            has_pending = self._pending_path is not None and bool(self._buffer)
        if not has_writer and has_pending:
            self._create_writer(self._fallback_fps)

        with self._lock:
            writer, path = self._writer, self._path
            frames, started = self._frames, self._start_time
            self._writer = None
            self._path = None
            self._recording = False

        if writer is None:
            return
        writer.release()
        if frames > 0:
            self.recording_finished.emit(path, time.time() - started, frames)

    @staticmethod
    def _measure_fps(stamps, fallback_fps: float) -> float:
        """用采样时间戳估算真实帧率，异常时退回摄像头上报值。"""
        if len(stamps) >= 2:
            span = stamps[-1] - stamps[0]
            if span > 0:
                return max(1.0, min(120.0, (len(stamps) - 1) / span))
        return max(1.0, min(120.0, fallback_fps))

    def _emit_frame(self, frame) -> None:
        height, width, channels = frame.shape
        image = QImage(
            frame.data, width, height, channels * width,
            QImage.Format.Format_BGR888,
        ).copy()          # 必须拷贝：frame 的缓冲区会被下一帧复用
        self.frame_ready.emit(image)

    def _emit_stats(self, frame, stamp: float) -> None:
        """每隔 STATS_INTERVAL 秒汇报一次真实分辨率和实测帧率。

        调试时最需要看的就是这两个数：摄像头经常「上报 30fps 实测 1fps」，
        或者干脆只吐黑帧；打开预览盯着这里的读数就能立刻发现。
        """
        self._stat_frames += 1
        span = stamp - self._stat_start
        if span < STATS_INTERVAL:
            return
        self.stats_ready.emit(frame.shape[1], frame.shape[0], self._stat_frames / span)
        self._stat_frames = 0
        self._stat_start = stamp


class RecordWindow(QWidget):
    """主窗口：左侧画布 + 右侧控制面板。

    两种取流方式互斥，用 _mode 表示当前处于哪一种：

    - ``preview``   摄像头调试：只预览，不写盘；关掉后画布回到黑屏；
    - ``recording`` 录制：预览的同时写视频文件；结束后画布保留最后一帧。

    互斥是有意的——同一个摄像头不能被两路 VideoCapture 同时打开，
    所以一种在跑的时候，另一个按钮直接禁用，比让用户点了报错更清楚。
    """

    MODE_IDLE = "idle"
    MODE_PREVIEW = "preview"
    MODE_RECORDING = "recording"

    def __init__(self, source=0, size=(0, 0), fps=25.0, out_dir=DEFAULT_OUT_DIR,
                 open_after_save=True):
        super().__init__()
        self._source = source
        self._size = size
        self._fps = fps
        self._out_dir = out_dir
        self._open_after_save = open_after_save     # 录完询问是否打开视频所在文件夹

        self.worker = None
        self._mode = self.MODE_IDLE
        self._closing = False       # 正在关摄像头：期间丢弃迟到的预览帧
        self._last_frame = None     # 停录后保留最后一帧
        self._saved_path = None
        self._error = None          # 本次取流的错误信息

        self._ticker = QTimer(self)
        self._ticker.setInterval(200)
        self._ticker.timeout.connect(self._tick)

        self._build_ui()
        self._refresh_controls()
        self._set_state("摄像头未开启")
        self.time_label.setStyleSheet(STYLE_TIME_IDLE)

    # ---------------- 界面 ----------------

    def _build_ui(self) -> None:
        self.setWindowTitle("摄像头录像 / 调试 Demo")
        self.resize(1100, 700)

        # 左：预览画布。未开摄像头时就是一块纯黑屏，不放提示文字。
        self.canvas = QLabel(self)
        self.canvas.setMinimumSize(640, 480)
        self.canvas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.setStyleSheet(STYLE_CANVAS)

        # 右上：摄像头调试（只预览，不写盘）
        self.preview_button = QPushButton("▶ 打开摄像头", self)
        self.preview_button.setStyleSheet(STYLE_PREVIEW_IDLE)
        self.preview_button.setMinimumHeight(48)
        self.preview_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preview_button.clicked.connect(self.toggle_preview)

        # 右下：录制
        self.record_button = QPushButton("● 开始录制", self)
        self.record_button.setStyleSheet(STYLE_IDLE)
        self.record_button.setMinimumHeight(60)
        self.record_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.record_button.clicked.connect(self.toggle_recording)

        self.state_label = QLabel("未录制", self)
        self.state_label.setWordWrap(True)
        self.state_label.setStyleSheet("font-size: 15px; color: #5f6368;")

        self.time_label = QLabel("00:00", self)
        self.time_label.setStyleSheet(STYLE_TIME)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 调试读数：真实分辨率 + 实测帧率（预览/录制时每约 1 秒刷新）
        self.stats_label = QLabel("", self)
        self.stats_label.setWordWrap(True)
        self.stats_label.setStyleSheet("font-size: 12px; color: #1a73e8;")

        self.info_label = QLabel(f"保存目录：\n{self._out_dir}", self)
        self.info_label.setWordWrap(True)
        self.info_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.info_label.setStyleSheet("font-size: 12px; color: #5f6368;")

        panel = QVBoxLayout()
        panel.setContentsMargins(18, 18, 18, 18)
        panel.setSpacing(14)
        panel.addWidget(self.preview_button)
        panel.addWidget(self.record_button)
        panel.addWidget(self.state_label)
        panel.addWidget(self.time_label)
        panel.addWidget(self.stats_label)
        panel.addStretch(1)
        panel.addWidget(self.info_label)

        panel_box = QWidget(self)
        panel_box.setLayout(panel)
        panel_box.setFixedWidth(250)
        panel_box.setStyleSheet("background-color: #f5f6f7; border-radius: 8px;")

        root = QHBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)
        root.addWidget(self.canvas, 1)
        root.addWidget(panel_box, 0)

    # ---------------- 界面状态 ----------------

    def _refresh_controls(self) -> None:
        """按当前模式决定两个按钮的外观和是否可点。"""
        if self._closing:
            self.preview_button.setEnabled(False)
            self.record_button.setEnabled(False)
            return

        previewing = self._mode == self.MODE_PREVIEW
        recording = self._mode == self.MODE_RECORDING

        self.preview_button.setEnabled(self._mode in (self.MODE_IDLE, self.MODE_PREVIEW))
        self.preview_button.setText("■ 关闭摄像头" if previewing else "▶ 打开摄像头")
        self.preview_button.setStyleSheet(
            STYLE_PREVIEW_ACTIVE if previewing else STYLE_PREVIEW_IDLE)

        self.record_button.setEnabled(self._mode in (self.MODE_IDLE, self.MODE_RECORDING))
        self.record_button.setText("■ 结束录制" if recording else "● 开始录制")
        self.record_button.setStyleSheet(STYLE_RECORDING if recording else STYLE_IDLE)

    def _set_state(self, text: str, color: str = "#5f6368", bold: bool = False) -> None:
        self.state_label.setText(text)
        self.state_label.setStyleSheet(
            f"font-size: 15px; color: {color}; font-weight: {'bold' if bold else 'normal'};")

    def _clear_canvas(self) -> None:
        """画布回到黑屏。"""
        self._last_frame = None
        self.canvas.setStyleSheet(STYLE_CANVAS)
        self.canvas.clear()

    def _show_canvas_text(self, text: str) -> None:
        self._last_frame = None
        self.canvas.setStyleSheet(STYLE_CANVAS_ERROR)
        self.canvas.setText(text)

    # ---------------- 统一的开/关 ----------------

    def _start_worker(self, path=None) -> None:
        """打开摄像头。path 为 None → 只预览（调试）；否则同时写盘。"""
        self._mode = self.MODE_PREVIEW if path is None else self.MODE_RECORDING
        self._error = None
        self._saved_path = None
        self._closing = False

        self.worker = CaptureWorker(self._source, self._size, self._fps, self._out_dir)
        self.worker.frame_ready.connect(self._on_frame)
        self.worker.stats_ready.connect(self._on_stats)
        self.worker.recording_started.connect(self._on_recording_started)
        self.worker.recording_finished.connect(self._on_recording_finished)
        self.worker.failed.connect(self._on_failed)
        self.worker.finished.connect(self._on_worker_finished)
        if path is not None:
            self.worker.start_recording(path)
        self.worker.start()

        self._clear_canvas()
        self.stats_label.setText("")
        self.time_label.setText("00:00")
        self.time_label.setStyleSheet(STYLE_TIME_IDLE)
        self._refresh_controls()
        self._set_state("正在打开摄像头…")

    def _stop_worker(self) -> None:
        """关摄像头：预览模式就是关预览，录制模式则顺带存盘收尾。"""
        self._closing = True
        self._ticker.stop()
        self._set_state("正在关闭摄像头…" if self._mode == self.MODE_PREVIEW
                        else "正在保存视频…")
        self._refresh_controls()
        if self.worker is not None:
            self.worker.request_stop()

    # ---------------- 摄像头调试（只预览，不录制） ----------------

    def toggle_preview(self) -> None:
        if self._closing:
            return
        if self._mode == self.MODE_PREVIEW:         # 第二次点击 → 关闭预览
            self._stop_worker()
        elif self._mode == self.MODE_IDLE:          # 第一次点击 → 打开预览
            self._start_worker()

    # ---------------- 录制流程 ----------------

    def toggle_recording(self) -> None:
        if self._closing:
            return
        if self._mode == self.MODE_RECORDING:
            self._stop_worker()
        elif self._mode == self.MODE_IDLE:
            os.makedirs(self._out_dir, exist_ok=True)
            self._start_worker(os.path.join(self._out_dir, f"{now_stamp()}.mp4"))

    def _on_recording_started(self, path: str) -> None:
        self._set_state("● 录制中", "#d93025", True)
        self.time_label.setStyleSheet(STYLE_TIME)
        self.time_label.setText("00:00")
        self._ticker.start()

    def _on_recording_finished(self, path: str, seconds: float, frames: int) -> None:
        self._ticker.stop()
        self._saved_path = path
        self._set_state(f"已保存 {fmt_duration(seconds)} / {frames} 帧", "#188038", True)
        self._show_saved_info(path)

        # 延到下一个事件循环再弹询问框：让采集线程先把收尾做完
        # （复位按钮、把模式置回 idle），免得在模态框里嵌套处理 finished。
        if self._open_after_save:
            QTimer.singleShot(0, lambda: self._ask_open_folder(path))

    def _show_saved_info(self, path: str, note: str = "") -> None:
        text = f"保存目录：\n{self._out_dir}\n\n最近文件：\n{os.path.basename(path)}"
        self.info_label.setText(text + (f"\n{note}" if note else ""))

    def _ask_open_folder(self, path: str) -> None:
        """录完先问一句要不要打开保存目录，而不是直接把资源管理器怼到脸上。"""
        if not self.isVisible():            # 窗口已经关了就别弹了
            return

        box = QMessageBox(self)
        box.setWindowTitle("录制完成")
        box.setIcon(QMessageBox.Icon.Question)
        box.setText("视频已保存。")
        box.setInformativeText(f"{os.path.basename(path)}\n\n要打开它所在的文件夹吗？")
        # 自己加按钮，不用标准按钮——标准按钮的文案跟系统语言走，中英混着很别扭
        open_button = box.addButton("打开文件夹", QMessageBox.ButtonRole.AcceptRole)
        box.addButton("不用了", QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(open_button)
        box.exec()

        if box.clickedButton() is not open_button:
            return
        # 弹不出来只提示一句，不改状态颜色——文件已经落盘了，那不是录制失败
        self._show_saved_info(path, "（已为你打开该文件夹）" if open_folder(path)
                              else "（未能自动打开文件夹）")

    # ---------------- 线程回调 ----------------

    def _on_frame(self, image: QImage) -> None:
        if self._closing:               # 已经在关了，别再刷新画面
            return
        self._last_frame = image
        self._paint(image)

    def _on_stats(self, width: int, height: int, fps: float) -> None:
        self.stats_label.setText(f"画面 {width}×{height} · 实测 {fps:.1f} fps")

    def _on_failed(self, message: str) -> None:
        self._ticker.stop()
        self._error = message
        self._set_state("出错了", "#d93025", True)
        self._show_canvas_text(message)

    def _on_worker_finished(self) -> None:
        self._ticker.stop()
        was_preview = self._mode == self.MODE_PREVIEW
        self.worker = None
        self._mode = self.MODE_IDLE
        self._closing = False
        self._refresh_controls()

        if self._error is not None:
            return                                  # 错误文字留在画布上，别擦掉
        if was_preview:                             # 关闭预览 → 回到黑屏
            self._clear_canvas()
            self.stats_label.setText("")
            self.time_label.setStyleSheet(STYLE_TIME_IDLE)
            self._set_state("摄像头未开启")
        elif self._saved_path is None:              # 录制没拿到任何画面
            self._set_state("未录制")
        # 录制正常结束：_on_recording_finished 已写好状态，画布保留最后一帧

    def _paint(self, image: QImage) -> None:
        pixmap = QPixmap.fromImage(image).scaled(
            self.canvas.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.canvas.setPixmap(pixmap)

    def _tick(self) -> None:
        if self.worker is not None and self.worker.is_recording():
            seconds = self.worker.elapsed_seconds()
            if seconds:
                self.time_label.setText(fmt_duration(seconds))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self._last_frame is not None:            # 画布跟随窗口缩放
            self._paint(self._last_frame)

    def closeEvent(self, event) -> None:
        if self.worker is not None and self.worker.isRunning():
            self.worker.request_stop()
            self.worker.wait(3000)
        super().closeEvent(event)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="摄像头录像 / 调试 Demo")
    parser.add_argument("--camera", default="0",
                        help="摄像头序号（默认 0，会自动探测 0~3）或视频文件路径")
    parser.add_argument("--width", type=int, default=0,
                        help="采集宽度，默认 0=沿用摄像头自身分辨率")
    parser.add_argument("--height", type=int, default=0,
                        help="采集高度，默认 0=沿用摄像头自身分辨率")
    parser.add_argument("--fps", type=float, default=25.0,
                        help="兜底录制帧率（正常按实测帧率，默认 25）")
    parser.add_argument("--out", default=DEFAULT_OUT_DIR, help="视频保存目录")
    parser.add_argument("--no-open", action="store_true",
                        help="录制结束后不再询问是否打开视频所在文件夹")
    args = parser.parse_args(argv)

    camera = args.camera
    if isinstance(camera, str) and not camera.isdigit():
        if not os.path.isfile(camera):
            parser.error(f"视频文件不存在：{camera}")
    else:
        camera = int(camera)
    return camera, (args.width, args.height), args.fps, args.out, not args.no_open


def main(argv=None) -> int:
    # 打成无控制台的 exe 后 sys.stdout / sys.stderr 会是 None，
    # 而 argparse 打印 --help 和参数报错都往这两个流写，会直接抛异常，
    # 所以这里补一个丢弃式的占位流。
    for stream in ("stdout", "stderr"):
        if getattr(sys, stream, None) is None:
            setattr(sys, stream, open(os.devnull, "w", encoding="utf-8"))

    source, size, fps, out_dir, open_after_save = parse_args(argv)

    app = QApplication(sys.argv[:1])
    app.setFont(QFont("Microsoft YaHei", 10))

    window = RecordWindow(source, size, fps, out_dir, open_after_save=open_after_save)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
