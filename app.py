import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Read token and chat id from environment variables (set by the hosting service)
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError('BOT_TOKEN and CHAT_ID environment variables must be set')
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('msg', '').strip()
        if not text:
            flash('กรุณาพิมพ์ข้อความก่อนส่ง', 'error')
            return redirect(url_for('index'))
        payload = {'chat_id': CHAT_ID, 'text': text}
        try:
            r = requests.post(API_URL, json=payload, timeout=10)
            r.raise_for_status()
            flash('ส่งข้อความไปยัง MeBot เรียบร้อย 🎉', 'success')
        except Exception as e:
            flash(f'ส่งไม่สำเร็จ: {e}', 'error')
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    # Bind to 0.0.0.0 so Render can access the service
    app.run(host='0.0.0.0', port=5000, debug=True)
