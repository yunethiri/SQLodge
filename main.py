from app_trytry import create_app
from flask_cors import CORS

app = create_app()

CORS(app)

PORT = 5012

app.run("0.0.0.0", PORT, debug=True)