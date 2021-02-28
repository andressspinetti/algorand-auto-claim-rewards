import os

from algosdk import encoding
from algosdk import transaction
from algosdk import kmd
from algosdk.v2client import algod
from algosdk import account
from algosdk import mnemonic
import json

# Setup HTTP client w/guest key provided by PureStake
algod_purestake_address = "https://mainnet-algorand.api.purestake.io/ps2"
algod_purestake_token = os.environ['ALGOD_PURESTAKE_TOKEN']
purestake_token_header = {"X-API-Key": algod_purestake_token}

# Warning: Only use a seed with just a few algo, since it's going to be used as a way to generate a txn. Never use the seed where your hold your Algo.
mnemonic_phrase = os.environ['ALGO_FROM_SEED']
account_private_key = mnemonic.to_private_key(mnemonic_phrase)
account_public_key = mnemonic.to_public_key(mnemonic_phrase)

algodclient = algod.AlgodClient(algod_purestake_token, algod_purestake_address, headers=purestake_token_header)

# get suggested parameters from Algod

params = algodclient.suggested_params()
gen = params.gen
gh = params.gh
first_valid_round = params.first
last_valid_round = params.last
fee = params.min_fee
send_amount = 0

existing_account = account_public_key

# The address that needs to claim the stake rewards
send_to_address = os.environ['ALGO_TO_ADDRESS']

# Create and sign transaction
tx = transaction.PaymentTxn(
    existing_account,
    fee,
    first_valid_round,
    last_valid_round,
    gh,
    send_to_address,
    send_amount,
    flat_fee=True,
)
signed_tx = tx.sign(account_private_key)


# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


try:
    tx_confirm = algodclient.send_transaction(signed_tx)
    wait_for_confirmation(algodclient, txid=signed_tx.transaction.get_txid())
except Exception as e:
    print(e)
