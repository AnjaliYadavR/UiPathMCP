import requests
import os
import asyncio
from fastmcp import Context
import json
import logging

logger=logging.getLogger(__name__)

def getToken(config:dict,context:Context,credential:dict)->str:
    #client_ID=os.getenv("CLIENT_ID")
    #client_SecretKey=os.getenv("CLIENT_SECRET")
    client_ID=credential.get("CLIENT_ID")
    client_SecretKey=credential.get("CLIENT_SECRET")
    if not all([client_ID,client_SecretKey]):
        raise ValueError("CLIENT_ID and SECRET KEY is required.")
    authenticURL=config.get("auth_url")
    body={
        "grant_type": "client_credentials",
        "client_id":client_ID,
        "client_secret":client_SecretKey,
    }
    header={
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        logger.info("Authenticating and getting Bearer Token...")
        response=requests.post(authenticURL,data=body,headers=header)
        response.raise_for_status()
        responseJson=response.json()
        bearerKey=responseJson.get("access_token")
        if bearerKey:
            logger.info("Token retrieved successfully.")
            return bearerKey
        logger.error(f"Authentication failed. Response: {responseJson}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Authentication API call failed: {e}")
        raise 
    