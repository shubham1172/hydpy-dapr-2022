import os
from dapr.ext.grpc import App, BindingRequest

TWITTER_BINDING_NAME = "twitter-binding"
APP_PORT = os.getenv("APP_PORT", "50051")

app = App()

@app.binding(TWITTER_BINDING_NAME)
def binding(request: BindingRequest):
    print("HERE", flush=True)
    print("binding request: {}".format(request.text), flush=True)
    print(request, flush=True)

if __name__ == '__main__':
    print("Starting app on port {}".format(APP_PORT), flush=True)
    app.run(APP_PORT)