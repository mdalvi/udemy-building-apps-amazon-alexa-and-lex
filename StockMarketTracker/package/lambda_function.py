#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import requests 
from datetime import datetime

def lambda_handler(event, context):
    
    try:
        if 'new' in event['session']:
            print("NEW SESSION")
        
        if event['request']['type'] == 'LaunchRequest':
            print('LAUNCH REQUEST')
            onLaunchRequest(event, context)
        elif event['request']['type'] == 'IntentRequest':
            print('INTENT REQUEST')
            onIntentRequest(event, context)
        elif event['request']['type'] == 'SessionEndedRequest':
            print('SESSION END REQUEST')
            onSessionEndRequest(event, context)
            
        raise Exception(f"INVALID REQUEST TYPE: {event['request']['type']}")
        
    except Exception as ex:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Exception: {repr(ex)}")
        }
    
def onLaunchRequest(event, context):
    print('In function onLaunchRequest')
    return generateResponse(buildSpeechletResponse("Welcome to Market Tracker. Ask me what the stock market is like today.", False))

def onIntentRequest(event, context):
    print("In function onIntentRequest")

    intent = event['request']['intent']

    if intent['name'] == 'GetIndex':
        print("Calling the GET INDEX intent")
        getIndex(intent, context)
        
    elif intent['name'] == 'AMAZON.HelpIntent':
        print("AMAZON.HelpIntent")
        onLaunchRequest(event, context)

    elif intent['name'] == 'AMAZON.StopIntent':
        print("AMAZON.StopIntent")
        onSessionEndRequest(event, context)
    else:
        raise Exception(f"Could not indentify indent: {intent['name']}")

def onSessionEndRequest():
    print("In function onSessionEndRequest");
    speechOutput = "Thank you for trying the Stock Market Tracker. Have a nice day!";
    return generateResponse(buildSpeechletResponse(speechOutput, True), {})

def getIndex(intent, context):
    
    ALPHAVANTAGE_API_KEY = os.environ['apikey']
    endpoint = f"https://www.alphavantage.co/query"

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'IBM',
        'outputsize': 1,
        'apikey': ALPHAVANTAGE_API_KEY
    }
    response = requests.get(url=endpoint, params=params)
    response = response.json()

    dt_now = datetime.strptime(response['Meta Data']['3. Last Refreshed'], '%Y-%m-%d %H:%M:%S')
    close_value = response['Time Series (Daily)'][dt_now.strftime('%Y-%m-%d')]['4. close']
  

    print(f"Current stock value is: {close_value}")
    speechOutput = f"IBM is {currentValue}. Thank you for using Market Tracker. Good bye."
    
    return generateResponse(buildSpeechletResponse(speechOutput, False), {})
   

def buildSpeechletResponse(outputText, shouldEndSession):
    return {
        'outputSpeech': {
            'type': "PlainText",
            'text': outputText
        },
        'card': {
            'type': "Simple",
            'title': "Stock Tracker",
            'content': outputText
        },
        'shouldEndSession': shouldEndSession
    }

def generateResponse(speechletResponse, sessionAttributes):
    return {
        'version': "1.0",
        'sessionAttributes': sessionAttributes,
        'response': speechletResponse
    }

