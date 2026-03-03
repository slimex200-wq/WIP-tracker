"""WIP Deadline Checker — Desktop App Wrapper"""
import webview
import os
import sys


def resource_path(relative_path):
    """PyInstaller 번들 내부 리소스 경로 반환"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)


if __name__ == '__main__':
    html_path = resource_path('wip_checker.html')
    window = webview.create_window(
        'WIP Deadline Checker',
        url=html_path,
        width=1400,
        height=900,
        min_size=(800, 600),
    )
    webview.start()
