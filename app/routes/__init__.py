from .url_routes import url_bp

def register_routes(app):
    app.register_blueprint(url_bp)
