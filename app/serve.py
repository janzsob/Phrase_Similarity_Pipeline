from log_config import get_logger
from flask import Flask, jsonify

# create logger instance
logger = get_logger()


# initialize flask app
app = Flask(__name__)


# Define the route for serving data (GET request)
@app.route('/data', methods=['GET'])
def serve_data():
    try:
        # This should be the result
        data = {"Result": '...'}
        return jsonify(data)

    except Exception as e:
        return False