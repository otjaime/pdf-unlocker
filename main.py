from flask import Flask, request, jsonify
import os
from pypdf import PdfReader

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "PDF Unlock API is running. POST to /unlock"})

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    try:
        # Recibe el archivo y la contraseña
        uploaded_file = request.files["file"]
        password = request.form.get("password", "")

        # Guarda el PDF recibido
        input_path = "input.pdf"
        uploaded_file.save(input_path)

        # Lee y desbloquea el PDF usando PyPDF
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            reader.decrypt(password)

        # Extrae todo el texto
        full_text = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            full_text.append(txt)
        text = "\n\n".join(full_text)

        # Limpia el archivo
        os.remove(input_path)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
