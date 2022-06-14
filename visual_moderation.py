# Imports:

import requests

# Used to call most Hive APIs
# from hive_response import hive_response_from_dict
# from moderation import ModerationElement

# Inputs:
# The unique API Key for your text project


def get_visual_hive_response(content_url,API_Key):
    headers = {'Authorization': f'Token {API_Key}'}
    # Must be a string. This is also where you would insert metadata if desired.
    data = {'url': content_url}
    # Submit request to the synchronous API endpoint.
    response = requests.post(
        'https://api.thehive.ai/api/v2/task/sync', headers=headers, data=data)
    response_dict = response.json()
    return response_dict
    # result = moderation_from_dict(response_dict)
    # return result