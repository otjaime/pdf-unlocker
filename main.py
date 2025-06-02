from flask import Flask, request, jsonify
from pypdf import PdfReader
import os

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"message": "PDF Unlock API is running. POST to /unlock"})

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    try:
        uploaded_file = request.files["file"]
        password      = request.form["password"]

        # save the incoming PDF
        input_path = "input.pdf"
        uploaded_file.save(input_path)

        # read & decrypt
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            reader.decrypt(password)

        # extract all text
        full_text = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            full_text.append(txt)
        text = "\n\n".join(full_text)

        os.remove(input_path)
        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


    app.run(host="0.0.0.0", port=port)
