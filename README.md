# College Management System (SMS)

A comprehensive Flask-based College/School Management System with admin, teacher, and student portals.

## Features

### 🎛️ Admin Dashboard
- Student, Teacher, Class, Subject management
- Attendance tracking with analytics
- Fee management
- Library system
- Exam & Homework management
- Role-based permissions

### 📊 Analytics
- Attendance trends (30-day charts)
- Student performance dashboard
- Department-wise statistics

### 👨‍🎓 Student Portal
- View attendance, marks, fees
- Class timetable
- Homework assignments

### 👨‍🏫 Teacher Portal
- Mark attendance (bulk)
- Enter grades
- View personal schedule

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL (Supabase) / SQLite (local dev)
- **Frontend**: Jinja2, Bootstrap 5, Chart.js
- **Deployment**: Vercel (serverless)

## Setup

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sms.git
cd sms
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

5. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run development server:
```bash
python run.py
```

### Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **Settings > Database > Connection string**
3. Copy the URI and add to your `.env`:
```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Vercel Deployment

1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables in Vercel dashboard:
   - `SECRET_KEY`
   - `DATABASE_URL` (Supabase connection string)
4. Deploy!

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `DATABASE_URL` | PostgreSQL connection string |
| `FLASK_ENV` | `development` or `production` |

## Default Admin Login

After running migrations, create an admin user:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@example.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
```

## Project Structure

```
sms/
├── api/
│   └── index.py          # Vercel serverless entry
├── app/
│   ├── routes/
│   │   ├── admin.py      # Admin routes
│   │   ├── student.py    # Student portal
│   │   └── teacher.py    # Teacher portal
│   ├── templates/
│   ├── static/
│   └── models.py
├── config.py
├── requirements.txt
├── vercel.json
└── run.py
```

## License

MIT License
