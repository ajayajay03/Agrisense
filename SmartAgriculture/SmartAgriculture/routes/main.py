import os, uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app import mysql
from utils.security import login_required
from ml_models.predictors import soil_recommendation, yield_prediction, disease_from_image

main_bp=Blueprint('main',__name__)
@main_bp.route('/')
def index(): return render_template('index.html')
@main_bp.route('/dashboard')
@login_required
def dashboard(): return render_template('dashboard.html')
@main_bp.route('/soil',methods=['GET','POST'])
@login_required
def soil():
    result=None
    if request.method=='POST':
        try: result=soil_recommendation(*[float(request.form[x]) for x in ('nitrogen','phosphorus','potassium','temperature','humidity','ph','rainfall')])
        except ValueError: flash('All soil inputs must be numeric.', 'danger')
    return render_template('soil.html',result=result)
@main_bp.route('/yield',methods=['GET','POST'])
@login_required
def yield_page():
    result=None
    if request.method=='POST':
        try:
            data=request.form; result=yield_prediction(data['crop'],float(data['area']),float(data['rainfall']),float(data['temperature']),data['soil_type'])
            cur=mysql.connection.cursor(); cur.execute('INSERT INTO crop_predictions(user_id,crop,area,rainfall,temperature,soil_type,predicted_yield) VALUES(%s,%s,%s,%s,%s,%s,%s)',(session['user_id'],data['crop'],data['area'],data['rainfall'],data['temperature'],data['soil_type'],result)); mysql.connection.commit(); cur.close()
        except (ValueError,KeyError): flash('Provide valid yield inputs.', 'danger')
    return render_template('yield.html',result=result)
@main_bp.route('/disease',methods=['GET','POST'])
@login_required
def disease():
    result=None
    if request.method=='POST':
        file=request.files.get('image')
        if not file or file.filename.rsplit('.',1)[-1].lower() not in current_app.config['ALLOWED_EXTENSIONS']: flash('Upload a PNG, JPG, or JPEG image.', 'danger')
        else:
            filename=f'{uuid.uuid4().hex}_{secure_filename(file.filename)}'; path=os.path.join(current_app.config['UPLOAD_FOLDER'],filename); file.save(path); result=disease_from_image(path)
            cur=mysql.connection.cursor(); cur.execute('INSERT INTO disease_history(user_id,image_path,disease_name,confidence,treatment) VALUES(%s,%s,%s,%s,%s)',(session['user_id'],filename,result['name'],result['confidence'],result['treatment'])); mysql.connection.commit(); cur.close()
    return render_template('disease.html',result=result)
@main_bp.route('/vendors')
@login_required
def vendors():
    cur=mysql.connection.cursor(); cur.execute('SELECT name,category,address,phone,latitude,longitude FROM vendors ORDER BY name'); rows=cur.fetchall(); cur.close(); return render_template('vendors.html',vendors=rows)
@main_bp.route('/feedback',methods=['GET','POST'])
@login_required
def feedback():
    if request.method=='POST':
        rating=int(request.form.get('rating',0)); comments=request.form.get('comments','').strip()
        if 1<=rating<=5 and comments: cur=mysql.connection.cursor(); cur.execute('INSERT INTO feedback(user_id,rating,comments) VALUES(%s,%s,%s)',(session['user_id'],rating,comments)); mysql.connection.commit(); cur.close(); flash('Thank you for your feedback!', 'success'); return redirect(url_for('main.feedback'))
        flash('Please provide a rating and comment.', 'danger')
    return render_template('feedback.html')
@main_bp.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST': flash('Thanks — your message has been received.', 'success'); return redirect(url_for('main.contact'))
    return render_template('contact.html')
@main_bp.route('/history')
@login_required
def history():
    cur=mysql.connection.cursor(); cur.execute('SELECT crop,predicted_yield,created_at FROM crop_predictions WHERE user_id=%s ORDER BY created_at DESC',(session['user_id'],)); predictions=cur.fetchall(); cur.execute('SELECT disease_name,confidence,created_at FROM disease_history WHERE user_id=%s ORDER BY created_at DESC',(session['user_id'],)); diseases=cur.fetchall(); cur.close(); return render_template('history.html',predictions=predictions,diseases=diseases)
