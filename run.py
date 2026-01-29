from app import create_app, db
from sqlalchemy import text

app = create_app()

# Auto-migration for Vercel/Production
# This ensures the 'is_approved' column exists even if migration scripts weren't run manually
with app.app_context():
    try:
        with db.engine.connect() as conn:
            # Add column safely
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_approved BOOLEAN DEFAULT FALSE"))
            # Ensure existing users are approved (safe to run multiple times)
            conn.execute(text("UPDATE users SET is_approved = TRUE WHERE is_approved IS NULL"))
            conn.commit()
            print("Database schema patched: verified 'is_approved' column.")
    except Exception as e:
        print(f"Database patch warning: {e}")

if __name__ == '__main__':
    app.run(debug=True)