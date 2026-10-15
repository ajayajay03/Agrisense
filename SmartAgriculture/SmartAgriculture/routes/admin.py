from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from werkzeug.security import check_password_hash
from app import mysql
from utils.security import admin_required
admin_bp=Blueprint('admin',__name__)
@admin_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        cur=mysql.connection.cursor(); cur.execute('SELECT id,name,password_hash FROM admins WHERE email=%s',(request.form.get('email','').lower(),)); a=cur.fetchone(); cur.close()
        if a and check_password_hash(a[2],request.form.get('password','')): session['admin_id']=a[0]; session['admin_name']=a[1]; return redirect(url_for('admin.dashboard'))
        flash('Invalid administrator credentials.','danger')
    return render_template('admin_login.html')
@admin_bp.route('/')
@admin_required
def dashboard():
    cur=mysql.connection.cursor(); stats={};
    for key,table in [('users','users'),('vendors','vendors'),('feedback','feedback'),('predictions','crop_predictions')]: cur.execute(f'SELECT COUNT(*) FROM {table}'); stats[key]=cur.fetchone()[0]
    cur.execute('SELECT f.rating,f.comments,f.created_at,u.name FROM feedback f LEFT JOIN users u ON u.id=f.user_id ORDER BY f.created_at DESC LIMIT 10'); feedback=cur.fetchall(); cur.close(); return render_template('admin.html',stats=stats,feedback=feedback)
@admin_bp.route('/logout')
def logout(): session.pop('admin_id',None); session.pop('admin_name',None); return redirect(url_for('main.index'))
