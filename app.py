from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(filename='server.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/data', methods=['GET'])
def get_data():
    logging.info("GET request received")
    return jsonify({"status": "success", "message": "Hello from RPi!"}), 200

@app.route('/data', methods=['POST'])
def post_data():
    content = request.json
    logging.info(f"POST request received: {content}")
    return jsonify({"received": content}), 201

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)