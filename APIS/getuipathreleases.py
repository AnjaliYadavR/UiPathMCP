import requests
import os
import json

def getRelease(Config:dict,bearerKey:str,processName:str,organization_unit:str):
    try:
        folderUrl=Config.get("base_url")+Config.get("Releaseurl").replace('$processName',processName.lower())
        if not folderUrl:
            print("Error: 'base_url' is missing in the configuration.")
            return None
        header={
            "accept": "application/json",
            "X-UIPATH-OrganizationUnitId":f"{organization_unit}",
            "authorization": f"Bearer {bearerKey}"
        }
        response=requests.get(folderUrl,headers=header)
        if response.status_code==200:
            release_json=json.loads(response.text)
            print(f"Successfully retrieved {release_json.get('@odata.count', 0)} folders.")
            if release_json.get('@odata.count', 0)>0:
                release_data=json.dumps(release_json.get('value'))
                return {"ReleaseId":json.loads(release_data)[0].get('Key'),
                        "organization_unit":f"{organization_unit}"}
            return None
    except requests.exceptions.HTTPError as err:
        print(f"❌ Failed to Releases folders (HTTP Error: {err.response.status_code}).")
        # Attempt to print the detailed UiPath error message
        try:
            error_details = err.response.json()
            print(f"Error Message: {error_details.get('message', 'No specific message.')}")
        except json.JSONDecodeError:
            print(f"Raw Error Response: {err.response.text}")
            raise
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ An error occurred during the API call: {e}")
        raise
    

