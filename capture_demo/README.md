# 摄像头录像 / 调试 Demo

从 `cells_detect` 主程序里分离出来的最小示例：**左侧一块大画布，右侧两个按钮**。

- **摄像头调试**：点「打开摄像头」→ 打开摄像头，画面实时显示在画布上，**不写任何文件**；
  再点一次「关闭摄像头」→ 释放摄像头，画布回到黑屏。
- **录制**：点「开始录制」→ 一边实时预览一边写入视频文件；
  再点一次「结束录制」→ 停止写盘、保存文件、释放摄像头，画布保留最后一帧。
  保存完成后会**弹窗问一句要不要打开视频所在文件夹**，选「打开文件夹」才去打开（`--no-open` 可关掉）。

启动时画布是纯黑屏（不放提示文字，避免和「真的没画面」混淆）。

两种取流方式**互斥**：一种在跑时另一个按钮会置灰。这是有意的——同一个摄像头不能被两路
`VideoCapture` 同时打开，直接禁用比让用户点了以后报错更清楚。

代码只有一个文件 `capture_demo.py`，不依赖主程序的 `MainWindow.ui`、`modules/`，可以直接拷走单独运行。

## 运行

```powershell
# 本机可用的环境（含 opencv + PySide6）
D:\anaconda3\envs\opencv\python.exe capture_demo.py
```

常用参数：

```powershell
python capture_demo.py --camera 1                    # 指定摄像头序号（默认 0，自动探测 0~3）
python capture_demo.py --width 1920 --height 1080    # 指定分辨率（默认 0=沿用摄像头自身分辨率）
python capture_demo.py --fps 30 --out D:\videos      # 兜底帧率 / 保存目录
python capture_demo.py --camera test.mp4             # 用视频文件当信号源（无摄像头时自测）
python capture_demo.py --no-open                     # 录制结束后不再询问是否打开保存文件夹
```

## 摄像头调试

点「打开摄像头」以后，右侧会实时显示一行读数，例如 `画面 640×480 · 实测 30.0 fps`：

- **画面** = 摄像头真正吐出来的分辨率；
- **实测 fps** = 每秒实际读到的帧数（注意：不是摄像头的上报值）。

这两个数正好对应下面「踩过的坑」里的前两条问题——预览时盯着它就够了。
另外，调试模式**不会**创建任何视频文件，所以可以放心长时间挂着找角度、调焦距。

## 输出

- 默认保存在 `capture_demo/videos/`，文件名为时间戳，如 `20250916_192446.mp4`；
- 编码器按 `mp4v(mp4) → XVID(avi) → MJPG(avi)` 依次尝试，第一个可用的生效；
- 界面右侧显示本次录制的时长、帧数和文件名；
- 录制结束后弹窗询问是否打开保存目录，点「打开文件夹」才在文件管理器里打开并选中该文件
  （`--no-open` 关闭这次询问）。

## 打包成免环境的 exe

产物：`capture_demo/dist/capture_demo.exe`，**单文件、约 92 MB**，内置了 Python + PySide6 + OpenCV。
拷到任意一台 64 位 Windows 上双击就能跑，**不需要装 Python 或 conda**。

重新打包（在仓库根目录执行）：

```powershell
D:\anaconda3\envs\opencv\python.exe -m PyInstaller ^
    --distpath capture_demo\dist --workpath capture_demo\build --noconfirm ^
    capture_demo\capture_demo.spec
```

打包相关的几个坑（都已在代码/配置里处理）：

- **录像存到 exe 旁边**：打包后 `__file__` 指向 PyInstaller 的临时解压目录（进程退出就被删掉），
  所以 `BASE_DIR` 在 frozen 模式下改用 `sys.executable` 所在目录；
  否则录下来的视频会跟着临时目录一起消失。即 `capture_demo.exe` 在哪，`videos/` 就在哪旁边。
- **无控制台**：`console=False` 时 `sys.stdout` / `sys.stderr` 是 `None`，
  而 argparse 打印 `--help` 和参数报错都要往这两个流写，会直接抛异常；
  `main()` 里补了一个丢弃式的占位流。
- **体积**：`capture_demo.spec` 的 `excludes` 排掉了 QtQml / QtQuick / QtWebEngine / Qt3D /
  QtMultimedia 等用不到的模块。UPX 关着（本机没装，而且压过的 exe 更容易被
  Windows Defender 误报）。
- `--distpath` / `--workpath` 是相对路径，所以按上面的命令在仓库根目录跑。

## 实现要点

| 位置 | 说明 |
| --- | --- |
| `CaptureWorker(QThread)` | 采集线程：读帧 → `frame_ready` 发预览 → 录制中 `VideoWriter.write()` |
| 只预览不录制 | `CaptureWorker` 不调 `start_recording()` 时 `_pending_path` 为 None，帧只发预览、不落盘 |
| 跨线程 | 状态用 `threading.Lock` 保护，界面只通过 Qt 信号回主线程刷新 |
| 模式互斥 | 界面 `_mode`（idle / preview / recording）单向驱动按钮的文案与 `setEnabled` |
| 关闭预览 | `_closing` 标志丢弃收尾期间迟到的帧，`_on_worker_finished` 里 `canvas.clear()` 回黑屏 |
| 调试读数 | `stats_ready` 每秒汇报一次真实分辨率 + 实测帧率（`_emit_stats`） |
| 打开相机 | Windows 上**优先 DSHOW**，再试 MSMF；每个候选都做一次「试读一帧」探测 |
| 画布 | `QImage.Format_BGR888` + `.copy()`（帧缓冲会被复用），按 `KeepAspectRatio` 随窗口缩放 |
| 帧率 | 先缓冲 3 帧 / 0.3 秒测出**实测帧率**再建文件，避免按摄像头上报值写错播放速度 |
| 停止 | GUI 置停止标志，采集线程把缓冲写完、关文件、发 `recording_finished`，保证文件完整 |
| 询问弹窗 | 录完用 `QTimer.singleShot(0, …)` 延到下一轮事件循环再弹 `QMessageBox`，避免在模态框里嵌套处理 `finished`；按钮自己加，不用跟系统语言走的标准按钮 |
| 弹出文件夹 | `open_folder()` 用 `explorer /select,` 打开目录并选中文件，失败退回 `os.startfile`；都是尽力而为，弹不出来也不影响录制结果 |
| 结束 | 关闭窗口时 `request_stop()` + `wait(3000)`，先释放摄像头再退出 |

### 踩过的坑（本机实测）

1. **MSMF 打开成功却读不出帧**：`cv2.VideoCapture(1)`（默认 MSMF）`isOpened()` 为 True，
   但 `read()` 一直报 `can't grab frame. Error: -2147024891`，换 `cv2.CAP_DSHOW` 才正常。
   所以 demo 里优先 DSHOW，并且打开后先试读一帧才算成功。
2. **强制设置不支持的分辨率会出黑帧**：本机摄像头原生 640×480，
   设成 1280×720 后驱动"接受"了但每帧全黑（`std=0`）且回帧速度异常。
   所以默认不设置分辨率，只有显式传 `--width/--height` 才设置。
3. **上报帧率 ≠ 实际帧率**：本机摄像头上报 30 fps，实际只有约 1 fps。
   直接按 30 fps 写盘，播放时会快 30 倍；demo 改为按实测帧率建 writer，
   调试面板里的「实测 fps」也是同一个读数。
