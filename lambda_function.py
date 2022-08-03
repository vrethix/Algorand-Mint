import json
import os

import boto3
from AlgorandMint.nft_service import NFTService
from algosdk.v2client import algod
from algosdk.v2client.algod import AlgodClient

REGION = os.environ["RegionName"]
PURESTAKE_SECRET = os.environ["Purestake"]
ALGOD_ADDRESS = os.environ["AlgodAddress"]


def lambda_handler(event, context):
    # TODO implement

    try:

        mint_status = tx_id = nft_id = None
        client = get_algod_client()

        event = json.loads(event)

        creator_address = event["CreatorAddress"]
        pk = event["PrivateKey"]
        url = event["Url"]
        asset_name = event["AssetName"]
        unit_name = event["UnitName"]
        metadata = event["MetaDataObj"]

        nft_service = NFTService(
            nft_creator_address=creator_address,
            nft_creator_pk=pk,
            client=client,
            nft_url=url,
            asset_name=asset_name,
            unit_name=unit_name,
        )

        metadatahash = nft_service.get_metadata_hash(metadata)

        tx_id, nft_id = nft_service.create_nft(metadatahash)
        print(tx_id)

        if tx_id and nft_id:
            resp = {"MintStatus": True, "TxId": tx_id, "NftId": nft_id}
        else:
            raise TypeError(
                "nft_id or tx_id is 'None' value"
            )

        return {"statusCode": 200, "body": json.dumps(resp)}

    except Exception as e:
        print("> Exception", e)
        resp = {"MintStatus": mint_status, "TxId": tx_id, "NftId": nft_id}
        return {"statusCode": 202, "body": json.dumps(resp)}


def get_algod_client() -> AlgodClient:

    session = boto3.session.Session()
    secman = session.client(service_name="secretsmanager", region_name=REGION)

    sec_response = secman.get_secret_value(SecretId=PURESTAKE_SECRET)
    api_key = eval(sec_response["SecretString"])["APIKey"]

    headers = {"X-API-Key": api_key}
    return AlgodClient(api_key, ALGOD_ADDRESS, headers)