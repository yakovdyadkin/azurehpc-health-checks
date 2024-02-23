import json
import urllib
import subprocess


def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    return result.stdout.strip()


def get_request(url, data=None, headers={}):
    req = urllib.request.Request(url, data = data, headers = headers)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Error! Failed to reach server')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('Error! The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        return None
    else:
       return response.read().decode('utf-8') 


def get_instance_metadata():
    IMDS_URL = "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
    headers = {'Metadata': 'true'}
    raw_data = get_request(IMDS_URL, headers = headers)
    data_dict = {}
    if raw_data:
        try:
            data_dict = json.loads(raw_data)
        except json.JSONDecodeError as e:
            print(f"Error! Failed failed to deserialize metadata:\n{e}")
    return data_dict
