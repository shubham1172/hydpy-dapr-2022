# Tweet-processor picks up a tweet from the message queue and processes it.
# It invokes the correct method from the banker service to update the account.

from cloudevents.sdk.event import v1
from dapr.ext.grpc import App
from dapr.clients.grpc._response import TopicEventResponse
from dapr.clients import DaprClient
import json

TWEETS_QUEUE_NAME="tweets-queue"
TWEET_TOPIC="tweets"

app = App()

@app.subscribe(pubsub_name=TWEETS_QUEUE_NAME, topic=TWEET_TOPIC)
def get_tweet(event: v1.Event) -> TopicEventResponse:
    data = json.loads(event.Data())
    print(f'Subscriber received: id={data["id"]}, message="{data["message"]}", '
          f'content_type="{event.content_type}"', flush=True)

    process_message(data["message"])
    
    return TopicEventResponse('success')

def process_message(message):
    if ('debit' in message):
        # invoke debit service
        with DaprClient() as d:
            resp = d.invoke_method("banker", "debit", message)
            print(f'Debit service response: {resp}', flush=True)
    elif ('credit' in message):
        # invoke credit service
        with DaprClient() as d:
            resp = d.invoke_method("banker", "credit", message)
            print(f'Credit service response: {resp}', flush=True)
