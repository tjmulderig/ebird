import requests
from config import get_redis_connection
from redis.commands.json.path import Path

class operation():

    @staticmethod
    def getData(api_key, regionCode, back=14):
        """ GET request sent to ebird API 2.0 for notable observations in state.

        Args:
            api_key (str): API key for user of ebird API 2.0
            regionCode (str): ISO 3166 for US state, example: US-NJ
            back (int): Number of days of data you want back from current
                         date, 1-30 days.

        Return:
            respon_data: JSON object with data from API

        """

        full_url = 'https://api.ebird.org/v2/data/obs/' + regionCode + '/recent/notable'
        headers = {'x-ebirdapitoken' :'{key}'.format(key=api_key)}
        params = {'regionCode': regionCode, 'back': back}

        response = requests.get(url=full_url, headers=headers, params=params)

        response_data = response.json()
        
        if response.status_code >= 200 and response.status_code <= 299:  # HTTP OK
            return response_data
        raise Exception("HTTP Response was:", response)
    
    @staticmethod
    def storeData(key: str, data):
        """ Store data (JSON format) into a redis database.
        
        Args:
            key (str): key of the key-value pair for the redis database.
            data (JSON): data in JSON format to be stored into database.
        """

        r = get_redis_connection()
        r.flushall()
        r.json().set(key, Path.root_path(), data)
        return
    
    @staticmethod
    def retreiveData(key: str):
        """ Retrieves data stored in a redis database.
        
        Args:
            key (str): key of the key-value pair for the redis database.
            data (JSON): data in JSON format to be stored into database.

        """
        r = get_redis_connection()
        data = r.json().get(key)
        return data