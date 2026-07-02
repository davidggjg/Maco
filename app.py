from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "alive", "message": "Mako API Proxy is running!"})

@app.route('/get-link')
def get_link():
    # כתובת ה-API של האפליקציה
    api_url = "https://pip-api.12plus.tv/playlist/v1/live/8/variant.json"
    
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-G973F Build/QP1A.190711.020)",
        "Accept-Encoding": "gzip"
    }
    
    try:
        # פנייה ל-API מתוך השרת של Render
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        # חילוץ הקישור
        stream_url = data['media']['url']
        return jsonify({
            "status": "success",
            "url": stream_url
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
