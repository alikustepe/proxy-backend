from flask import Flask, request
import requests

app = Flask(__name__)

FIREBASE_URL = "https: // us - central1 - mobile - vehicle - control.cloudfunctions.net / konum_guncelle"   # kendi Firebase HTTPS fonksiyon URL'in
GIZLI_SIFRE = "COK_GIZLI_ARAC_SIFRESI_123"

@app.route("/api", methods=["GET", "POST"])
def api():
    try:
        if request.method == "POST":
            data = request.form.to_dict()
        else:
            data = request.args.to_dict()

        # Güvenlik kontrolü
        if data.get("sifre") != GIZLI_SIFRE:
            return "403", 403

        # Firebase Cloud Function’a ilet
        firebase_response = requests.post(FIREBASE_URL, data=data)

        return firebase_response.text, firebase_response.status_code

    except Exception as e:
        return f"Proxy Hatası: {e}", 500


@app.route("/")
def home():
    return "Proxy Çalışıyor"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
