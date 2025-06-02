from flask import Flask, request, jsonify
import os
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber

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
            reader.decrypt(password)
        except Exception as e:
            return jsonify({"error": f"Failed to decrypt PDF: {str(e)}"}), 400

    # Guardar el PDF desbloqueado
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(unlocked_path, "wb") as f_out:
        writer.write(f_out)

    # Usar pdfplumber para extraer texto
    text = ""
    with pdfplumber.open(unlocked_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n\n"

    # Limpiar archivos
    os.remove(input_path)
    os.remove(unlocked_path)

    return jsonify({"text": text})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
