import uvicorn
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from stream_chat import StreamChat

from event import event_from_dict
from hive import get_hive_response
API_Key = os.environ.get('HIVE_API_KEY')

your_api_key = os.environ.get('api_key')
your_api_secret = os.environ.get('api_secret')


chat = StreamChat(api_key=your_api_key, api_secret=your_api_secret)
app = Starlette(debug=True)


@app.route('/chatEvent', methods=['POST'])
async def chatEvent(request):
    data = await request.json()
    event = event_from_dict(data)
    if event.type == "message.new":
        text = event.message.text
        moderation = get_hive_response(text)
        if(moderation.is_moderated):
            print("flagged")
    return JSONResponse({"received": data})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
