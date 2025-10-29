import requests
import json
import time
import logging # <-- NEW: Logging for requests

# 1. NEW: Enable HTTP debugging for the requests library
# This makes the client print the raw headers being sent and received.
logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True 

SERVER_URL = "http://127.0.0.1:8000/mcp"
TIMEOUT = 5

def send_rpc_request(method_name: str, params: dict):
    """Sends a JSON-RPC 2.0 request to the FastMCP HTTP server."""
    
    request_data = {
        "jsonrpc": "2.0",
        "method": method_name,
        "params": params,
        "id": 1
    }
    
    print("\n" + "="*50)
    print(f"CLIENT: Sending request to {SERVER_URL}")
    print(f"CLIENT: Method: {method_name}, Params: {params}")
    print("="*50)

    # --- FINAL FIX ATTEMPT FOR 406 ERROR ---
    # We must be extremely explicit about Content-Type and Accept.
    headers = {
        "Content-Type": "application/json-rpc", 
        "Accept": "application/json-rpc"        
    }
    # ----------------------------------------

    try:
        response = requests.post(
            SERVER_URL,
            data=json.dumps(request_data), 
            headers=headers,
            timeout=TIMEOUT
        )
        response.raise_for_status() 
        
        # The server should respond with a JSON object
        response_json = response.json()
        
        if "error" in response_json:
            print(f"\nSERVER ERROR RESPONSE:")
            print(json.dumps(response_json, indent=4))
        else:
            print(f"\nSERVER SUCCESS RESPONSE (Result for '{method_name}'):")
            print(json.dumps(response_json["result"], indent=4))
            
    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Could not connect to server or request failed.")
        print(f"Reason: {e}")
        print(f"Please ensure 'main.py' is running and outputting a Uvicorn address like http://127.0.0.1:8000")

# --- Test Execution ---

if __name__ == "__main__":
    # 1. Test the 'listProcesses' tool you defined
    print("--- TEST 1: Calling the listProcesses tool ---")
    send_rpc_request("listProcesses", {})

    time.sleep(1)
    
    # 2. Test a simple system status method (often exposed by the framework)
    print("\n--- TEST 2: Testing a simple system status method ---")
    send_rpc_request("system.status", {"detail": "basic"}) 
