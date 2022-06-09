import uvicorn
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from stream_chat import StreamChat

from hive import get_hive_response
hive_api_key = os.environ.get('HIVE_API_KEY')
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
        is_moderated = get_hive_response(text,hive_api_key)
        if(is_moderated):
            print("flagged")
            chat.flag_message(data["message"]["id"], user_id="hive-bot")
    return JSONResponse({"received": data})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
