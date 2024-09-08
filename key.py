from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os
import io
import zipfile
app = Flask(__name__)

# Generate and store a key for encryption/decryption
key = Fernet.generate_key()
print(Fernet.generate_key())