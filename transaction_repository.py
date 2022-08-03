from typing import Any, Dict, List, Optional, Tuple, Union

from AlgorandMint.network_interaction import NetworkInteraction
from algosdk import account as algo_acc
from algosdk.future import transaction as algo_txn
from algosdk.future.transaction import SignedTransaction, Transaction
from algosdk.v2client import algod


class ASATransactionRepository:
    """
    Initializes transactions related to Algorand Standard Assets
    """

    @classmethod
    def create_asa(cls,
                   client: algod.AlgodClient,
                   creator_private_key: str,
                   unit_name: str,
                   asset_name: str,
                   total: int,
                   decimals: int,
                   metadata_hash : bytes,
                   note: Optional[bytes] = None,
                   manager_address: Optional[str] = None,
                   reserve_address: Optional[str] = None,
                   freeze_address: Optional[str] = None,
                   clawback_address: Optional[str] = None,
                   url: Optional[str] = None,
                   default_frozen: bool = False,
                   sign_transaction: bool = True) -> Union[Transaction, SignedTransaction]:
        """

        :param client:
        :param creator_private_key:
        :param unit_name:
        :param asset_name:
        :param total:
        :param decimals:
        :param note:
        :param manager_address:
        :param reserve_address:
        :param freeze_address:
        :param clawback_address:
        :param url:
        :param default_frozen:
        :param sign_transaction:
        :return:
        """

        suggested_params = NetworkInteraction.get_default_suggested_params(client=client)

        creator_address = algo_acc.address_from_private_key(private_key=creator_private_key)

        txn = algo_txn.AssetConfigTxn(sender=creator_address,
                                      sp=suggested_params,
                                      total=total,
                                      default_frozen=default_frozen,
                                      unit_name=unit_name,
                                      asset_name=asset_name,
                                      manager=manager_address,
                                      reserve=reserve_address,
                                      freeze=freeze_address,
                                      clawback=clawback_address,
                                      url=url,
                                      metadata_hash = metadata_hash,
                                      decimals=decimals,
                                      note=note)

        if sign_transaction:
            txn = txn.sign(private_key=creator_private_key)

        return txn

    @classmethod
    def create_non_fungible_asa(cls,
                                client: algod.AlgodClient,
                                creator_private_key: str,
                                unit_name: str,
                                asset_name: str,
                                metadata : bytes,
                                url: str,
                                note: Optional[bytes] = None,
                                manager_address: Optional[str] = None,
                                reserve_address: Optional[str] = None,
                                freeze_address: Optional[str] = None,
                                clawback_address: Optional[str] = None,
                                default_frozen: bool = False,
                                sign_transaction: bool = True) -> Union[Transaction, SignedTransaction]:
        """

        :param client:
        :param creator_private_key:
        :param unit_name:
        :param asset_name:
        :param note:
        :param manager_address:
        :param reserve_address:
        :param freeze_address:
        :param clawback_address:
        :param url:
        :param default_frozen:
        :param sign_transaction:
        :return:
        """

        return ASATransactionRepository.create_asa(client=client,
                                                   creator_private_key=creator_private_key,
                                                   unit_name=unit_name,
                                                   asset_name=asset_name,
                                                   total=1,
                                                   decimals=0,
                                                   note=note,
                                                   manager_address=manager_address,
                                                   reserve_address=reserve_address,
                                                   freeze_address=freeze_address,
                                                   clawback_address=clawback_address,
                                                   url=url,
                                                   metadata_hash = metadata,
                                                   default_frozen=default_frozen,
                                                   sign_transaction=sign_transaction)