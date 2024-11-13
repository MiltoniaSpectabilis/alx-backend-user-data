#!/usr/bin/python3
""" Module for API """
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(401)
def unauthorized(error):
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '5000'))
    app.run(host=host, port=port)
