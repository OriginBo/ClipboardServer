# ClipboardServer
一个可以一键把电脑剪贴板截图通过http请求发送给安卓手机和平板的项目

## 在开始使用之前

本应用极度特化，没有普适性，所以在你常识使用本应用之前，我推荐你尝试如下应用

### ClipShare

[ClipShare](https://clipshare.coclyun.top/)

体感最好用的剪贴板图片同步，我是遇到了 Windows 端无法识别复制的问题，但群里其他用户好像没有遇到

### Pic2Pad

[Pic2Pad](https://github.com/dangswing/Pic2Pad)

使用 LocalSend 来一键发送图片，需要安卓端的 LocalSend 一直挂在前台。

三星平板可以缩成一个图标挂在前台，很是优雅，但图标长期一片区域高亮我怕烧屏

本项目使用 MacroDroid 可以调节悬浮按钮的透明度，淡淡的一点，无惧烧屏！

### SyncClipboard

[SyncClipboard](https://github.com/Jeric-X/SyncClipboard)

本项目的启发者，也是本项目的完全体

但是 PotPlayer 反色视频截图存在问题，同时 MacroDroid 也需要自己设置，当然你也可以用此项目的模板魔改一下

## 适用场景

1. 听网课需要截图到平板做笔记
2. 只存在把电脑截图发送到手机平板的情况
3. 可能会需要把截图反色

## 使用方法

请先去 Release 下载发布的 zip 压缩包，并解压

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

4. 将下载的 ` clipboard_server.py ` 存放在刚才新建的文件夹中

### Android

1. 请在手机或平板上安装 MicroDroid

2. MicroDroid 导入预设宏
- 主屏幕选择「导出/导入」
- 选择导入
- 打开下载的 ` ClipboardServer.macro `

### MicroDroid 宏自定义

- 请先打开宏，并点击宏下方的「局部变量」
   - 填写「url」为你电脑的 ip 地址（例如：192.168.0.1）
   - 填写「port」为你开服务器时的端口号
   - 填写「userName」为你开服务器时设置的用户名
   - 填写「userCode」为你开服务器时设置的密码

1. 如果你有一个经常性连接的固定 WiFi（比如家里的），同时这个 WiFi 开启了 IP 绑定
   - 你可以修改 任何网络 成自己家的 WiFi
   - 你可以修改 192.168.0.0 成你电脑的 IP 地址

2. 如果你经常换 WiFi 或者 WiFi 地址不固定，你可以把从开头「如果」到第一个「结束条件」之间的内容删除
   - 这样你之后每次更换网络或 ip 地址，都会自动让你输入新的 IP 地址
  
3. 你还可以把倒数第七行的宏运行改成自动点击，帮你在下载的图片的时候自动点击笔记软件的插入图片
