from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form.get('name','').strip(); email=request.form.get('email','').strip().lower(); password=request.form.get('password','')
        if len(name)<2 or '@' not in email or len(password)<8: flash('Use a valid email and a password of at least 8 characters.', 'danger'); return render_template('auth.html', mode='register')
        cur=mysql.connection.cursor(); cur.execute('SELECT id FROM users WHERE email=%s',(email,))
        if cur.fetchone(): cur.close(); flash('An account with that email already exists.', 'warning'); return render_template('auth.html', mode='register')
        cur.execute('INSERT INTO users(name,email,password_hash,location) VALUES(%s,%s,%s,%s)',(name,email,generate_password_hash(password),request.form.get('location','').strip())); mysql.connection.commit(); cur.close()
        flash('Account created. Please sign in.', 'success'); return redirect(url_for('auth.login'))
    return render_template('auth.html', mode='register')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cur=mysql.connection.cursor(); cur.execute('SELECT id,name,password_hash FROM users WHERE email=%s',(request.form.get('email','').strip().lower(),)); user=cur.fetchone(); cur.close()
        if user and check_password_hash(user[2], request.form.get('password','')):
            session.clear(); session['user_id']=user[0]; session['user_name']=user[1]; return redirect(url_for('main.dashboard'))
        flash('Incorrect email or password.', 'danger')
    return render_template('auth.html', mode='login')

@auth_bp.route('/forgot', methods=['GET','POST'])
def forgot():
    if request.method=='POST': flash('For security, contact your platform administrator to reset access.', 'info'); return redirect(url_for('auth.login'))
    return render_template('forgot.html')

@auth_bp.route('/logout')
def logout(): session.clear(); flash('You have been signed out.', 'info'); return redirect(url_for('main.index'))
