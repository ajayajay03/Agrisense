

"""Smart Agriculture Platform application factory entry point."""
import os
from flask import Flask, g
import mysql.connector as mysql_connector
from flask_wtf.csrf import CSRFProtect
from config import Config

class Database:
    """Small Windows-friendly mysql-connector integration used by routes."""
    def init_app(self, app):
        app.teardown_appcontext(lambda error: self.close())
    @property
    def connection(self):
        if 'db' not in g:
            g.db = mysql_connector.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DB, port=Config.MYSQL_PORT)
        return g.db
    def close(self):
        db=g.pop('db', None)
        if db and db.is_connected(): db.close()
mysql = Database()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    mysql.init_app(app)
    csrf.init_app(app)
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.api import api_bp
    from routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='127.0.0.1', port=5000)
