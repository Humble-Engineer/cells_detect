# 交接说明（HANDOVER）

> 用途：把 `F:\deepseek_harness\cells_detect` 这个 DSH 会话里做完的事，交接给 `D:\repos\Projects\cells_detect` 工作区的新会话。
> 写于 2026-09-16，来源会话 `session-85eb11ff-01ad-4ec0-8898-82321ab295ad`。

## 1. 用户的原话需求

> "帮我把这个程序分离出一个摄像头捕获视频并存储的小 demo，界面也可以简化一下，就是左侧有一个大的画布，右侧有一个开始录制的按钮，按下之后捕获摄像头的实时画面录制成视频，再点击一下结束录制"

## 2. 当前目录情况（重要）

| | 路径 | 说明 |
| --- | --- | --- |
| 旧会话工作区 | `F:\deepseek_harness\cells_detect` | 上一轮开发所在地，**本会话的沙箱只能写这里** |
| 新会话工作区 | `D:\repos\Projects\cells_detect` | 你现在所在目录 |
| 关系 | 同一个 git 仓库的两个克隆 | `origin git@github.com:Humble-Engineer/cells_detect.git`，分支 `ch`，HEAD 均为 `808ebc6` |

两边内容已逐文件核对一致（1187 / 1182 个文件，D: 少的 5 个只是旧工作区的 `.dsh-meow` 记忆库），**代码无需再搬**。

未提交内容：`capture_demo/` 在两个克隆里都是 untracked（`?? capture_demo/`）。要不要 `git add/commit/push` 由你定；注意两边各自提交会造成分叉，建议只在一边提交后推拉同步。

## 3. 本次交付物

- `capture_demo/capture_demo.py` —— 独立摄像头录制 demo（单文件，不依赖 `MainWindow.ui` / `modules/`，可单独拷走）
- `capture_demo/README.md` —— 用法与踩坑说明

界面与行为：

- 左侧一块大画布（黑底）实时预览，随窗口缩放，保持比例；
- 右侧一个按钮：`● 开始录制` → 打开摄像头、预览、同时写盘；再点变 `■ 结束录制` → 停止写盘、保存、释放摄像头，画布保留最后一帧；
- 录制中右侧显示 `● 录制中` + 大号计时；结束后显示 `已保存 mm:ss / N 帧`；
- 输出：`capture_demo/videos/YYYYmmdd_HHMMSS.mp4`（编码器按 `mp4v → XVID → MJPG` 依次兜底）。

运行环境与命令：

```powershell
D:\anaconda3\envs\opencv\python.exe capture_demo\capture_demo.py
```

参数：`--camera`（序号，默认 0 自动探测 0~3；也可传视频文件路径做无硬件自测）、`--width/--height`（默认 0 = 用摄像头自身分辨率）、`--fps`（兜底帧率，默认 25）、`--out`（输出目录）。

## 4. 本机摄像头的三个坑（已写进代码）

1. **MSMF 打开成功却读不出帧**：`cv2.VideoCapture(1)`（默认 MSMF）`isOpened()=True`，但 `read()` 一直报
   `can't grab frame. Error: -2147024891`；换 `cv2.CAP_DSHOW` 才正常。→ demo 里 Windows 下优先 DSHOW，且打开后必须试读一帧才算成功。
2. **强制设不支持的分辨率会出黑帧**：本机摄像头原生 640×480，设成 1280×720 后驱动"接受"了但每帧全黑（`std=0`）且回帧速度异常。→ 默认不设置分辨率。
3. **上报帧率 ≠ 实际帧率**：本机摄像头上报 30 fps，实际约 1 fps。按上报值写 `VideoWriter` 会让播放快 30 倍。→ 先缓冲 3 帧／0.3 秒测出实测帧率，再创建 writer 并把缓冲帧补写进去。

另外：本机摄像头在 **index 1**（0/2/3 无设备），自动探测会找到它。

## 5. 已验证情况

- 合成视频源当相机：录出 60 帧 / 19.69 fps 的可读 mp4；
- 真实摄像头（走自动探测 0→1）：录出 5 帧 / 1.00 fps，帧率按实测写入；
- 真实 Windows 图形平台冒烟：窗口正常弹出，画布拿到 814×610 预览图并成功落盘；
- 临时自测脚本与产物已清理，工作区只留 `capture_demo/`。

## 6. 待办 / 可选改进

- [ ] **预览模式可切换**：现在「结束录制」会一并关闭预览并释放摄像头（再点要重新开，约 1 秒）。用户提过另一种偏好：预览常开、按钮只切换是否写盘。可按需改成那种模式。
- [ ] **主程序 `modules/camera.py` 同样有坑**：它用的是默认后端（本机 MSMF 读不出帧），建议改成优先 `cv2.CAP_DSHOW`；另外它在子线程里直接调 `algorithm.count()` → 间接操作 Qt 控件（`display_image`），跨线程刷 UI 不安全，建议改成信号槽。
- [ ] `capture_demo/` 尚未纳入 git。
- [ ] 可选：把 `F:\deepseek_harness\cells_detect\.dsh-meow\` 拷到本项目根目录，可把旧工作区的 meow-memory 记忆（项目结构、环境、摄像头经验）一起带过来；不拷则新工作区的记忆库是空的。
