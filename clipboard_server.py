import sys
import os
import threading
import socket
import datetime
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import tkinter as tk
from tkinter import messagebox

# Clipboard access on Windows
import win32clipboard
from PIL import Image, ImageGrab, ImageOps

# 全局配置
IMAGE_DIR_NAME = 'ImageFile'
INVERT_ENABLED = False
server = None
server_thread = None


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class ClipboardHTTPRequestHandler(BaseHTTPRequestHandler):
    root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    username = ''
    password = ''

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="ClipboardServer"')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def authenticate(self):
        auth = self.headers.get('Authorization')
        if not auth:
            self.do_AUTHHEAD()
            return False
        try:
            import base64
            method, encoded = auth.split(' ', 1)
            if method != 'Basic':
                raise ValueError
            decoded = base64.b64decode(encoded).decode('utf-8')
            user, pwd = decoded.split(':', 1)
        except Exception:
            self.do_AUTHHEAD()
            return False
        if user == self.username and pwd == self.password:
            return True
        self.do_AUTHHEAD()
        return False

    def do_GET(self):
        if not self.authenticate():
            return
        path = unquote(self.path)
        if path == '/clipboard':
            self.handle_clipboard()
        else:
            self.serve_file(path.lstrip('/'))

    def handle_clipboard(self):
        result = {'Type': None, 'Text': None, 'File': None}
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                result = {'Type': 'Text', 'Text': text, 'File': None}
            else:
                img = ImageGrab.grabclipboard()
                if img:
                    if INVERT_ENABLED:
                        img = ImageOps.invert(img.convert('RGB'))
                    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"PyCS_{timestamp}.jpg"
                    image_dir = os.path.join(self.root_dir, IMAGE_DIR_NAME)
                    os.makedirs(image_dir, exist_ok=True)
                    filepath = os.path.join(image_dir, filename)
                    img.save(filepath, format='JPEG')
                    result = {'Type': 'Image', 'Text': None, 'File': f"{IMAGE_DIR_NAME}/{filename}"}
        except Exception as e:
            print(f"Clipboard error: {e}")
        finally:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

    def serve_file(self, filename):
        filepath = os.path.join(self.root_dir, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as f:
                    data = f.read()
                ext = os.path.splitext(filename)[1].lower()
                if ext in ('.png', '.jpg', '.jpeg', '.gif'):
                    ctype = f'image/{ext.lstrip(".")}'
                else:
                    ctype = 'application/octet-stream'
                self.send_response(200)
                self.send_header('Content-Type', ctype)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_error(500, f"Server Error: {e}")
        else:
            self.send_error(404, "File Not Found")


def start_server(port, username, password, status_label):
    global server
    ClipboardHTTPRequestHandler.username = username
    ClipboardHTTPRequestHandler.password = password
    server = HTTPServer(('', port), ClipboardHTTPRequestHandler)
    ip = get_local_ip()
    status_label.config(text=f" 服务器运行于 http://{ip}:{port}")
    try:
        server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
        messagebox.showerror(" 错误 ", f" 服务器启动失败 : {e}")


def stop_server(status_label, start_btn, stop_btn, restart_btn):
    global server
    if server:
        server.shutdown()
        server.server_close()
        server = None
    status_label.config(text=' 服务器已停止 ')
    start_btn.config(state='normal')
    stop_btn.config(state='disabled')
    restart_btn.config(state='disabled')


def main():
    global INVERT_ENABLED, server_thread
    root = tk.Tk()
    root.title('Clipboard HTTP Server')

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text=' 端口 :').grid(row=0, column=0, sticky='e')
    port_var = tk.StringVar(value='8888')
    tk.Entry(frame, textvariable=port_var, width=10).grid(row=0, column=1)

    tk.Label(frame, text=' 用户名 :').grid(row=0, column=2, sticky='e')
    user_var = tk.StringVar()
    tk.Entry(frame, textvariable=user_var, width=10).grid(row=0, column=3)

    tk.Label(frame, text=' 密码 :').grid(row=0, column=4, sticky='e')
    pass_var = tk.StringVar()
    tk.Entry(frame, textvariable=pass_var, show='*', width=10).grid(row=0, column=5)

    invert_var = tk.BooleanVar(value=False)
    tk.Checkbutton(frame, text=' 截图反色 ', variable=invert_var).grid(row=1, column=0, columnspan=2, sticky='w')

    status_label = tk.Label(root, text=' 服务器未运行 ', pady=5)
    status_label.pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    start_btn = tk.Button(btn_frame, text=' 启动服务器 ')
    stop_btn = tk.Button(btn_frame, text=' 停止服务器 ', state='disabled')
    restart_btn = tk.Button(btn_frame, text=' 重启服务器 ', state='disabled')
    start_btn.grid(row=0, column=0, padx=5)
    stop_btn.grid(row=0, column=1, padx=5)
    restart_btn.grid(row=0, column=2, padx=5)

    def on_start():
        global INVERT_ENABLED, server_thread
        try:
            port = int(port_var.get().strip())
        except ValueError:
            messagebox.showwarning(' 警告 ', ' 端口必须是数字 ')
            return
        username = user_var.get().strip()
        password = pass_var.get().strip()
        if not (username and password):
            messagebox.showwarning(' 警告 ', ' 请填写用户名和密码 ')
            return
        INVERT_ENABLED = invert_var.get()
        start_btn.config(state='disabled')
        stop_btn.config(state='normal')
        restart_btn.config(state='normal')
        server_thread = threading.Thread(
            target=start_server,
            args=(port, username, password, status_label),
            daemon=True
        )
        server_thread.start()

    def on_stop():
        stop_server(status_label, start_btn, stop_btn, restart_btn)

    def on_restart():
        on_stop()
        on_start()

    start_btn.config(command=on_start)
    stop_btn.config(command=on_stop)
    restart_btn.config(command=on_restart)

    root.mainloop()


if __name__ == '__main__':
    main()
