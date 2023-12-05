# app.py
from hashing import hash_password, verify_password
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import db, Admin, Organisation, Service
import uuid 
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4().hex)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/queue_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return Admin.query.get(user_id)
    except:
        return None
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        org_name = request.form.get('org_name')
        org_address = request.form.get('org_address')
        org_number = request.form.get('org_number')
        if password == confirm_password:
            existing_user = Admin.query.filter_by(username=username).first()
            existing_organisation = Organisation.query.filter_by(org_name=org_name).first()
            if existing_user and existing_organisation:
                flash('Username already exists. Please choose a different one.', 'danger')
                render_template('registration.html')
            else:
                
               # Create a new Organisation instance
                new_org = Organisation(org_name=org_name, org_address=org_address, org_contact=org_number)
                
                # Add and commit the new_org to the database
                db.session.add(new_org)
                db.session.commit()

                # Now, the new_org will have its org_id assigned
                new_admin = Admin(username=username, password=hash_password(password), org_id=new_org.org_id)
                
                # Add and commit the new_admin to the database
                db.session.add(new_admin)
                db.session.commit()

                login_user(new_admin)
                return redirect(url_for('dashboard'))
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        plain_password = request.form.get('password')
        user = Admin.query.filter_by(username=username).first()

        if user and verify_password(plain_password, user.password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Login unsuccessful!', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        service = request.form.get('service')
        description = request.form.get('description')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        new_service = Service(service_name=service,description = description, start_time=datetime.strptime(start_time, '%H:%M').time(),end_time=datetime.strptime(end_time, '%H:%M').time(), org_id=current_user.org_id)
        db.session.add(new_service)
        db.session.commit()
        flash('Service successfully created!', 'success')
    return render_template('settings.html', username=current_user.username)
@app.route('/dashboard')
@login_required
def dashboard():
    
    return render_template('dashboard.html', username=current_user.username)

# ... (Other routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
