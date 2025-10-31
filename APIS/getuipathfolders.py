import requests
import os
import json
from .getuipathreleases import getRelease

def getFolders(Config:dict,bearerKey:str,process_name:str):
    try:
        folderUrl=Config.get("base_url")+Config.get("Folderurl")
        if not folderUrl:
            print("Error: 'base_url' is missing in the configuration.")
            return ValueError("API url is missing in Config for folders.")
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(folderUrl,headers=header)
        if response:
            folder_json=dict()
            folder_json=json.loads(response.content)
            print(f"Successfully retrieved {folder_json.get('@odata.count', 0)} folders.")
            for folder in folder_json.get('value'):
                release_data=getRelease(Config=Config,bearerKey=bearerKey,processName=process_name,organization_unit=folder.get('Id'))
                if release_data is not None:
                    return release_data
            if release_data is None:
                return ValueError(f"Process {process_name} not found,can't trigger the job.Please check whether job name is correct ot not!!")
    except requests.exceptions.HTTPError as err:
        print(f"❌ Failed to fetch folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            print(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            print(f"Raw Error Response: {err.response.text}")
            raise
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ An Request error occurred during the API call: {e}")
        raise
    except Exception as e:
        print(f"⚠️ An error occurred during the API call: {e}")
        raise