from dapr.ext.grpc import App, BindingRequest
import json
import os

APP_PORT = os.getenv("APP_PORT", "50051")
TWITTER_BINDING_NAME = "twitter-binding"

app = App()

@app.binding(TWITTER_BINDING_NAME)
def binding(request: BindingRequest):    
    tweet = extract_tweets(json.loads(request.text()))
    print(f'Got a new tweet by {tweet["author"]}!', flush=True)

def extract_tweets(payload):
    content = payload['text']

    ext_text = payload.get('extended_tweet')
    if ext_text:
        content = ext_text['full_text']

    user_info = payload['user']

    return {
        'id': payload['id_str'],
        'author': user_info['screen_name'] or user_info['name'],
        'author_pic': user_info['profile_image_url_https'],
        'content': content,
        'lang': payload['lang'],
        'published': payload['created_at'],
    }


if __name__ == '__main__':
    print("Starting app on port {}".format(APP_PORT), flush=True)
    app.run(APP_PORT)