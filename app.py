from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    # إرسال طلب إلى الحاويتين الأخريين
    response_tp41 = requests.get("http://tp4.1:5000")
    response_tp42 = requests.get("http://tp4.2:5000")
    return f"""
    <h1>CONTENEUR PRINCIPALE (TP4)</h1>
    <p>MESSAGE TP4.1: {response_tp41.text}</p>
    <p> MESSAGE TP4.2: {response_tp42.text}</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)