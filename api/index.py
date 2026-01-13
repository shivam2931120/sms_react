from flask import Flask
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

# This is the entry point for Vercel
# Vercel expects a WSGI app named 'app' or 'application'
