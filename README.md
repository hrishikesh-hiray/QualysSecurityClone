# CyferTrace Security Platform (QualysSecurityClone)

A full-stack, modern cybersecurity platform inspired by Qualys.com, built with Flask, SQLAlchemy, and modern frontend technologies. CyferTrace provides advanced vulnerability scanning, reporting, and security research tools for web applications and cloud infrastructure.

---

## Features

- **Web Application Security Scanner**
  - Scan any web application for vulnerabilities (mock/demo results for local/dev)
  - Detects XSS, SQL Injection, authentication issues, security headers, and more
  - Beautiful, accessible UI with real-time scan progress and downloadable reports (PDF/JSON)

- **Infrastructure as Code (IaC) Scanner**
  - Upload and scan IaC files for misconfigurations (mock/demo results)
  - Supports best practices for AWS, Azure, GCP, and more

- **Admin Dashboard**
  - View scan history, statistics, and manage users
  - Secure login/logout with Flask-Login

- **Blog/Research Section**
  - Latest security research, news, and best practices

- **Modern UI/UX**
  - Responsive, dark-themed design with Tailwind CSS and custom styles
  - Accessible forms, navigation, and feedback

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend:** Jinja2 templates, Tailwind CSS, custom CSS, Font Awesome
- **Database:** SQLite (default, for local/dev), PostgreSQL (for production)
- **Other:** Gunicorn (for deployment), python-dotenv, ReportLab (PDF reports)

---

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/hrishikesh-hiray/QualysSecurityClone.git
   cd QualysSecurityClone
   ```
2. **Create a virtual environment and install dependencies:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   - Copy `.env.example` to `.env` and set your secrets (or use the provided `.env`)
   - By default, uses SQLite for local development

4. **Run the application:**
   ```sh
   flask run
   # or for production
   gunicorn --bind 0.0.0.0:5000 main:app
   ```
5. **Access the app:**
   - Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser

---

## Project Structure

```
QualysSecurityClone/
├── app.py                # Flask app and configuration
├── main.py               # App entry point
├── models.py             # SQLAlchemy models
├── routes.py             # Flask routes/views
├── security_tools.py     # WAS/IaC scanner logic (mock/demo)
├── report_generator.py   # PDF report generation
├── templates/            # Jinja2 HTML templates
├── static/               # CSS, JS, images
├── uploads/              # Uploaded files
├── reports/              # Generated reports
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── .gitignore            # Git ignore rules
└── ...
```

---

## Demo Credentials
- **Admin:**
  - Username: `admin`
  - Password: `admin123`

---

## Deployment
- Ready for deployment on Replit, Heroku, or any cloud supporting Python/Flask.
- Gunicorn is used for production serving.
- PostgreSQL support is available for production (see `.env` and `requirements.txt`).

---

## License
This project is for educational and demonstration purposes only. Not for production use without further security review.

---

## Credits
- Inspired by [Qualys.com](https://www.qualys.com/)
- Built by Team CyferTrace
