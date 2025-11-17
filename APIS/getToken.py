import requests
import os
import asyncio


def getToken(config:dict)->str:
    client_ID=os.getenv("CLIENT_ID")
    client_SecretKey=os.getenv("CLIENT_SECRET")
    if not all([client_ID,client_SecretKey]):
        raise ValueError("Error: CLIENT_ID, SECRET KEY is missing in the .env file.")
    
    authenticURL=config.get("auth_url")
    body={
        "grant_type": "client_credentials",
        "client_id":client_ID,
        "client_secret":client_SecretKey,
        #"scope":scope
    }
    header={
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        print("Step 1: Authenticating and getting Bearer Token...")
        response=requests.post(authenticURL,data=body,headers=header)
        response.raise_for_status()
        responseJson=response.json()
        bearerKey=responseJson.get("access_token")
        if bearerKey:
            print("Token retrieved successfully.")
            return bearerKey
        print(f"Authentication failed. Response: {responseJson}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Authentication API call failed: {e}")
        raise 
    