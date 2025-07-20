# CyferTrace Security Platform

## Overview
CyferTrace is a full-stack cybersecurity platform built as a Qualys.com clone. It provides comprehensive security solutions including web application scanning and infrastructure as code analysis. The platform features a modern web interface, administrative dashboard, and AI-powered security tools.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: HTML templates with Tailwind CSS for styling
- **JavaScript**: Vanilla JS with custom scanner functionality
- **Responsive Design**: Mobile-first approach using Tailwind's grid system
- **UI Components**: Font Awesome icons, Chart.js for data visualization
- **Template Engine**: Jinja2 templates extending from a base layout

### Backend Architecture
- **Framework**: Flask web framework
- **Database**: SQLAlchemy ORM with support for multiple databases (SQLite default, PostgreSQL ready)
- **Authentication**: Flask-Login for session management
- **File Handling**: Werkzeug for secure file uploads
- **Security**: ProxyFix middleware for proper header handling behind proxies

### Key Components

#### Models (models.py)
- **User**: Authentication and authorization with role-based access
- **SecurityScan**: Tracks scan requests, results, and status
- **BlogPost**: Content management for news/blog functionality

#### Security Tools (security_tools.py)
- **WASScanner**: Web Application Security scanner using OWASP ZAP
- **IaCScanner**: Infrastructure as Code scanner using Checkov
- Both tools support fallback mock implementations when dependencies aren't available

#### Report Generation (report_generator.py)
- **PDFReportGenerator**: Creates downloadable PDF reports using ReportLab
- Structured reporting with custom styling and vulnerability categorization

#### Web Interface
- **Admin Dashboard**: System overview with scan statistics and management
- **Scanner Interfaces**: Dedicated pages for WAS and IaC scanning
- **Content Pages**: Industry solutions, research, and company information

## Data Flow

### Scan Workflow
1. User submits scan request through web interface
2. System validates input and creates SecurityScan record
3. Background scanner processes the request
4. Results are stored and made available for download
5. Real-time progress updates via JavaScript polling

### Authentication Flow
1. Users log in through dedicated login page
2. Flask-Login manages session state
3. Protected routes require authentication
4. Admin dashboard restricted to admin users

## External Dependencies

### Security Tools
- **OWASP ZAP**: Web application vulnerability scanning
- **Checkov**: Infrastructure as code security analysis
- Both tools gracefully degrade to mock implementations if not installed

### Python Packages
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and migrations
- **ReportLab**: PDF report generation
- **Werkzeug**: WSGI utilities and security helpers

### Frontend Libraries
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library
- **Chart.js**: Data visualization for dashboards

## Deployment Strategy

### Environment Configuration
- Database URL configurable via environment variables
- Session secrets managed through environment variables
- Upload directories created automatically
- Support for both development and production configurations

### File Structure
- Static assets served from `/static` directory
- File uploads stored in `/uploads` directory
- Generated reports saved to `/reports` directory
- Templates organized by functionality

### Database Support
- Primary: SQLite for development
- Production-ready: PostgreSQL support via DATABASE_URL
- Connection pooling and health checks configured
- Automatic table creation on startup

### Security Considerations
- CSRF protection through Flask's secret key mechanism
- Secure file upload handling with size limits
- SQL injection prevention via SQLAlchemy ORM
- XSS protection through template escaping