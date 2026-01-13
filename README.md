# Shikshan - Education Management System

A comprehensive education management platform built with Flask, designed for schools and colleges.

## Features

- 🎓 **Student Management** - Enrollment, profiles, classes
- 👨‍🏫 **Teacher Portal** - Schedule, attendance, marks entry
- 📅 **Timetable** - Calendar-based schedule view
- 📊 **Analytics** - Performance and attendance insights
- 💰 **Fee Management** - Track payments and dues
- 🎫 **Hall Tickets** - Auto-generated (requires cleared fees)
- 📱 **Mobile Responsive** - Works on all devices

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
python init_db.py

# Create admin user
python create_admin.py

# Run development server
python run.py
```

### Deploy to Vercel

1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables in Vercel dashboard:
   - `SECRET_KEY` - Random secure string
   - `DATABASE_URL` - PostgreSQL connection URL
4. Deploy

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Session encryption key | Yes |
| `DATABASE_URL` | PostgreSQL connection URL | Yes |
| `FLASK_ENV` | `development` or `production` | No |

## Database Setup (Supabase)

1. Create a Supabase project
2. Get the connection string from Settings > Database
3. Add it as `DATABASE_URL` in your environment

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL (Supabase)
- **Frontend**: Bootstrap 5, FullCalendar
- **Deployment**: Vercel

## License

MIT License - © 2024 Shikshan
