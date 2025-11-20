from fastmcp import FastMCP,Context
import requests
import sys
import json
from APIS.getToken import getToken
from APIS.getProcess import getProcess
from APIS.getuipathfolders import getFolders
from APIS.triggeruipathjob import triggerUiPathJob
from APIS.getuipathreleases import getRelease
import tempfile
import os
import asyncio
import logging

mcp=FastMCP("UiPathMCP")
current_directory = os.getcwd()
config={}
bearer_token=None
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UiPathMCP_Server")

logging.info(f"Current working directory using os: {current_directory}")
config_file_path = os.path.join(current_directory, "Config.json")
with open(config_file_path, 'r') as f:
    config=json.load(f)

@mcp.tool
async def loadConfig(context:Context):
    global config
    logging.info(f"client id - {config.get("CLIENT_ID")} secret key - {config.get("CLIENT_SECRET")}")
    if not (config.get("CLIENT_ID",None) and config.get("CLIENT_SECRET",None)):
        headers = context.request_context.request.headers
        logging.info(f"loading Config value from header data.{str(headers)}")
        uipath_config_str = headers.get("uipathmcp")
        logging.info(f"{uipath_config_str}")
        if not uipath_config_str:
            return {"error": "Configuration header 'uipathmcp' missing from client request."}
        try:
            uipath_config = json.loads(uipath_config_str)
            logging.info(f"Anjali 2 - {uipath_config}")
            api_key = uipath_config.get("env", {})
            logging.warning(f"Anjali- {api_key}")
            config["CLIENT_ID"]=api_key.get("CLIENT_ID")
            config["CLIENT_SECRET"]=api_key.get("CLIENT_SECRET")
        except json.JSONDecodeError:
            return {"error": "Error parsing JSON from header."}
        if not api_key:
            return {"error": "Client ID and Secret Key not found in the client's 'env' block."}

@mcp.tool
async def generate_Token(context:Context):
    global bearer_token,config
    try:
        await loadConfig(context=context)
    except Exception as e:
        return {"status": "error", "message": f"{str(e)}"}
    
    try:
        bearer_token = await asyncio.to_thread(getToken,context=context,config=config)
        logging.info("token generated successfully")
        return {"status": "success", "message": f"token generated suucessfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error while generating token: {str(e)}"}
    
@mcp.tool
async def listProcesses(context:Context):
    global bearer_token,config
    try:
        await loadConfig(context=context)
    except Exception as e:
        return {"status": "error", "message": f"{str(e)}"}
    # Make sure getProcess returns valid data.
    logging.info("!!Process job workflow started")
    if not bearer_token:
        logging.info("regenerating bearer key")
        try:
            bearer_token=await asyncio.to_thread(getToken,context=context,config=config)
        except Exception as e:
            return {"status": "error", "message": f"Error while regenrating token: {str(e)}"}
    try:
        json_output= await asyncio.to_thread(getProcess,Config=config,bearerKey=bearer_token)
        if json_output:
            return {
                "status": "success",
                "data": json_output
                }
        return {"status": "error", "message": f"Process not found"}
    except Exception as e:
        return {"status": "error", "message": f"Error listing process: {str(e)}"}
    
@mcp.tool
async def triggerJob(context:Context,process_name:str):
    global bearer_token,config
    try:
        await loadConfig(context=context)
    except Exception as e:
        return {"status": "error", "message": f"{str(e)}"}
    # Make sure getProcess returns valid data.
    logging.info("!!Triger job workflow started")
    if not bearer_token:
        logging.info("regenerating bearer key")
        try:
            bearer_token=await asyncio.to_thread(getToken,context=context,config=config)
        except Exception as e:
            return {"status": "error", "message": f"Error while regenrating token: {str(e)}"}
    try:
        json_output= await asyncio.to_thread(triggerUiPathJob,process_name=process_name,config=config,bearerKey=bearer_token)
        logging.info("Job trigger successfully.")
        if json_output:
            return {
                "status": "success",
                "data": json_output
                }
        return {"status": "error", "message": f"failed to trigger the job"}
    except Exception as e:
        return {"status": "error", "message": f"Error while triggering job: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)