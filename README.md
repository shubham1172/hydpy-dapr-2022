# Demo

This respository contains the source code for my demo at HydPy.

Architecture:
Twitter ----> Invoke ----> Sentiment Analysis ----> Tweets queue ---> Tweets viewer

Components:
Twitter binding
Secret store for Twitter secrets
Pub/Sub
State Store

Concepts:
- Service invocation
- State/secret store
- Messaging pub/sub
- Resiliency
- Observability
- Swapping components

TODO: Add more details.

#hydpy_dapr debit 10
#hydpy_dapr credit 2000

Twitter provider --> Pubsub --> Tweet processor ---> Invokes Bank App ---> Stores records ---> UI

```bash
dapr run --app-id tweet-provider --app-port 50051 --app-protocol grpc --log-level info --components-path ./components/ python3 services/tweet-provider/app.py

dapr run --app-id tweet-processor --app-port 50052 --app-protocol grpc --log-level info --components-path ./components/ python3 services/tweet-processor/app.py

dapr run --app-id banker --app-port 50053 --app-protocol grpc --log-level info --components-path ./components/ python3 services/banker/app.py
 ```