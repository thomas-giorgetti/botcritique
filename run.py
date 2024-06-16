import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=os.getenv('FLASK_RUN_HOST', '127.0.0.1'), port=int(os.getenv('FLASK_RUN_PORT', 8000)), debug=True)
