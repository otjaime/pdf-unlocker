from flask import Flask, request, jsonify
import os
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "PDF Unlocker API is running!"})

@app.route("/unlock", methods=["POST"])
def unlock_and_extract():
    uploaded_file = request.files["file"]
    password = request.form.get("password", "")

    input_path = "input.pdf"
    uploaded_file.save(input_path)

    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            if not reader.decrypt(password):
                return jsonify({"error": "Failed to decrypt PDF. Check the password."}), 400

        # Extraer texto (PyPDF2)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n\n"

    except Exception as e:
        return jsonify({"error": f"Error reading PDF: {str(e)}"}), 500
    finally:
        os.remove(input_path)

    return jsonify({"text": text})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
