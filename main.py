from flask import Flask, request, jsonify, redirect
import pikepdf
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"message": "PDF Unlock API is running. Send POST requests to /unlock endpoint."})

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    try:
        uploaded_file = request.files['file']
        password      = request.form['password']

        input_path    = "input.pdf"
        unlocked_path = "unlocked.pdf"
        uploaded_file.save(input_path)

        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(unlocked_path)

        doc  = fitz.open(unlocked_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()

        os.remove(input_path)
        os.remove(unlocked_path)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
