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

async def loadConfig(context:Context=None):
    global config
    try:
        logging.info(f"client id - {config.get('CLIENT_ID')} secret key - {config.get('CLIENT_SECRET')}")
        if (config.get("CLIENT_ID",None) and config.get("CLIENT_SECRET",None)):
            headers = context.request_context.request.headers
            logging.info(f"loading Config value from header data.{headers}")
            try:
                print(f"****************************************{type(headers)} ******** {headers.get('client_id')} ,{headers.get('client_secret')}")
                config["CLIENT_ID"]=headers.get("client_id")
                config["CLIENT_SECRET"]=headers.get("client_secret")
            except json.JSONDecodeError as e:
                return {"error": f"Error parsing JSON from header- {e}"}
            except Exception as e:
                return {"error": f"Error while loading header- {e}"}
        else:
            config["CLIENT_ID"]=os.getenv("CLIENT_ID")
            config["CLIENT_SECRET"]=os.getenv("CLIENT_SECRET")
    except Exception as e:
        return {"status": "error", "message": f"Excepton found while loading Config value {str(e)}"}


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
        logger.info("Returning the list of process")
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
    #asyncio.run(generate_Token(None))
    mcp.run(transport="http", host="0.0.0.0", port=8000)