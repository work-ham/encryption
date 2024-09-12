from flask import Flask, render_template, request, send_file,   jsonify, send_from_directory
import os
from cryptography.fernet import Fernet
import os
import io
import zipfile
from dotenv import load_dotenv
import time
load_dotenv()
app = Flask(__name__)

# Generate and store a key for encryption/decryption
key = os.getenv('ENCRYPTION_KEY')
cipher = Fernet(key)
ENCRYPTED_FOLDER = "encrypted"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collection', endpoint='gallery_page')
def gallery():
    return render_template('gallery.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_files():
    files = request.files.getlist('files')
    encrypted_files = []

    for file in files:
        filename = file.filename
        file_path = os.path.join('uploads', filename)

        # Save the original file
        file.save(file_path)

        # Read the file data
        with open(file_path, 'rb') as f:
            data = f.read()

        # Encrypt the data
        encrypted_data = cipher.encrypt(data)

        # Save the encrypted file
        encrypted_file_path = os.path.join('encrypted', 'encrypted_' + filename)
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)

        encrypted_files.append(encrypted_file_path)

    # Create a zip file with all encrypted files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in encrypted_files:
            if os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(file_path))
            else:
                print(f"File not found: {file_path}")
    zip_buffer.seek(0)

    return send_file(zip_buffer, as_attachment=True, download_name="encrypted_files.zip", mimetype='application/zip')

# Ensure the 'temp' directory exists
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Fernet encryption key (use the same key for encryption and decryption)
fernet_key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(fernet_key)

# Decrypt file function
def decrypt_file(file_path):
    # Read the encrypted file
    with open(file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Decrypt the file
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Create a new decrypted file path
    if not file_path.startswith('decrypted_'):
        decrypted_file_path = file_path.replace('encrypted_', 'decrypted_')
    else:
        decrypted_file_path = file_path  # Avoid adding 'decrypted_' twice

    # Save the decrypted file
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    return decrypted_file_path

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'files' not in request.files:
        return "No file part", 400

    files = request.files.getlist('files')
    decrypted_files = []

    for uploaded_file in files:
        if uploaded_file.filename == '':
            continue

        # Save the file temporarily
        temp_file_path = os.path.join(TEMP_DIR, 'encrypted_' + uploaded_file.filename)
        uploaded_file.save(temp_file_path)

        # Decrypt the file
        decrypted_file_path = decrypt_file(temp_file_path)
        decrypted_filename = os.path.basename(decrypted_file_path)
        
        # Determine file type
        file_type = 'image' if decrypted_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) else 'video'
        
        decrypted_files.append({
            'filename': decrypted_filename,
            'type': file_type
        })

    return jsonify(decrypted_files)

def gallery_decrypt_file(file_path, output_folder):
    """Decrypt a single file and save it to the output folder."""
    try:
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        
        decrypted_filename = file_path.replace('encrypted_', 'decrypted_')
        decrypted_path = os.path.join(output_folder, os.path.basename(decrypted_filename))
        
        with open(decrypted_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        return decrypted_path
    except Exception as e:
        print(f"Error decrypting file {file_path}: {e}")
        return None

# Route to display gallery
@app.route('/gallery')
def gallery_files():
    encrypted_folder = 'encrypted'  # Folder where encrypted files are stored
    decrypted_folder = 'temp/gallery'       # Folder where decrypted files will be stored
    files = []

    # Create the decrypted folder if it doesn't exist
    if not os.path.exists(decrypted_folder):
        os.makedirs(decrypted_folder)
    
    # Decrypt all files in the encrypted folder
    for filename in os.listdir(encrypted_folder):
        file_path = os.path.join(encrypted_folder, filename)
        
        if filename.endswith(('png', 'jpg', 'jpeg', 'mp4')):
            decrypted_path = gallery_decrypt_file(file_path, decrypted_folder)
            file_type = 'image' if decrypted_path.endswith(('png', 'jpg', 'jpeg')) else 'video'
            files.append({'filename': os.path.basename(decrypted_path), 'type': file_type})

    return jsonify(files)

# Serve the decrypted files from the temp directory
@app.route('/temp/<filename>')
def serve_file(filename):
    return send_from_directory(TEMP_DIR, filename)
@app.route('/temp/gallery/<path:filename>')
def gallery_serve_file(filename):
    return send_from_directory('temp/gallery', filename)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('encrypted', exist_ok=True)
    os.makedirs('decrypted', exist_ok=True)
    app.run(host='0.0.0.0')
