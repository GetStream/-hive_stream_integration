import uvicorn
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from stream_chat import StreamChat
from decimal import *
from hive import get_hive_response
threshold = Decimal(0.9)

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
        print(user)
        banned = False
        reason=""
        for attachment in attachments:
            print(attachment["type"])
            if attachment["type"] == "image":
                dic = get_visual_hive_response(attachment["image_url"],hive_visual_api_key)
                for output in dic["status"][0]["response"]["output"]:
                    for class_ in output["classes"]:
                        score = class_["score"]
                        decimal_score = Decimal(score)
                        
                        if Decimal(threshold).compare(decimal_score) == -1:
                            print(class_["class"])
                            print(class_["score"])
                            if class_["class"] == "general_nsfw":
                                reason = "NSFW"
                                banned = True
                            if class_["class"] == "general_suggestive":
                                reason = "suggestive"
                                banned = True
        if banned:
            print(banned)
            chat.ban_user(user["id"], banned_by_id="hive-bot", timeout=24*60, reason=reason)
        text_moderation = get_hive_response(
            text, hive_api_key)
        if(text_moderation.is_moderated):
            print("flagged")
            chat.flag_message(data["message"]["id"], user_id="hive-bot")
    return JSONResponse({"received": data})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
