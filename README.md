# ClipboardServer
一个可以把电脑截图通过http请求发送给安卓手机和平板的项目

## 适用场景

1. 听网课需要截图到平板做笔记
2. 只存在把电脑截图发送到手机平板的情况
3. 可能会需要把截图反色

## 使用方法

### Windows

1. 请先安装 Python
- Windows 应用商店搜索 Python
- 安装 ` Python 3.13 `

2. 请安装前置 Python 应用
- 随便打开一个文件夹
- 文件夹空白处右击
- 在终端中打开
- 输入命令：` pip install pywin32 pillow `
- 等待安装完成

3. 创建一个文件夹，文件夹路径中请不要包含中文

4. 将 ` clipboard_server.py ` 存放在刚才新建的文件夹中

### Android

1. 请在手机或平板上安装 MicroDroid

2. MicroDroid 导入预设宏
- 主屏幕选择「导出/导入」
- 选择导入
- 打开下载的

### MicroDroid 宏自定义

1. 如果你有一个经常性连接的固定 WiFi（比如家里的），同时这个 WiFi 开启了 IP 绑定
    1. 你可以修改 任何网络 成自己家的 WiFi
    2. 你可以修改 192.168.0.106 成你电脑的 IP 地址
