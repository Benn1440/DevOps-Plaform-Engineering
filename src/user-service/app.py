import json
from flask import Flask, request, jsonify
from dapr.clients import DaprClient

app = Flask(__name__)

# In-memory user data for demonstration
users = {
    "1": {"user_id": "1", "name": "Alice Johnson", "email": "alice@example.com"},
    "2": {"user_id": "2", "name": "Bob Smith", "email": "bob@example.com"},
    "3": {"user_id": "3", "name": "Charlie Brown", "email": "charlie@example.com"}
}

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/orders', methods=['POST'])
def handle_order_event():
    # This is the endpoint that Dapr will call when a message arrives on the Kafka topic
    event_data = request.get_json()
    if not event_data:
        return jsonify({"error": "No data received"}), 400
    
    print(f"Received order event: {json.dumps(event_data, indent=2)}")
    
    # Process the event (e.g., update user order count, send notification, etc.)
    # For this demo, we'll just log it
    order_id = event_data.get('order_id')
    user_id = event_data.get('user_id')
    direct_call_success = event_data.get('direct_call_success', False)
    
    print(f"Processing order {order_id} for user {user_id}. Direct call was successful: {direct_call_success}")
    
    return jsonify({"status": "order event processed"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "user-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)