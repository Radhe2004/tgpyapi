from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# rest of your code ...
