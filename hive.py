# Imports:

import requests

# Used to call most Hive APIs

# Inputs:
# The unique API Key for your text project


def get_hive_response(input_text,API_Key):
    headers = {'Authorization': f'Token {API_Key}'}
    # Must be a string. This is also where you would insert metadata if desired.
    data = {'text_data': input_text}
    # Submit request to the synchronous API endpoint.
    response = requests.post(
        'https://api.thehive.ai/api/v2/task/sync', headers=headers, data=data)
    response_dict = response.json()
    return response_dict