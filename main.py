from flask import Flask, request, jsonify
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PDF Unlocker API is running!"})

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    uploaded_file = request.files["file"]
    password = request.form.get("password", "")

    input_path = "input.pdf"
    unlocked_path = "unlocked.pdf"
    uploaded_file.save(input_path)

    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            if not reader.decrypt(password):
                return jsonify({"error": "Failed to decrypt PDF with provided password"}), 400

        writer = PdfWriter()
        text = ""

        for page in reader.pages:
            writer.add_page(page)
            # Extraer texto con manejo de errores
            try:
                extracted_text = page.extract_text() or ""
                text += extracted_text + "\n\n"
            except Exception as e:
                # Saltar la página problemática sin romper todo
                print(f"Warning: could not extract text from a page: {str(e)}")
                continue

        with open(unlocked_path, "wb") as f_out:
            writer.write(f_out)

        os.remove(input_path)
        os.remove(unlocked_path)

        return jsonify({"text": text.strip()})

    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
