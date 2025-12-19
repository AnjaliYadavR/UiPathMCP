import requests
import os
import json
import asyncio
from .getToken import getToken
import logging

logger=logging.getLogger(__name__)

def getRelease(Config:dict,bearerKey:str,processName:str,organization_unit:str):
    try:
        folderUrl=Config.get("base_url")+Config.get("Releaseurl").replace('$processName',processName.lower())
        if not folderUrl:
            logger.info("Error: Release API URL is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "X-UIPATH-OrganizationUnitId":f"{organization_unit}",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(folderUrl,headers=header)
        if response.status_code==401:
            try:
                bearerKey = getToken(config=Config)
                logger.info("token generated successfully")
                getRelease(Config=Config, bearerKey=bearerKey)
            except Exception as e:
                raise SystemError("Failed to generate the Token.")
        elif response.status_code==200:
            release_json=json.loads(response.text)
            if release_json.get('@odata.count', 0)>0:
                release_data=json.dumps(release_json.get('value'))
                logger.info(f"Suucessfully found process info under folder {json.loads(release_data)[0].get('OrganizationUnitFullyQualifiedName')}")
                argument_value=json.loads(release_data)[0].get("InputArguments")
                list_argument={}
                if argument_value:
                    logger.info(f"Release argument found.")
                    for key,value in json.loads(json.loads(release_data)[0].get("InputArguments")).items():
                        list_argument[key]=value
                return {"ReleaseId":json.loads(release_data)[0].get('Key'),
                        "InputArguments":list_argument,
                        "organization_unit":f"{organization_unit}"
                        }
            return None
    except requests.exceptions.HTTPError as err:
        logger.error(f"❌ Failed to Releases folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            logger.error(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            logger.error(f"Raw Error Response: {err.response.text}")
            raise
        
    except requests.exceptions.RequestException as e:
        logger.error(f"⚠️ An error occurred during the API call: {e}")
        raise