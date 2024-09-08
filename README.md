# File Encryptor/Decryptor

This project is a **Bulk File Encryptor/Decryptor** tool built with **Flask** on the backend and a futuristic-style **HTML/CSS (Tailwind CSS)** frontend. It allows users to upload files for bulk encryption and decryption using **server-side encryption** using **Python** and **Fernet** from the `cryptography` library.

## Features

- **File Encryption**: Encrypt multiple files using a secure key.
- **File Decryption**: Decrypt previously encrypted files.
- **Bulk File Processing**: Upload multiple files at once for processing.
- **Futuristic UI**: A modern, sleek user interface designed with **Tailwind CSS** for a futuristic feel.
- **Server-Side Encryption**: Encryption key is stored securely in the `.env` file for safe server-side encryption.
  
## Project Structure

```
.
├── templates/
│   └── index.html        # Frontend HTML (Futuristic UI)
├── static/
│   └── css/              # Tailwind CSS integration
├── app.py                # Flask backend code (API routes)
├── deploy.sh             # Shell script for automated deployment
├── .env                  # Environment file (for storing encryption keys)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **Flask**: Python web framework
- **Git**: To clone the repository
- **pip**: Python package installer

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory with your encryption key. Alternatively, run the `deploy.sh` script to automatically generate the `.env` file.

**Manually create `.env`:**
```bash
touch .env
```

Inside the `.env` file, add the following line:

```
ENCRYPTION_KEY='your-32-byte-base64-key'
```

If you don't have a key, you can generate one using `openssl`:

```bash
openssl rand -base64 32
```

### 4. Run the Application

You can run the Flask application locally using:

```bash
python app.py
```

By default, the app will be available at `http://localhost:5000`.

### 5. Deploy Using `deploy.sh`

The project includes a **deployment script** (`deploy.sh`) to automate the setup and deployment process.

To deploy:

1. Make the script executable:
   ```bash
   chmod +x deploy.sh
   ```

2. Run the script:
   ```bash
   ./deploy.sh
   ```

This script will:
- Clone the latest code from the repository.
- Install the necessary Python dependencies.
- Generate the `.env` file (if not present).
- Run the Flask app.

## API Endpoints

### `/encrypt` (POST)
Upload files for encryption. The API will encrypt each file and return a ZIP file containing the encrypted versions.

#### Example:
```bash
curl -X POST -F "files=@file1.txt" -F "files=@file2.txt" http://localhost:5000/encrypt
```

### `/decrypt` (POST)
Upload encrypted files for decryption. The API will return a ZIP file containing the decrypted versions.

#### Example:
```bash
curl -X POST -F "files=@encrypted_file1.txt" -F "files=@encrypted_file2.txt" http://localhost:5000/decrypt
```

## Frontend (Futuristic Design)

The frontend uses **Tailwind CSS** to provide a sleek, futuristic design. The UI has two main sections:
- **Encrypt Files**: Allows users to select multiple files and encrypt them.
- **Decrypt Files**: Allows users to select multiple encrypted files and decrypt them.

The design includes:
- Neon glow effects
- Gradient backgrounds
- Smooth hover effects on buttons

## Future Enhancements

- **Improved Error Handling**: Add better error handling for file upload failures.
- **Drag-and-Drop UI**: Implement a drag-and-drop feature for file uploads.
- **Progress Indicators**: Show file encryption/decryption progress to the user.

## License

This project is licensed under the MIT License.