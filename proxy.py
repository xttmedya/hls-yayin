from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "❌ URL parametresi eksik.", 400

    try:
        resp = requests.get(url, stream=True, verify=False)
        return Response(resp.iter_content(chunk_size=8192), content_type=resp.headers.get('Content-Type'))
    except Exception as e:
        return f"⚠️ Proxy hatası: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
