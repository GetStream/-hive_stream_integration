import uvicorn
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from stream_chat import StreamChat
from decimal import *
from hive import get_hive_response
visual_threshold = Decimal(0.9)
text_ban_threshold = 3
text_flag_threshold = 1
banned_classes = ['general_nsfw','general_suggestive', 'gun_in_hand','gun_not_in_hand']

# from hive import get_hive_response
from visual_moderation import get_visual_hive_response
hive_api_key = os.environ.get('HIVE_API_KEY')
hive_visual_api_key = os.environ.get('HIVE_VISUAL_API_KEY')
your_api_key = os.environ.get('api_key')
your_api_secret = os.environ.get('api_secret')


chat = StreamChat(api_key=your_api_key, api_secret=your_api_secret)
chat.upsert_user({"id": "hive-bot", "role": "admin"})
app = Starlette(debug=True)

@app.route('/chatEvent', methods=['POST'])
async def chatEvent(request):
    data = await request.json()
    if data["type"] == "message.new":
        text = data["message"]["text"]
        attachments = data["message"]["attachments"]
        user = data["message"]["user"]
        banned = False
        flagged = False
        reason=""
        for attachment in attachments:
            print(attachment["type"])
            if attachment["type"] == "image":
                visual_hive_response = get_visual_hive_response(attachment["image_url"],hive_visual_api_key)
                for output in visual_hive_response["status"][0]["response"]["output"]:
                    for class_ in output["classes"]:
                        score = class_["score"]
                        decimal_score = Decimal(score)
                        
                        if Decimal(visual_threshold).compare(decimal_score) == -1:
                            print(class_["class"])
                            print(class_["score"])
                            if class_["class"] in banned_classes:
                                reason = class_["class"]
                                banned = True
        hive_response = get_hive_response(
            text, hive_api_key)
        filters = hive_response["status"][0]["response"]["text_filters"]
        for text_filter in filters:
            moderated_word = text_filter["value"]
            print("moderated word: "+moderated_word)
            print("filtered : "+text_filter["type"])
            flagged = len(filters) > 0
        for output in hive_response["status"][0]["response"]["output"]:            
                    for class_ in output["classes"]:
                        print(class_["class"])
                        print(class_["score"])
                        score = class_["score"]
                        if score >= text_flag_threshold:
                            print("FLAG")
                            flagged = True
                            if score >= text_ban_threshold:
                                banned = True
                                reason = class_["class"]
                                print("BAN")
        if flagged:
            chat.flag_message(data["message"]["id"], user_id="hive-bot")
        if banned:
            print(banned)
            chat.ban_user(user["id"], banned_by_id="hive-bot", timeout=24*60, reason=reason)
               
    return JSONResponse({"received": data})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
