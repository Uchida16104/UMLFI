#!/bin/bash
set -e

echo "Starting UMLFI Deployment..."

# Python venv setup
python3 -m venv venv
source venv/bin/activate

# Core Stack Installation
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pandas scikit-learn numpy requests

# Frontend Setup
cd frontend
npm install
cd ..

echo "All components installed successfully."