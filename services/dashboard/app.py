from dapr.clients import DaprClient

with DaprClient() as d:
        resp = d.get_secret(store_name='twitter-secret-store', key='apiKey')
        print(resp.secret)