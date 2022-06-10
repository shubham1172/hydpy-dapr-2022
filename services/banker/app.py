from dapr.clients import DaprClient
from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse
import json
import os

APP_PORT = os.getenv("APP_PORT", "50052")
BANK_STORE_NAME = "bank-store"

app = App()


@app.method(name='debit')
def debit(request: InvokeMethodRequest) -> InvokeMethodResponse:
    amount = request.text()
    print(f'Debiting {amount} from account.', flush=True)
    try:
        balance = transact(-int(amount))
        print(f'New balance is {balance}.', flush=True)
        return InvokeMethodResponse(json.dumps({"status": "success", "balance": balance}))
    except Exception as e:
        print(f'Failed to debit {amount}: {e}', flush=True)
        return InvokeMethodResponse(json.dumps({"status": "failure", "balance": balance, "error": str(e)}))

@app.method(name='credit')
def credit(request: InvokeMethodRequest) -> InvokeMethodResponse:
    amount = request.text()
    print(f'Crediting {amount} to account.', flush=True)
    try:
        balance = transact(int(amount))
        print(f'New balance is {balance}.', flush=True)
        return InvokeMethodResponse(json.dumps({"status": "success", "balance": balance}))
    except Exception as e:
        print(f'Failed to credit {amount}: {e}', flush=True)
        return InvokeMethodResponse(json.dumps({"status": "failure", "balance": balance, "error": str(e)}))

def transact(amount: int) -> int:
    with DaprClient() as d:
        state = d.get_state(BANK_STORE_NAME, 'balance')
        balance = int(state.text())
        new_balance = balance + amount
        if new_balance < 0:
            raise Exception('Insufficient funds.')

        try:
            d.set_state(BANK_STORE_NAME, 'balance', str(new_balance))
            return new_balance
        except Exception as e:
            print(f'Failed to update balance: {e}', flush=True)
            raise e


if __name__ == '__main__':
    print("Starting app on port {}".format(APP_PORT), flush=True)
    app.run(APP_PORT)
