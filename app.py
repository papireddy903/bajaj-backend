from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
import magic  # Python package to detect file types

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to validate and process the file
def process_file(file_b64):
    try:
        # Decode the base64 string to get the file data
        file_data = base64.b64decode(file_b64)
        
        # Assuming files are stored temporarily for validation
        temp_file_path = "temp_file"
        with open(temp_file_path, "wb") as f:
            f.write(file_data)

        # Validate file
        file_valid = True

        # Use `magic` to detect the MIME type
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_file(temp_file_path)
        
        # Calculate file size in KB
        file_size_kb = os.path.getsize(temp_file_path) / 1024

        # Remove the temporary file after processing
        os.remove(temp_file_path)
        
        return file_valid, file_mime_type, file_size_kb
    except Exception as e:
        print(f"Error processing file: {e}")
        return False, "", 0

# GET endpoint
@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    response = {
        "operation_code": 1
    }
    return jsonify(response), 200

# POST endpoint
@app.route('/bfhl', methods=['POST'])
def post_data():
    try:
        data = request.json.get("data", [])
        file_b64 = request.json.get("file_b64", "")

        # Extracting user details
        user_id = "papireddy_22091998"  # Replace with your format
        email = "papireddy@example.com"  # Replace with your college email
        roll_number = "12345678"  # Replace with your college roll number

        # Separate numbers and alphabets
        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]

        # Find highest lowercase alphabet
        lowercase_alphabets = [item for item in alphabets if item.islower()]
        highest_lowercase_alphabet = [max(lowercase_alphabets)] if lowercase_alphabets else []

        # File validation
        file_valid, file_mime_type, file_size_kb = process_file(file_b64) if file_b64 else (False, "", 0)

        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_lowercase_alphabet,
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": round(file_size_kb, 2)
        }

        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"is_success": False}), 400

if __name__ == "__main__":
    app.run(debug=True)
