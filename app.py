from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
import base64
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Merhaba, uygulaman çalışıyor! 🚀"

@app.route("/decrypt", methods=["POST"])
def decrypt_media():
    try:
        data = request.json
        media_key_b64 = data.get("media_key")
        media_url = data.get("url")
        mime_type = data.get("mime_type")  # opsiyonel
        file_enc_sha256 = data.get("file_enc_sha256")  # opsiyonel

        if not media_key_b64 or not media_url:
            return jsonify({"error": "media_key ve url gerekli"}), 400

        media_key = base64.b64decode(media_key_b64)

        # Media Key'den AES anahtarlarını üretmek için HKDF kullanımı
        media_type_info = b"WhatsApp Image Keys"

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=112,
            salt=None,
            info=media_type_info,
            backend=default_backend()
        )
        media_derived = hkdf.derive(media_key)

        iv = media_derived[0:16]
        cipher_key = media_derived[16:48]
        mac_key = media_derived[48:80]

        # Şifrelenmiş dosyayı indir
        response = requests.get(media_url)
        if response.status_code != 200:
            return jsonify({"error": "Dosya indirilemedi"}), 400

        file_enc = response.content[:-10]  # son 10 byte: MAC
        cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(file_enc)

        # Padding temizliği (PKCS#7)
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]

        image_base64 = base64.b64encode(decrypted).decode("utf-8")

        return jsonify({
            "status": "success",
            "length": len(decrypted),
            "preview": base64.b64encode(decrypted[:20]).decode("utf-8"),  # ilk 20 byte örnek
            "base64": image_base64  # 👈 TAM GÖRSEL buradan alınacak
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
