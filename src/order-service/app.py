import json
import os
import requests
from flask import Flask, request, jsonify
from dapr.clients import DaprClient

app = Flask(__name__)

# Dapr sidecar configuration
DAPR_STORE_NAME = "statestore"
DAPR_PUBSUB_NAME = "pubsub"
DAPR_PUBSUB_TOPIC = "order_created"
SERVICE_2_APP_ID = "user-service"  # Dapr app id for user-service
SERVICE_2_URL = f"http://localhost:3500/v1.0/invoke/{SERVICE_2_APP_ID}/method/users"

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'product' not in data:
        return jsonify({"error": "Missing user_id or product"}), 400
    
    order_id = data.get('order_id', 1)  # Simple ID generation for demo
    
    # 1. Store order in YugabyteDB via Dapr State Store
    order_data = {
        "order_id": order_id,
        "user_id": data['user_id'],
        "product": data['product'],
        "status": "created"
    }
    
    with DaprClient() as client:
        # Save state
        client.save_state(
            store_name=DAPR_STORE_NAME,
            key=f"order_{order_id}",
            value=json.dumps(order_data)
        )
        print(f"Order {order_id} saved to state store.")
        
        # 2. ATTEMPT DIRECT CALL TO USER-SERVICE (Will be blocked by OPA)
        try:
            user_info_response = requests.get(f"{SERVICE_2_URL}/{data['user_id']}", timeout=3)
            direct_call_success = user_info_response.status_code == 200
            user_info = user_info_response.json() if direct_call_success else {"error": "Call failed"}
        except requests.exceptions.RequestException as e:
            direct_call_success = False
            user_info = {"error": str(e)}
        
        # 3. PUBLISH EVENT TO KAFKA VIA DAPR PUB/SUB (This will always work)
        pubsub_data = {
            "order_id": order_id,
            "user_id": data['user_id'],
            "product": data['product'],
            "direct_call_success": direct_call_success,
            "direct_call_response": user_info
        }
        
        client.publish_event(
            pubsub_name=DAPR_PUBSUB_NAME,
            topic_name=DAPR_PUBSUB_TOPIC,
            data=json.dumps(pubsub_data),
            data_content_type='application/json'
        )
        print(f"Published event to {DAPR_PUBSUB_TOPIC} topic.")
    
    return jsonify({
        "order": order_data,
        "direct_call_attempted": True,
        "direct_call_success": direct_call_success,
        "direct_call_response": user_info
    }), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "order-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)