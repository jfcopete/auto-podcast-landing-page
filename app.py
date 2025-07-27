import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Database and CSV file paths
DATABASE = '/data/counter.db'
CSV_FEEDBACK_FILE = '/data/feedback.csv'
CSV_EMAILS_FILE = '/data/emails.csv'
CSV_ROOT_FILE = './podcast_subscriptions.csv'  # CSV in root directory

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the counter table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            categories TEXT,
            podcast_request TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT
        )
    ''')
    
    # Create Kano survey table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kano_surveys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            ip_address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            -- Personalización
            personalizacion_funcional TEXT,
            personalizacion_disfuncional TEXT,
            
            -- Duración
            duracion_funcional TEXT,
            duracion_disfuncional TEXT,
            
            -- Voz
            voz_funcional TEXT,
            voz_disfuncional TEXT,
            
            -- Fuentes
            fuentes_funcional TEXT,
            fuentes_disfuncional TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_csv_files():
    """Initialize CSV files with headers if they don't exist"""
    # Initialize feedback CSV
    if not os.path.exists(CSV_FEEDBACK_FILE):
        with open(CSV_FEEDBACK_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'type', 'content', 'email', 'ip_address', 'timestamp'])
    
    # Initialize emails CSV
    if not os.path.exists(CSV_EMAILS_FILE):
        with open(CSV_EMAILS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'email', 'categories', 'podcast_request', 'ip_address', 'timestamp'])
    
    # Initialize Kano surveys CSV
    if not os.path.exists('/data/kano_surveys.csv'):
        with open('/data/kano_surveys.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'email', 'ip_address', 'timestamp',
                'personalizacion_funcional', 'personalizacion_disfuncional', 'duracion_funcional', 'duracion_disfuncional',
                'voz_funcional', 'voz_disfuncional', 'fuentes_funcional', 'fuentes_disfuncional'
            ])
    
    # Initialize root CSV file
    if not os.path.exists(CSV_ROOT_FILE):
        with open(CSV_ROOT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp', 'email', 'categories', 'podcast_request'])

def save_to_csv_email(submission_id, email, categories, podcast_request, ip_address, timestamp):
    """Save email submission to CSV files"""
    try:
        # Save to data directory CSV
        with open(CSV_EMAILS_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([submission_id, email, categories, podcast_request, ip_address, timestamp])
        
        # Save to root directory CSV
        with open(CSV_ROOT_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, email, categories, podcast_request])
        
        return True
    except Exception as e:
        print(f"Error saving email to CSV: {e}")
        return False

def save_to_csv_feedback(feedback_id, feedback_type, content, email, ip_address, timestamp):
    """Save feedback to CSV file"""
    try:
        with open(CSV_FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([feedback_id, feedback_type, content, email, ip_address, timestamp])
        return True
    except Exception as e:
        print(f"Error saving feedback to CSV: {e}")
        return False

def save_to_csv_kano(survey_id, email, ip_address, timestamp, survey_data):
    """Save Kano survey to CSV file"""
    try:
        with open('/data/kano_surveys.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                survey_id, email, ip_address, timestamp,
                survey_data.get('personalizacion_funcional', ''),
                survey_data.get('personalizacion_disfuncional', ''),
                survey_data.get('duracion_funcional', ''),
                survey_data.get('duracion_disfuncional', ''),
                survey_data.get('voz_funcional', ''),
                survey_data.get('voz_disfuncional', ''),
                survey_data.get('fuentes_funcional', ''),
                survey_data.get('fuentes_disfuncional', '')
            ])
        return True
    except Exception as e:
        print(f"Error saving Kano survey to CSV: {e}")
        return False

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/submit-email', methods=['POST'])
def submit_email():
    """Submit email subscription"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        categories = data.get('categories', [])
        podcast_request = data.get('podcast_request', '').strip()
        
        # Get client IP
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email es requerido'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert email submission
        cursor.execute('''
            INSERT INTO email_submissions (email, categories, podcast_request, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (email, ','.join(categories), podcast_request, ip_address))
        
        email_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Save to CSV
        save_to_csv_email(email_id, email, ','.join(categories), podcast_request, ip_address, timestamp)
        
        return jsonify({'success': True, 'message': '¡Gracias por suscribirte!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@app.route('/api/counter')
def get_counter():
    """Get subscription counter"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM email_submissions')
        result = cursor.fetchone()
        conn.close()
        
        count = result['count'] if result else 0
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'count': 0})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback"""
    try:
        data = request.get_json()
        feedback_type = data.get('type', 'feedback')
        content = data.get('content', '').strip()
        email = data.get('email', '').strip()
        
        # Get client IP
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if not content:
            return jsonify({'success': False, 'message': 'Contenido es requerido'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert feedback
        cursor.execute('''
            INSERT INTO feedback (type, content, email, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (feedback_type, content, email, ip_address))
        
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Save to CSV
        save_to_csv_feedback(feedback_id, feedback_type, content, email, ip_address, timestamp)
        
        return jsonify({'success': True, 'message': '¡Gracias por tu feedback!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@app.route('/api/kano-survey', methods=['POST'])
def submit_kano_survey():
    """Submit Kano survey"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        # Get client IP
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract survey responses
        survey_data = {}
        radio_groups = [
            'personalizacion_funcional', 'personalizacion_disfuncional',
            'duracion_funcional', 'duracion_disfuncional',
            'voz_funcional', 'voz_disfuncional',
            'fuentes_funcional', 'fuentes_disfuncional'
        ]
        
        for field in radio_groups:
            survey_data[field] = data.get(field, '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert Kano survey
        cursor.execute('''
            INSERT INTO kano_surveys (
                email, ip_address, personalizacion_funcional, personalizacion_disfuncional,
                duracion_funcional, duracion_disfuncional, voz_funcional, voz_disfuncional,
                fuentes_funcional, fuentes_disfuncional
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email, ip_address,
            survey_data['personalizacion_funcional'], survey_data['personalizacion_disfuncional'],
            survey_data['duracion_funcional'], survey_data['duracion_disfuncional'],
            survey_data['voz_funcional'], survey_data['voz_disfuncional'],
            survey_data['fuentes_funcional'], survey_data['fuentes_disfuncional']
        ))
        
        survey_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Save to CSV
        save_to_csv_kano(survey_id, email, ip_address, timestamp, survey_data)
        
        return jsonify({'success': True, 'message': '¡Gracias por completar la encuesta!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@app.route('/api/export-csv')
def export_csv():
    """Export all data to CSV files"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all emails
        cursor.execute('SELECT * FROM email_submissions')
        emails = cursor.fetchall()
        
        # Write emails to CSV
        with open(CSV_EMAILS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'email', 'categories', 'podcast_request', 'ip_address', 'timestamp'])
            for email in emails:
                writer.writerow([email['id'], email['email'], email['categories'], email['podcast_request'], email['ip_address'], email['timestamp']])
        
        # Write feedback to CSV
        cursor.execute('SELECT * FROM feedback')
        feedbacks = cursor.fetchall()
        
        with open(CSV_FEEDBACK_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'type', 'content', 'email', 'ip_address', 'timestamp'])
            for feedback in feedbacks:
                writer.writerow([feedback['id'], feedback['type'], feedback['content'], feedback['email'], feedback['ip_address'], feedback['timestamp']])
        
        # Write Kano surveys to CSV
        cursor.execute('SELECT * FROM kano_surveys')
        surveys = cursor.fetchall()
        
        with open('/data/kano_surveys.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'email', 'ip_address', 'timestamp',
                'personalizacion_funcional', 'personalizacion_disfuncional', 'duracion_funcional', 'duracion_disfuncional',
                'voz_funcional', 'voz_disfuncional', 'fuentes_funcional', 'fuentes_disfuncional'
            ])
            for survey in surveys:
                writer.writerow([
                    survey['id'], survey['email'], survey['ip_address'], survey['timestamp'],
                    survey['personalizacion_funcional'], survey['personalizacion_disfuncional'],
                    survey['duracion_funcional'], survey['duracion_disfuncional'],
                    survey['voz_funcional'], survey['voz_disfuncional'],
                    survey['fuentes_funcional'], survey['fuentes_disfuncional']
                ])
        
        conn.close()
        
        return jsonify({'success': True, 'message': 'CSV files exported successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error exporting CSV files'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('/data', exist_ok=True)
    
    # Initialize database and CSV files
    init_db()
    init_csv_files()
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=False) 