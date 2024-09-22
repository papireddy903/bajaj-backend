from flask import Flask, request, jsonify
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_mime_type(base64_string):
    if base64_string.startswith("data:"):
        mime_info = base64_string.split(";")[0]
        mime_type = mime_info.split(":")[1]
        return mime_type
    return "doc/pdf"

def format_file_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} Bytes"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"

@app.route('/bfhl', methods=['POST'])
def process_data():
    data = request.json
    user_id = "john_doe_17091999"
    email = "john@xyz.com"
    roll_number = "ABCD123"
    
    if 'data' not in data:
        return jsonify({"is_success": False, "user_id": user_id}), 400

    raw_data = data['data']
    numbers = [item for item in raw_data if item.isdigit()]
    alphabets = [item for item in raw_data if item.isalpha()]
    highest_lowercase = [max(filter(str.islower, alphabets), default=None)] if alphabets else []

    file_b64 = data.get('file_b64')
    file_valid, file_mime_type, file_size = False, None, 0

    if file_b64:
        try:
            file_data = base64.b64decode(file_b64)
            file_valid = True
            file_size = len(file_data)
            file_mime_type = get_mime_type(file_b64)
        except Exception:
            file_valid = False

    file_size_formatted = format_file_size(file_size)

    response = {
        "is_success": True,
        "user_id": user_id,
        "email": email,
        "roll_number": roll_number,
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": highest_lowercase,
        "file_valid": file_valid,
        "file_mime_type": file_mime_type,
        "file_size": file_size_formatted
    }
    
    return jsonify(response)

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True)
