from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

from app import app, db
from models import User, SecurityScan, BlogPost
from security_tools import WASScanner, IaCScanner
from report_generator import PDFReportGenerator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/industries')
def industries():
    return render_template('industries.html')

@app.route('/solutions')
def solutions():
    return render_template('solutions.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/news')
def news():
    # Get recent blog posts
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(10).all()
    return render_template('news.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    # Get recent scans
    recent_scans = SecurityScan.query.order_by(SecurityScan.created_at.desc()).limit(20).all()
    
    # Get scan statistics
    total_scans = SecurityScan.query.count()
    was_scans = SecurityScan.query.filter_by(scan_type='was').count()
    iac_scans = SecurityScan.query.filter_by(scan_type='iac').count()
    
    return render_template('admin.html', 
                         recent_scans=recent_scans,
                         total_scans=total_scans,
                         was_scans=was_scans,
                         iac_scans=iac_scans)

@app.route('/tools/was')
def was_scanner():
    return render_template('was_scanner.html')

@app.route('/tools/iac')
def iac_scanner():
    return render_template('iac_scanner.html')

@app.route('/api/scan/was', methods=['POST'])
@login_required
def start_was_scan():
    target_url = request.form.get('target_url')
    
    if not target_url:
        return jsonify({'error': 'Target URL is required'}), 400
    
    # Create scan record
    scan = SecurityScan()
    scan.scan_type = 'was'
    scan.target = target_url
    scan.user_id = current_user.id
    scan.status = 'running'
    db.session.add(scan)
    db.session.commit()
    
    try:
        # Initialize WAS scanner
        scanner = WASScanner()
        results = scanner.scan_url(target_url)
        
        # Update scan with results
        scan.results = json.dumps(results)
        scan.status = 'completed'
        scan.completed_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'scan_id': scan.id,
            'status': 'completed',
            'results': results
        })
        
    except Exception as e:
        scan.status = 'failed'
        scan.results = json.dumps({'error': str(e)})
        db.session.commit()
        
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan/iac', methods=['POST'])
@login_required
def start_iac_scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    if file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        return jsonify({'error': 'Invalid filename'}), 400
    
    # Create scan record
    scan = SecurityScan()
    scan.scan_type = 'iac'
    scan.target = filename
    scan.user_id = current_user.id
    scan.status = 'running'
    db.session.add(scan)
    db.session.commit()
    
    try:
        # Initialize IaC scanner
        scanner = IaCScanner()
        results = scanner.scan_file(filepath)
        
        # Update scan with results
        scan.results = json.dumps(results)
        scan.status = 'completed'
        scan.completed_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'scan_id': scan.id,
            'status': 'completed',
            'results': results
        })
        
    except Exception as e:
        scan.status = 'failed'
        scan.results = json.dumps({'error': str(e)})
        db.session.commit()
        
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan/<int:scan_id>/report/<format>')
@login_required
def download_report(scan_id, format):
    scan = SecurityScan.query.get_or_404(scan_id)
    
    if scan.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    if format == 'json':
        # Return JSON report
        return jsonify(json.loads(scan.results))
    
    elif format == 'pdf':
        # Generate PDF report
        generator = PDFReportGenerator()
        pdf_path = generator.generate_report(scan)
        
        return send_file(pdf_path, as_attachment=True, 
                        download_name=f'scan_report_{scan.id}.pdf')
    
    else:
        return jsonify({'error': 'Invalid format'}), 400

# API endpoint to get scan status
@app.route('/api/scan/<int:scan_id>/status')
@login_required
def get_scan_status(scan_id):
    scan = SecurityScan.query.get_or_404(scan_id)
    
    if scan.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    response = {
        'scan_id': scan.id,
        'status': scan.status,
        'created_at': scan.created_at.isoformat(),
        'target': scan.target,
        'scan_type': scan.scan_type
    }
    
    if scan.completed_at:
        response['completed_at'] = scan.completed_at.isoformat()
    
    if scan.results:
        response['results'] = json.loads(scan.results)
    
    return jsonify(response)

