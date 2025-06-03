from flask import Flask, request, jsonify
import os
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PDF Unlocker API is running! POST to /unlock"})

@app.route("/unlock", methods=["POST"])
def unlock_and_extract():
    try:
        # Recibe archivo y contraseña
        uploaded_file = request.files["file"]
        password = request.form.get("password", "")

        input_path = "input.pdf"
        uploaded_file.save(input_path)

        # Desbloquear PDF con pypdf
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            reader.decrypt(password)

        # Crear nuevo PDF desbloqueado
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open("unlocked.pdf", "wb") as f_out:
            writer.write(f_out)

        # Extraer texto del PDF desbloqueado
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n\n"

        # Limpiar archivos temporales
        os.remove(input_path)
        os.remove("unlocked.pdf")

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
