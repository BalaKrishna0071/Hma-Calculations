import os
import  requests
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
auth_token= os.getenv("AUTHTOKEN")

def fetching(start_date_timestamp:int,end_date_timestamp:int, sym:str):

    # Headers for Trading View API
    headers = {
        'accept': '*/*',
        'accept-language': 'en,en-US;q=0.9',
        'auth-token': auth_token,
        'origin': 'https://chart.tradeclue.com',
        'priority': 'u=1, i',
        'referer': 'https://chart.tradeclue.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    # Params for Trading View API
    params = {
        'symbol': sym ,
        'resolution': '1D',
        'from': start_date_timestamp,
        'to': end_date_timestamp,
        'countback': '80',
        'currencyCode': 'INR',
    }

    # Request Get
    response = requests.get('https://api.tradeclue.com/v1/tv/history', params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
       return {}

