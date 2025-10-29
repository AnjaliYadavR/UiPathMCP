from fastmcp import FastMCP
import requests
import sys
from dotenv import load_dotenv
load_dotenv()
import json

from APIS.getToken import getToken
from APIS.getProcess import getProcess
from APIS.getReleases import getRelease
from APIS.getFolders import getFolders
import os

mcp=FastMCP("UiPathMCP")
current_directory = os.getcwd()
config={}
bearer_token=""

print(f"Current working directory using os: {current_directory}")
config_file_path = os.path.join(current_directory, "Config.json")
with open(config_file_path, 'r') as f:
    config=json.load(f)

# --- Ensure Authentication is Clean ---
# The logic here is critical. If getToken fails, it will print to stdout/stderr 
# and contaminate the FastMCP communication, causing the 'bytes' error.
# The sys.exit(1) is good, but the authentication MUST succeed cleanly.
def init_Token():
    try:
        bearer_token = getToken(config=config)
    except Exception as e:
        error_message = f"FATAL ERROR: Exception found while authenticating the user. Exception - {e}"
        print(error_message, file=sys.stderr)
        sys.exit(1)

init_Token()

@mcp.tool
def listProcesses():
    # Make sure getProcess returns valid data.
    print(config)
    print(bearer_token)
    try:
        json_output= getProcess(Config=config,bearerKey=bearer_token)
        if json_output:
            return {
                "status": "success",
                "data_type": "json_string",
                "data": json_output
                }
        return {"status": "error", "message": f"PRocess not found"}
    except Exception as e:
        return {"status": "error", "message": f"Error listing expenses: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # The mcp.run() line is the default STDIO transport, which is incorrect for your client.
