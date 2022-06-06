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

TODO: Add more details.z


#hydpy debit 100
#hydpy credit 2000

Twitter provider --> Pubsub --> Tweet processor ---> Invokes Bank App ---> Stores records ---> UI
