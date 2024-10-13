from flask import Flask, request, jsonify
import os
import hashlib
import datetime
import processImage
from processImage import *

# Initialize Flask app
app = Flask(__name__)

# Define upload folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
identifier = processImage.ImageProcessor()

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the request has a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if the file is a PNG
    if file.filename == '' or not file.filename.lower().endswith('.png'):
        return jsonify({"error": "Only PNG files are accepted"}), 400

    file.filename=hashlib.md5(file.filename.encode('utf-8') + datetime.date.today().strftime("%B %d, %Y").encode('utf-8')).hexdigest()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    match, compostable = identifier.process(file_path)
    # Return a success response
    return jsonify({"compostable": compostable,"message": match}), 200

# Start the Flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)