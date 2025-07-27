from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Merhaba, uygulaman çalışıyor!"

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    media_key = data.get('media_key')
    url = data.get('url')
    mime_type = data.get('mime_type')
    file_enc_sha256 = data.get('file_enc_sha256')

    if not all([media_key, url, mime_type, file_enc_sha256]):
        return jsonify({"success": False, "error": "Eksik parametre"}), 400

    # Örnek sahte dönüş (gerçek çözümleme kodunu buraya koymalısın)
    return jsonify({
        "success": True,
        "file_url": "https://senin-domenin/uploads/cozulmus_dosya.jpg"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
