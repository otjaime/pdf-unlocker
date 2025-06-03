from flask import Flask, request, jsonify, redirect
import pikepdf
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from pypdf import PdfReader
import os

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"message": "PDF Unlock API is running. Send POST requests to /unlock endpoint."})
    return jsonify({"message": "PDF Unlock API is running. POST to /unlock"})

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    try:
        uploaded_file = request.files['file']
        password      = request.form['password']
        uploaded_file = request.files["file"]
        password      = request.form["password"]

        input_path    = "input.pdf"
        unlocked_path = "unlocked.pdf"
        # save the incoming PDF
        input_path = "input.pdf"
        uploaded_file.save(input_path)

        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(unlocked_path)
        # read & decrypt
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            reader.decrypt(password)

        doc  = fitz.open(unlocked_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        # extract all text
        full_text = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            full_text.append(txt)
        text = "\n\n".join(full_text)

        os.remove(input_path)
        os.remove(unlocked_path)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
