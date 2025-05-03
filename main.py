from flask import Flask, abort, request, jsonify
import os
import shutil

app = Flask(__name__)

## keys
KEYS = ["rayuwu"]

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")


os.makedirs(CONTENT_DIR, exist_ok=True)

@app.route("/get-image")
def get_image():
    key = request.args.get("key")
    filename = request.args.get("filename")

    if not key or not filename:
        abort(400, description="Missing key or filename.")

    if key not in KEYS:
        abort(404, description="Invalid verification key.")

    source_path = os.path.join(DOWNLOADS_DIR, filename)
    dest_path = os.path.join(CONTENT_DIR, filename)

    if not os.path.exists(source_path):
        abort(404, description="Image not found in Downloads folder.")

    
    try:
        shutil.copy2(source_path, dest_path)
    except Exception as e:
        abort(500, description=f"Failed to copy file: {str(e)}")

    return jsonify({"status": "success", "message": f"{filename} saved to /content"})

if __name__ == "__main__":
    app.run(debug=True)
