from flask import Flask, request, jsonify
import pikepdf
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "PDF Unlock API is running. Send POST requests to /unlock endpoint."})

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    try:
        # Recibe el archivo y la contraseña
        uploaded_file = request.files["file"]
        password = request.form.get("password", "")

        # Guarda el PDF recibido
        input_path = "input.pdf"
        unlocked_path = "unlocked.pdf"
        uploaded_file.save(input_path)

        # Desbloquea el PDF usando pikepdf
        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(unlocked_path)

        # Extrae texto con PyMuPDF (fitz)
        doc = fitz.open(unlocked_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()

        # Limpia archivos
        os.remove(input_path)
        os.remove(unlocked_path)

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)

