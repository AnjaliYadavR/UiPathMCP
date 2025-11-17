import requests
import os
import json
import asyncio
from .getToken import getToken

async def getProcess(Config:dict,bearerKey:str):
    try:
        processUrl=Config.get("base_url")+Config.get("Processurl")
        if not processUrl:
            print("Error: 'Folder_URL' is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=await asyncio.to_thread(requests.get,processUrl,headers=header)
        if response.status_code==401:
            try:
                bearerKey = getToken(config=Config)
                print("token generated successfully")
                await getProcess(Config=Config, bearerKey=bearerKey)
            except Exception as e:
                raise SystemError("Failed to generate the Token.")
        elif response.status_code==200:
            data=json.loads(response.text)
            print(f"Successfully retrieved {data.get('@odata.count', 0)} folders.")
            try:
                processes = data.get('value', [])
            except Exception as e:
                raise
            extracted_details = []
            for process in processes:
                if process.get("PackageType")=='Process':
                    details = {
                        "Process": process.get("Id")
                    }
                    extracted_details.append(details)
            return extracted_details
    except requests.exceptions.HTTPError as err:
        print(f"❌ Failed to fetch folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            print(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            raise
        
    except requests.exceptions.RequestException as e:
        raise