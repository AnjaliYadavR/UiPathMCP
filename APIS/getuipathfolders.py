import requests
import os
import json
from .getuipathreleases import getRelease
import asyncio
from .getToken import getToken
import logging

logger=logging.getLogger(__name__)

def getFolders(Config:dict,bearerKey:str,process_name:str):
    try:
        folderUrl=Config.get("base_url")+Config.get("Folderurl")
        if not folderUrl:
            logger.error("Error: Folder API URL is missing in the configuration.")
            return ValueError("API url is missing in Config for folders.")
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(folderUrl,headers=header)
        if response:
            folder_json=dict()
            folder_json=json.loads(response.content)
            logger.info(f"Successfully retrieved total number of folder {folder_json.get('@odata.count', 0)} folders.")
            for folder in folder_json.get('value'):
                release_data=getRelease(Config=Config,bearerKey=bearerKey,processName=process_name,organization_unit=folder.get('Id'))
                if release_data is not None:
                    return release_data
            return ValueError(f"Process {process_name} not found,can't trigger the job.Please check whether job name is correct ot not!!")
    except requests.exceptions.HTTPError as err:
        logger.error(f"❌ Failed to fetch folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            logger.error(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            logger.error(f"Raw Error Response: {err.response.text}")
            raise
        
    except requests.exceptions.RequestException as e:
        logger.error(f"⚠️ An Request error occurred during the API call: {e}")
        raise
    except Exception as e:
        logger.error(f"⚠️ An error occurred during the API call: {e}")
        raise