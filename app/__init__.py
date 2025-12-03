from flask import Flask


def create_app():
    app = Flask(__name__)

    # 注册蓝图
    from app.routes.api import api_bp
    from app.routes.web import web_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    return app