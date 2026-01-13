from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(email='admin@sms.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@sms.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Email: admin@sms.com")
        print("Password: admin123")
    else:
        print("Admin user already exists.")
