from flask import Flask, request, jsonify
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PDF Unlocker + Extractor API is running!"})

@app.route("/unlock", methods=["POST"])
def unlock_and_extract():
    uploaded_file = request.files["file"]
    password = request.form.get("password", "")

    input_path = "input.pdf"
    unlocked_path = "unlocked.pdf"
    uploaded_file.save(input_path)

    # Intentar desbloquear con PyPDF2
    reader = PdfReader(input_path)
    if reader.is_encrypted:
        try:
            if reader.decrypt(password) == 0:
                return jsonify({"error": "Password incorrect or cannot unlock"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to decrypt PDF: {str(e)}"}), 400

    # Verificar si tiene páginas
    if not reader.pages:
        return jsonify({"error": "No pages found in PDF"}), 400

    # Guardar el PDF desbloqueado
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(unlocked_path, "wb") as f_out:
        writer.write(f_out)

    # Extraer texto con PyPDF2 directamente (sin pdfplumber)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n\n"

    # Limpiar archivos
    os.remove(input_path)
    os.remove(unlocked_path)

    return jsonify({"text": text})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
