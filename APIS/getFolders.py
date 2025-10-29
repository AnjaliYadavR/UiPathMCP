import requests
import os
import json

def getFolders(Config:dict,bearerKey:str,processName:str):
    try:
        folderUrl=Config.get("base_url")+Config.get("Folderurl").str.replace('$processName',processName)
        if not folderUrl:
            print("Error: 'base_url' is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(folderUrl,headers=header)
        if response:
            data=response.content
            print(f"Successfully retrieved {data.get('@odata.count', 0)} folders.")
            return data
    except requests.exceptions.HTTPError as err:
        print(f"❌ Failed to fetch folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            print(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            print(f"Raw Error Response: {err.response.text}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ An error occurred during the API call: {e}")
        return None