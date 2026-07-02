from flask import Flask, jsonify
import requests
import urllib3

# ביטול התראות אבטחה על אישור ה-SSL בגלל השימוש ב-IP ישיר
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "alive", "message": "Bridge is active"})

@app.route('/get-link')
def get_link():
    # פנייה ל-IP הישיר במקום לדומיין שנחסם ב-DNS
    api_url = "https://185.151.200.22/playlist/v1/live/8/variant.json"
    
    # הגדרת כותרות (Headers) כדי לגרום לשרת לחשוב שמגיעים מהאפליקציה הרשמית
    headers = {
        "Host": "pip-api.12plus.tv",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; SM-G973F Build/QP1A.190711.020)",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive"
    }
    
    try:
        # verify=False מאפשר פנייה ל-IP ללא התאמת תעודת SSL של הדומיין
        response = requests.get(api_url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            # חילוץ הקישור מהמבנה שהשרת מחזיר
            stream_url = data['media']['url']
            return jsonify({"status": "success", "url": stream_url})
        else:
            return jsonify({"status": "error", "message": f"Server returned status {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
