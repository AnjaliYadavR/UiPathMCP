from fastmcp import FastMCP
import requests
import sys
from dotenv import load_dotenv
load_dotenv()
import json
from APIS.getToken import getToken
from APIS.getProcess import getProcess
from APIS.getuipathfolders import getFolders
from APIS.triggeruipathjob import triggerUiPathJob
from APIS.getuipathreleases import getRelease
import tempfile
import os
import asyncio

mcp=FastMCP("UiPathMCP")
current_directory = os.getcwd()
config={}
bearer_token=None

print(f"Current working directory using os: {current_directory}")
config_file_path = os.path.join(current_directory, "Config.json")
with open(config_file_path, 'r') as f:
    config=json.load(f)


@mcp.tool
async def generate_Token():
    global bearer_token
    try:
        bearer_token = await asyncio.to_thread(getToken,config=config)
        print("token generated successfully")
        return {"status": "success", "message": f"token generated suucessfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error while egenrating token: {str(e)}"}
    
#@mcp.tool
async def listProcesses():
    global bearer_token
    # Make sure getProcess returns valid data.
    print("!!Process job workflow started")
    if not bearer_token:
        print("regenerating bearer key")
        try:
            #bearer_token=await asyncio.to_thread(getToken,config=config)
            print("hello")
        except Exception as e:
            return {"status": "error", "message": f"Error while regenrating token: {str(e)}"}
    try:
        json_output= await asyncio.to_thread(getProcess,Config=config,bearerKey=bearer_token)
        if json_output:
            return {
                "status": "success",
                "data_type": "json_string",
                "data": json_output
                }
        return {"status": "error", "message": f"Process not found"}
    except Exception as e:
        return {"status": "error", "message": f"Error listing process: {str(e)}"}
    
@mcp.tool
async def triggerJob(process_name:str):
    global bearer_token
    # Make sure getProcess returns valid data.
    print("!!Triger job workflow started")
    if not bearer_token:
        print("regenerating bearer key")
        try:
            bearer_token=await asyncio.to_thread(getToken,config=config)
        except Exception as e:
            return {"status": "error", "message": f"Error while regenrating token: {str(e)}"}
    try:
        json_output= await asyncio.to_thread(triggerUiPathJob,process_name=process_name,config=config,bearerKey=bearer_token)
        if json_output:
            return {
                "status": "success",
                "data_type": "json_string",
                "data": json_output
                }
        return {"status": "error", "message": f"failed to trigger the job"}
    except Exception as e:
        return {"status": "error", "message": f"Error while triggering job: {str(e)}"}

if __name__ == "__main__":
    asyncio.run(listProcesses())
    #mcp.run(transport="http", host="0.0.0.0", port=8000)