if __name__ == "__main__":
    getRelease(Config={
  "auth_url": "https://cloud.uipath.com/identity_/connect/token",
   "scope": "Orchestrator.Jobs.ReadWrite",
   "base_url": "https://cloud.uipath.com/anjalqeebhkv/DefaultTenant/orchestrator_/",
   "Folderurl": "odata/Folders",
   "Releaseurl":"odata/Releases?$filter=tolower(ProcessKey) eq '$processName'",
   "Processurl":"odata/Processes",
   "triggerJob":"odata/Jobs/UiPath.Server.Configuration.OData.StartJob",
   "tenant_name":"DefaultTenant",
   "organization_unit_id":""
},
               bearerKey='eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2QTY0RjI2NTA3MzY4MkQ4NTFGMDFBRUFEMTQxNjgyNUFEOTNDNTciLCJ4NXQiOiJocVpQSmxCemFDMkZId0d1clJRV2dsclpQRmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2Nsb3VkLnVpcGF0aC5jb20vaWRlbnRpdHlfIiwibmJmIjoxNzYxODE5OTI4LCJpYXQiOjE3NjE4MjAyMjgsImV4cCI6MTc2MTgyMzgyOCwiYXVkIjoiVWlQYXRoLk9yY2hlc3RyYXRvciIsInNjb3BlIjpbIk9SLkFkbWluaXN0cmF0aW9uIiwiT1IuQWRtaW5pc3RyYXRpb24uUmVhZCIsIk9SLkFkbWluaXN0cmF0aW9uLldyaXRlIiwiT1IuQW5hbHl0aWNzIiwiT1IuQW5hbHl0aWNzLlJlYWQiLCJPUi5BbmFseXRpY3MuV3JpdGUiLCJPUi5Bc3NldHMiLCJPUi5Bc3NldHMuUmVhZCIsIk9SLkFzc2V0cy5Xcml0ZSIsIk9SLkF1ZGl0IiwiT1IuQXVkaXQuUmVhZCIsIk9SLkF1ZGl0LldyaXRlIiwiT1IuQXV0b21hdGlvblNvbHV0aW9ucy5BY2Nlc3MiLCJPUi5CYWNrZ3JvdW5kVGFza3MiLCJPUi5CYWNrZ3JvdW5kVGFza3MuUmVhZCIsIk9SLkJhY2tncm91bmRUYXNrcy5Xcml0ZSIsIk9SLkV4ZWN1dGlvbiIsIk9SLkV4ZWN1dGlvbi5SZWFkIiwiT1IuRXhlY3V0aW9uLldyaXRlIiwiT1IuRm9sZGVycyIsIk9SLkZvbGRlcnMuUmVhZCIsIk9SLkZvbGRlcnMuV3JpdGUiLCJPUi5IeXBlcnZpc29yIiwiT1IuSHlwZXJ2aXNvci5SZWFkIiwiT1IuSHlwZXJ2aXNvci5Xcml0ZSIsIk9SLkpvYnMiLCJPUi5Kb2JzLlJlYWQiLCJPUi5Kb2JzLldyaXRlIiwiT1IuTGljZW5zZSIsIk9SLkxpY2Vuc2UuUmVhZCIsIk9SLkxpY2Vuc2UuV3JpdGUiLCJPUi5NYWNoaW5lcyIsIk9SLk1hY2hpbmVzLlJlYWQiLCJPUi5NYWNoaW5lcy5Xcml0ZSIsIk9SLk1MIiwiT1IuTUwuUmVhZCIsIk9SLk1MLldyaXRlIiwiT1IuTW9uaXRvcmluZyIsIk9SLk1vbml0b3JpbmcuUmVhZCIsIk9SLk1vbml0b3JpbmcuV3JpdGUiLCJPUi5RdWV1ZXMiLCJPUi5RdWV1ZXMuUmVhZCIsIk9SLlF1ZXVlcy5Xcml0ZSIsIk9SLlJvYm90cyIsIk9SLlJvYm90cy5SZWFkIiwiT1IuUm9ib3RzLldyaXRlIiwiT1IuU2V0dGluZ3MiLCJPUi5TZXR0aW5ncy5SZWFkIiwiT1IuU2V0dGluZ3MuV3JpdGUiLCJPUi5UYXNrcyIsIk9SLlRhc2tzLlJlYWQiLCJPUi5UYXNrcy5Xcml0ZSIsIk9SLlRlc3REYXRhUXVldWVzIiwiT1IuVGVzdERhdGFRdWV1ZXMuUmVhZCIsIk9SLlRlc3REYXRhUXVldWVzLldyaXRlIiwiT1IuVGVzdFNldEV4ZWN1dGlvbnMiLCJPUi5UZXN0U2V0RXhlY3V0aW9ucy5SZWFkIiwiT1IuVGVzdFNldEV4ZWN1dGlvbnMuV3JpdGUiLCJPUi5UZXN0U2V0cyIsIk9SLlRlc3RTZXRzLlJlYWQiLCJPUi5UZXN0U2V0cy5Xcml0ZSIsIk9SLlRlc3RTZXRTY2hlZHVsZXMiLCJPUi5UZXN0U2V0U2NoZWR1bGVzLlJlYWQiLCJPUi5UZXN0U2V0U2NoZWR1bGVzLldyaXRlIiwiT1IuVXNlcnMiLCJPUi5Vc2Vycy5SZWFkIiwiT1IuVXNlcnMuV3JpdGUiLCJPUi5XZWJob29rcyIsIk9SLldlYmhvb2tzLlJlYWQiLCJPUi5XZWJob29rcy5Xcml0ZSJdLCJzdWJfdHlwZSI6InNlcnZpY2UuZXh0ZXJuYWwiLCJwcnRfaWQiOiIzYTk5YmUwZi00NDdjLTQ5YTgtYmY1ZC02NWQ0NzcyNTQ2MTAiLCJjbGllbnRfaWQiOiI0NTBmMGFkNC1mYTE4LTRiMGItYTQ5OC05YWQ3ZWM0OTBmMDYiLCJqdGkiOiJEOUZGMTA4QjA0MzRCMDAwRjk4RDNENzRCOEE3NDg4RiJ9.h7ajyne4htdMp3dJ2la2DgBlNnE-cjd3HB-YXvBdxBN0zj8nXHAFvvq321rq6liOLManRgZDeO1AIvQqNyuKogpQl2x4Ih-e6UnxtYqI2YEUwlE8v1jbToqrSSbg0_76zZfjCFnWmqSlo-YwHv4etMwjGAyTy15rYGcQcNG5IqNvxxQu1gWbzzWuYpmCpyhLaMHt9NBkts-HQBrURYuFl6mcPY86tfjmFxo_SOHL53mO_MGgwhe1wMe5uxTPem46ZSTIG8l2ormWMM3h_XGOXInNSOffCfTcdTgV9DOXDIOajqJQGPpnEnl_7PNekuJ3bbOemZ8VyHB6GVN3cBT8hg',
               processName="GenerateExcelFile",
               organization_unit="5835818")