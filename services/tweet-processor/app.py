# Tweet-processor picks up a tweet from the message queue and processes it.
# It invokes the correct method from the banker service to update the account.

from cloudevents.sdk.event import v1
from dapr.clients.grpc._response import TopicEventResponse
from dapr.clients import DaprClient
from dapr.ext.grpc import App
import json
import os
import re

APP_PORT = os.getenv("APP_PORT", "50051")
BANKER_APP_ID = os.getenv("BANKER_APP_ID", "banker")
TWEETS_QUEUE_NAME = "tweets-queue"
TWEET_TOPIC = "tweets"
TWEET_STORE_NAME = "tweet-store"
COMMAND_REGEX = re.compile(r'(debit|credit) ([0-9]{1,3})$')

app = App()


@app.subscribe(pubsub_name=TWEETS_QUEUE_NAME, topic=TWEET_TOPIC)
def get_tweet(event: v1.Event) -> TopicEventResponse:
    tweet = json.loads(event.Data())
    print(f'Got a new tweet by {tweet["author"]}!', flush=True)

    save_tweet(tweet)
    process_command(tweet["content"])

    return TopicEventResponse('success')

def save_tweet(tweet):
    with DaprClient() as d:
        try:
            d.save_state(TWEET_STORE_NAME, tweet["id"], json.dumps(tweet))
            print(f'Saved tweet to store.', flush=True)
        except Exception as e:
            print(f'Failed to save tweet to store: {e}', flush=True)

def process_command(command):
    res = COMMAND_REGEX.search(command)
    if not res:
        print(f'Invalid command, skipping.', flush=True)
        return

    command_type = res.group(1)
    amount = int(res.group(2))

    with DaprClient() as d:
        raw = d.invoke_method(BANKER_APP_ID, command_type, json.dumps({"amount": amount}))
        print(
            f'Invoked banker service with {command_type} {amount}.', flush=True)

        result = json.loads(raw.data)
        if result['status'] == 'success':
            print(
                f'Successfully processed command {command_type}, balance is {result["balance"]}.', flush=True)
        else:
            print(
                f'Failed to process command {command_type}, error: {result["error"]}.', flush=True)


if __name__ == '__main__':
    print("Starting app on port {}".format(APP_PORT), flush=True)
    app.run(APP_PORT)
