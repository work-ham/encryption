from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os
import io
import zipfile
from dotenv import load_dotenv
import os

load_dotenv()  # This line brings all environment variables from .env into os.environ
print(os.getenv('ENCRYPTION_KEY'))  