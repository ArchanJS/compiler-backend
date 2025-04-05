from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import subprocess
import datetime

app = Flask(__name__)
app = Flask(__name__)
CORS(app)
UPLOAD_DIR = "code_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

EXTENSIONS = {
    "py": ("py", "3.10.4"),
    "c": ("c", "GCC 9.4.0"),
    "cpp": ("cpp", "G++ 9.4.0"),
    "java": ("java", "OpenJDK 11"),
    "js": ("js", "Node.js 14.x"),
    "go": ("go", "1.13")
}

@app.route("/compile", methods=["POST"])
def compile_code():
    data = request.get_json()
    code = data.get("code")
    lang = data.get("language")
    user_input = data.get("input", "")

    if lang not in EXTENSIONS:
        return jsonify({
            "success": False,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "error": "Unsupported language"
        }), 400

    file_ext, version = EXTENSIONS[lang]
    filename = f"{uuid.uuid4()}.{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "w") as f:
        f.write(code)

    try:
        result = subprocess.run([
            "python3", "executor.py", 
            lang,
            filepath
        ], input=user_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)

        return jsonify({
            "success": True,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "output": result.stdout or result.stderr,
            "language": lang,
            "version": version
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "error": "Execution timed out",
            "language": lang,
            "version": version
        }), 408

    except Exception as e:
        return jsonify({
            "success": False,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "error": str(e),
            "language": lang,
            "version": version
        }), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))