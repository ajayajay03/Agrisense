from flask import Blueprint, request, jsonify, session, current_app
from app import mysql
from utils.security import login_required
from services.weather import get_weather, weather_label
from services.chatbot import ask_agriculture

api_bp=Blueprint('api',__name__)
@api_bp.get('/weather')
@login_required
def weather():
    try:
        lat=float(request.args.get('lat',12.9716)); lon=float(request.args.get('lon',77.5946)); data=get_weather(lat,lon); data['current']['label']=weather_label(data['current']['weather_code']); return jsonify(data)
    except Exception as exc: return jsonify({'error':f'Weather service unavailable: {exc}'}),503
@api_bp.post('/chat')
@login_required
def chat():
    question=(request.get_json(silent=True) or {}).get('question','').strip()
    if not question: return jsonify({'error':'Question is required.'}),400
    answer=ask_agriculture(question,current_app.config['GEMINI_API_KEY']); cur=mysql.connection.cursor(); cur.execute('INSERT INTO chat_history(user_id,question,answer) VALUES(%s,%s,%s)',(session['user_id'],question,answer)); mysql.connection.commit(); cur.close(); return jsonify({'answer':answer})
