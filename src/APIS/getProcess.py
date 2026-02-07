import requests
import os
import json
import asyncio
from .getToken import getToken
import logging

logger=logging.getLogger(__name__)

def getProcess(Config:dict,bearerKey:str=None):
    try:
        processUrl=Config.get("base_url")+Config.get("Processurl")
        if not processUrl:
            logger.info.info("Error: Process API path is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(processUrl,headers=header)
        if response.status_code==401:
            try:
                logger.warning("Failed  to authenticate the user while listing the process.")
                bearerKey = getToken(config=Config)
                logger.info("token generated successfully")
                return getProcess(Config=Config, bearerKey=bearerKey)
            except Exception as e:
                raise SystemError("Failed to generate the Token.")
        elif response.status_code==200:
            data=json.loads(response.text)
            logger.info(f"Successfully retrieved {data.get('@odata.count', 0)} folders.")
            try:
                processes = data.get('value', [])
            except Exception as e:
                raise
            extracted_details = []
            for process in processes:
                if process.get("PackageType")=='Process':
                    extracted_details.append(process.get("Id"))
            return extracted_details
    except requests.exceptions.HTTPError as err:
        logger.error(f"❌ Failed to fetch folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            logger.error(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            raise
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Exception - {str(e)}")
        raise
    except Exception as e:
        logger.error(f"General exception for get process - {str(e)}")
        raise
    return None