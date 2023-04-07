from app import create_app
from flask_cors import CORS

app = create_app()

CORS(app)

PORT = 5018

app.run("0.0.0.0", PORT, debug=True)