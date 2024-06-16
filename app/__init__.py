from flask import Flask
from .routes import routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)

    @app.template_filter('wrap_text')
    def wrap_text_filter(text, word_limit=20):
        words = text.split()
        wrapped_text = '\n'.join([' '.join(words[i:i + word_limit]) for i in range(0, len(words), word_limit)])
        return wrapped_text
    
    app.config['DEBUG'] = True
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
