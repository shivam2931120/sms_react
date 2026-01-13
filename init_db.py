"""
Database initialization script for Supabase/PostgreSQL
Run this after connecting to a new database to create tables and admin user
"""
from app import create_app, db
from app.models import User, Department, Class, Subject

def init_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created!")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@sms.edu',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created (username: admin, password: admin123)")
        else:
            print("ℹ️ Admin user already exists")
        
        # Create sample department if none exists
        if not Department.query.first():
            dept = Department(name='Computer Science', code='CS')
            db.session.add(dept)
            db.session.commit()
            print("✅ Sample department created")
        
        print("\n🎉 Database initialization complete!")
        print("You can now login with:")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == '__main__':
    init_database()