# Initialize blog posts if none exist
def init_blog_posts():
    if BlogPost.query.count() == 0:
        sample_posts = [
            {
                'title': 'The Evolution of Cybersecurity in 2025: AI-Powered Threat Detection',
                'excerpt': 'Exploring how artificial intelligence is revolutionizing threat detection and response in modern cybersecurity frameworks.',
                'content': '''The cybersecurity landscape continues to evolve at an unprecedented pace in 2025. With the integration of artificial intelligence and machine learning technologies, organizations are now capable of detecting and responding to threats in real-time with greater accuracy than ever before.

Key developments include:
- Advanced behavioral analytics for anomaly detection
- Automated incident response systems
- Predictive threat intelligence
- Zero-trust architecture implementation

As cyber threats become more sophisticated, the need for intelligent security solutions has never been more critical. Organizations that adopt AI-powered security tools are seeing significant improvements in their overall security posture.''',
                'category': 'AI & ML'
            },
            {
                'title': 'Infrastructure as Code Security: Best Practices for 2025',
                'excerpt': 'A comprehensive guide to securing your IaC deployments and preventing configuration drift in cloud environments.',
                'content': '''Infrastructure as Code (IaC) has become the backbone of modern cloud deployments. However, with this shift comes new security challenges that organizations must address proactively.

Essential IaC security practices include:
- Policy-as-code implementation
- Continuous compliance monitoring
- Automated security scanning in CI/CD pipelines
- Configuration drift detection
- Secure secrets management

By implementing these practices, organizations can ensure their infrastructure remains secure and compliant throughout the deployment lifecycle.''',
                'category': 'Infrastructure'
            },
            {
                'title': 'Web Application Security: Emerging Threats and Countermeasures',
                'excerpt': 'Understanding the latest web application vulnerabilities and how to protect against them using modern security tools.',
                'content': '''Web applications continue to be prime targets for cybercriminals. As development practices evolve, so do the attack vectors and vulnerabilities that security teams must defend against.

Current threat landscape includes:
- API security vulnerabilities
- Supply chain attacks
- Client-side security issues
- Authentication bypass techniques
- Advanced persistent threats

Organizations must adopt a multi-layered approach to web application security, combining automated scanning tools with manual security testing and continuous monitoring.''',
                'category': 'Web Security'
            },
            {
                'title': 'Compliance Automation: Streamlining SOX, HIPAA, and PCI-DSS Requirements',
                'excerpt': 'How automated compliance tools are helping organizations maintain continuous compliance with critical regulatory frameworks.',
                'content': '''Regulatory compliance remains a significant challenge for organizations across all industries. Traditional manual compliance processes are time-consuming, error-prone, and often fail to provide real-time visibility into compliance status.

Automation benefits include:
- Continuous compliance monitoring
- Automated evidence collection
- Real-time reporting and dashboards
- Reduced compliance costs
- Improved audit readiness

Modern compliance platforms leverage automation to transform how organizations approach regulatory requirements, making compliance a continuous process rather than a periodic burden.''',
                'category': 'Compliance'
            },
            {
                'title': 'The Future of SaaS Security: SSPM and Beyond',
                'excerpt': 'Exploring the growing importance of SaaS Security Posture Management in protecting cloud-based business applications.',
                'content': '''As organizations increasingly rely on Software-as-a-Service applications, the need for comprehensive SaaS security management has become critical. SaaS Security Posture Management (SSPM) represents the next evolution in cloud security.

Key SSPM capabilities include:
- Continuous SaaS application discovery
- Configuration assessment and monitoring
- Identity and access management oversight
- Data loss prevention integration
- Compliance posture management

Organizations implementing SSPM solutions are better positioned to maintain visibility and control over their expanding SaaS ecosystems while ensuring security and compliance requirements are met.''',
                'category': 'SaaS Security'
            }
        ]
        
        for post_data in sample_posts:
            post = BlogPost(**post_data)
            db.session.add(post)
        
        db.session.commit()
