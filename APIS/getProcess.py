import requests
import os
import json
import asyncio
from .getToken import getToken

def getProcess(Config:dict,bearerKey:str=None):
    try:
        processUrl=Config.get("base_url")+Config.get("Processurl")
        if not processUrl:
            print("Error: 'Folder_URL' is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(processUrl,headers=header)
        if response.status_code==401:
            try:
                print("Failed  to authenticate the user while listing the process.")
                bearerKey = getToken(config=Config)
                print("token generated successfully")
                return getProcess(Config=Config, bearerKey=bearerKey)
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
        print("Request Exception.")
        raise
    except Exception as e:
        print("General exception.")
        raise
    return None

if __name__ == "__main__":
    asyncio.run(getProcess(Config={'auth_url': 'https://cloud.uipath.com/identity_/connect/token', 'scope': 'Orchestrator.Jobs.ReadWrite', 'base_url': 'https://cloud.uipath.com/anjalqeebhkv/DefaultTenant/orchestrator_/', 'Folderurl': 'odata/Folders',
'Releaseurl': "odata/Releases?$filter=tolower(ProcessKey) eq '$processName'", 'Processurl': 'odata/Processes', 'triggerJob': 'odata/Jobs/UiPath.Server.Configuration.OData.StartJobs', 'tenant_name': 'DefaultTenant', 'organization_unit_id': ''},bearerKey=None))



#bearerKey = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkRDNTI0OUNFQ0Q0RTQyMDJEOUFEQjc3MkM5N0M5OUY5MDk4N0NFMDAiLCJ4NXQiOiIzRkpKenMxT1FnTFpyYmR5eVh5Wi1RbUh6Z0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2Nsb3VkLnVpcGF0aC5jb20vaWRlbnRpdHlfIiwibmJmIjoxNzYzMzYxNTMyLCJpYXQiOjE3NjMzNjE4MzIsImV4cCI6MTc2MzM2NTQzMiwiYXVkIjoiVWlQYXRoLk9yY2hlc3RyYXRvciIsInNjb3BlIjpbIk9SLkFkbWluaXN0cmF0aW9uIiwiT1IuQWRtaW5pc3RyYXRpb24uUmVhZCIsIk9SLkFkbWluaXN0cmF0aW9uLldyaXRlIiwiT1IuQW5hbHl0aWNzIiwiT1IuQW5hbHl0aWNzLlJlYWQiLCJPUi5BbmFseXRpY3MuV3JpdGUiLCJPUi5Bc3NldHMiLCJPUi5Bc3NldHMuUmVhZCIsIk9SLkFzc2V0cy5Xcml0ZSIsIk9SLkF1ZGl0IiwiT1IuQXVkaXQuUmVhZCIsIk9SLkF1ZGl0LldyaXRlIiwiT1IuQXV0b21hdGlvblNvbHV0aW9ucy5BY2Nlc3MiLCJPUi5CYWNrZ3JvdW5kVGFza3MiLCJPUi5CYWNrZ3JvdW5kVGFza3MuUmVhZCIsIk9SLkJhY2tncm91bmRUYXNrcy5Xcml0ZSIsIk9SLkV4ZWN1dGlvbiIsIk9SLkV4ZWN1dGlvbi5SZWFkIiwiT1IuRXhlY3V0aW9uLldyaXRlIiwiT1IuRm9sZGVycyIsIk9SLkZvbGRlcnMuUmVhZCIsIk9SLkZvbGRlcnMuV3JpdGUiLCJPUi5IeXBlcnZpc29yIiwiT1IuSHlwZXJ2aXNvci5SZWFkIiwiT1IuSHlwZXJ2aXNvci5Xcml0ZSIsIk9SLkpvYnMiLCJPUi5Kb2JzLlJlYWQiLCJPUi5Kb2JzLldyaXRlIiwiT1IuTGljZW5zZSIsIk9SLkxpY2Vuc2UuUmVhZCIsIk9SLkxpY2Vuc2UuV3JpdGUiLCJPUi5NYWNoaW5lcyIsIk9SLk1hY2hpbmVzLlJlYWQiLCJPUi5NYWNoaW5lcy5Xcml0ZSIsIk9SLk1MIiwiT1IuTUwuUmVhZCIsIk9SLk1MLldyaXRlIiwiT1IuTW9uaXRvcmluZyIsIk9SLk1vbml0b3JpbmcuUmVhZCIsIk9SLk1vbml0b3JpbmcuV3JpdGUiLCJPUi5RdWV1ZXMiLCJPUi5RdWV1ZXMuUmVhZCIsIk9SLlF1ZXVlcy5Xcml0ZSIsIk9SLlJvYm90cyIsIk9SLlJvYm90cy5SZWFkIiwiT1IuUm9ib3RzLldyaXRlIiwiT1IuU2V0dGluZ3MiLCJPUi5TZXR0aW5ncy5SZWFkIiwiT1IuU2V0dGluZ3MuV3JpdGUiLCJPUi5UYXNrcyIsIk9SLlRhc2tzLlJlYWQiLCJPUi5UYXNrcy5Xcml0ZSIsIk9SLlRlc3REYXRhUXVldWVzIiwiT1IuVGVzdERhdGFRdWV1ZXMuUmVhZCIsIk9SLlRlc3REYXRhUXVldWVzLldyaXRlIiwiT1IuVGVzdFNldEV4ZWN1dGlvbnMiLCJPUi5UZXN0U2V0RXhlY3V0aW9ucy5SZWFkIiwiT1IuVGVzdFNldEV4ZWN1dGlvbnMuV3JpdGUiLCJPUi5UZXN0U2V0cyIsIk9SLlRlc3RTZXRzLlJlYWQiLCJPUi5UZXN0U2V0cy5Xcml0ZSIsIk9SLlRlc3RTZXRTY2hlZHVsZXMiLCJPUi5UZXN0U2V0U2NoZWR1bGVzLlJlYWQiLCJPUi5UZXN0U2V0U2NoZWR1bGVzLldyaXRlIiwiT1IuVXNlcnMiLCJPUi5Vc2Vycy5SZWFkIiwiT1IuVXNlcnMuV3JpdGUiLCJPUi5XZWJob29rcyIsIk9SLldlYmhvb2tzLlJlYWQiLCJPUi5XZWJob29rcy5Xcml0ZSJdLCJzdWJfdHlwZSI6InNlcnZpY2UuZXh0ZXJuYWwiLCJwcnRfaWQiOiIzYTk5YmUwZi00NDdjLTQ5YTgtYmY1ZC02NWQ0NzcyNTQ2MTAiLCJjbGllbnRfaWQiOiI0NTBmMGFkNC1mYTE4LTRiMGItYTQ5OC05YWQ3ZWM0OTBmMDYiLCJqdGkiOiJCNEIyRkMzRTg5RThGQkE4N0YzOUY1NzY1RDVERTkwMCJ9.usCVz1E8F9AfLwOs0VRk-C9RMlRCMxz43tpjBcW9Vl_KviS0lTBtZracCBFOwiSFbz7QCLP7c6r8IBl7jyCU0vq5fu0NX72pBoBRJvtfBL3f04FfSc7Ccppl5ztDjaCh7rM1ViIgJa_m7ZY6p10vo6LAtIpcJpsHCUoZO5ntL7E1kbAZn04lB9eZpcqvIOfBINrAw_2M43bjOMKk_yrjfMGtJiVVp6YekTI6xHHabrm5RgxMMO0YZmCl6AZKoNq1Blx6kCOcaGJzPH4PGSc3ChHndN6ZYXfxU9pojeZlBISe2-CKMfOfTsR-G1evSYzCP2DERz7tBl74Upm9g0fptg'))