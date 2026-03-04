"""WIP Deadline Checker — 로컬 서버 (HTML 뷰어 + Windows 알림 통합)"""
import os
import sys
import json
import threading
import webbrowser
from pathlib import Path

from bottle import Bottle, static_file, request, response

app = Bottle()
BASE = Path(__file__).resolve().parent
notifier_thread = None


@app.route('/')
def index():
    return static_file('wip_checker.html', root=str(BASE))


@app.route('/api/upload', method='POST')
def upload_file():
    """엑셀 파일 업로드 → 임시 저장 후 경로 반환"""
    response.content_type = 'application/json'
    upload = request.files.get('file')
    if not upload:
        return json.dumps({"ok": False})
    save_dir = BASE / '.uploads'
    save_dir.mkdir(exist_ok=True)
    save_path = save_dir / upload.filename
    upload.save(str(save_path), overwrite=True)
    return json.dumps({"ok": True, "path": str(save_path)})


@app.route('/api/start-notifier', method='POST')
def start_notifier():
    """HTML에서 엑셀 업로드 후 호출 → 알림 스케줄러 시작"""
    global notifier_thread
    response.content_type = 'application/json'

    data = request.json or {}
    excel_path = data.get('path', '')

    if not excel_path or not os.path.exists(excel_path):
        return json.dumps({"ok": False, "msg": "파일 경로 없음"})

    try:
        from wip_notifier import load_config, save_config, run_scheduler
        cfg = load_config()
        cfg["excel_path"] = excel_path
        save_config(cfg)

        if notifier_thread and notifier_thread.is_alive():
            return json.dumps({"ok": True, "msg": "이미 실행 중"})

        notifier_thread = threading.Thread(
            target=run_scheduler, args=(cfg,), daemon=True
        )
        notifier_thread.start()
        return json.dumps({"ok": True, "msg": "알림 시작"})
    except Exception as e:
        return json.dumps({"ok": False, "msg": str(e)})


@app.route('/api/notifier-status')
def notifier_status():
    response.content_type = 'application/json'
    running = notifier_thread is not None and notifier_thread.is_alive()
    return json.dumps({"running": running})


if __name__ == '__main__':
    port = 8070
    url = f'http://localhost:{port}'
    print(f'[WIP Checker] {url} 에서 실행 중...')
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    app.run(host='localhost', port=port, quiet=True)
