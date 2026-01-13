"""
Shikshan - Create Admin User for Production
Run this script to create an admin user for your deployment:
    python create_admin.py
"""
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def create_admin():
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Get admin credentials
        print("\n🔐 Shikshan Admin Setup")
        print("-" * 30)
        
        username = input("Enter admin username: ").strip()
        if not username:
            print("❌ Username is required!")
            return
        
        # Check if user exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"❌ User '{username}' already exists!")
            return
        
        email = input("Enter admin email: ").strip()
        if not email:
            email = f"{username}@shikshan.local"
        
        password = input("Enter admin password (min 6 chars): ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters!")
            return
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            role='admin'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"\n✅ Admin user '{username}' created successfully!")
        print(f"   Email: {email}")
        print(f"   Role: admin")
        print("\nYou can now login at /login")

if __name__ == '__main__':
    create_admin()
