import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

app = create_app()

# Auto-setup database tables for Vercel/Production
with app.app_context():
    try:
        # Create all tables if they don't exist
        db.create_all()
        print("✅ Database tables ensured")
        
        # Add is_approved column if missing
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_approved BOOLEAN DEFAULT FALSE"))
            conn.execute(text("UPDATE users SET is_approved = TRUE WHERE is_approved IS NULL"))
            conn.commit()
            print("✅ Database schema patched")
    except Exception as e:
        print(f"⚠️ Database setup warning: {e}")

# WSGI application for Vercel
application = app
