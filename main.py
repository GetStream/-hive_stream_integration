# Imports:
import os
import requests

# Used to call most Hive APIs
from hive_response import HiveResponse, hive_response_from_dict
from moderation import ModerationElement, moderation_to_dict

# Inputs:
# The unique API Key for your text project
API_Key = os.environ.get('HIVE_API_KEY')


def get_hive_response(input_text) -> ModerationElement:
    headers = {'Authorization': f'Token {API_Key}'}
    # Must be a string. This is also where you would insert metadata if desired.
    data = {'text_data': input_text}
    # Submit request to the synchronous API endpoint.
    response = requests.post(
        'https://api.thehive.ai/api/v2/task/sync', headers=headers, data=data)
    response_dict = response.json()
  
    result = hive_response_from_dict(response_dict)
    input = ""
    moderation_class = None
    score = None
    is_moderated = False
    moderated_word = None
    reason = None
    for status in result.status:
        input = status.response.input.text

        for output in status.response.output:

            for class_ in output.classes:

                if class_.score > 0:
                    moderation_class = class_.class_class
                    score = class_.score
        filters = status.response.text_filters
        is_moderated = len(filters) > 0
        for text_filter in status.response.text_filters:
            moderated_word = text_filter.value
            reason = text_filter.type

    moderation = ModerationElement(
        input, moderation_class, score, is_moderated, moderated_word, reason)
    return moderation


# moderation = get_hive_response("you are a nice guy")
# if(moderation.is_moderated):
    # stream_chat_client.flag_message(msg["id"], user_id=server_user["id"])


