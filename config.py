import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DB_URL')
    
    if database_url:
        # Standardize scheme
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
        # URL encode password if it contains @
        try:
            from urllib.parse import quote_plus
            if '://' in database_url:
                scheme, rest = database_url.split('://', 1)
                if '@' in rest:
                    auth_part, host_part = rest.rsplit('@', 1)
                    if ':' in auth_part:
                        user, password = auth_part.split(':', 1)
                        if '@' in password:
                            database_url = f"{scheme}://{user}:{quote_plus(password)}@{host_part}"
        except:
            pass

    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///site.db'
    
    # Supabase Connection Pooling Recommendation:
    # Use the **Session Pooler (Port 5432)** for this application.
    # Why? Flask-SQLAlchemy manages sessions and transaction states that may break with Transaction Pooling (Port 6543)
    # properly unless you disable prepared statements and manage transactions manually.
    # The Session Pooler works like a direct connection but multiplexes the underlying connections, which is safer here.
    
    # Supabase Session Pooler Optimizations
    if SQLALCHEMY_DATABASE_URI and 'postgresql' in SQLALCHEMY_DATABASE_URI:
        if 'sslmode' not in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += ('&' if '?' in SQLALCHEMY_DATABASE_URI else '?') + 'sslmode=require'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,            # Small pool to avoid exhausting Supabase connections
        'max_overflow': 10,
        'pool_recycle': 300,       # Recycle connections every 5 mins
        'pool_pre_ping': True,     # Test connection before using
        'connect_args': {
            'sslmode': 'require',
            'connect_timeout': 10
        }
    }
    
    # Upload configurations
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Session
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
