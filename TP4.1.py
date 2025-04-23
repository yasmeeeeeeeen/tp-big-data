from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "COUCOU JE SUIS LE CONTENEUR TP4.1 🐳"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)