#!/bin/bash
pip install -r requirements.txt
ENCRYPTION_KEY='your_encryption_key'
touch .env
echo "ENCRYPTION_KEY=$ENCRYPTION_KEY" >> .env