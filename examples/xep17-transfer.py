"""
This files has 2 examples that show how to transfer XEP-17 tokens for a contract that
has an existing wrapper (like EpicChain) and how to transfer for any arbitrary contract that
implements the XEP-17 standard
"""
import asyncio
from epicchain.api.wrappers import ChainFacade, EpicChain, Xep17Contract
from epicchain.api.helpers.signing import sign_insecure_with_account
from epicchain.network.payloads.verification import Signer
from epicchain.core import types
from examples import shared


async def example_transfer_xpp(epicchainxp: shared.EpicChainExpress):
    # This example shows how to transfer EpicChain tokens, a contract that has a dedicated wrapper
    wallet = shared.user_wallet
    account = wallet.account_default

    # This is your interface for talking to the blockchain
    facade = ChainFacade(rpc_host=epicchainxp.rpc_host)
    facade.add_signer(
        sign_insecure_with_account(account, password="123"),
        Signer(account.script_hash),  # default scope is CALLED_BY_ENTRY
    )

    source = account.address
    destination = "XyPUJMm6PhmtvGM7D1NsYagEfyNbVT1NGB"
    # Dedicated EpicChain native contract wrapper
    epicchain = EpicChain()
    print("Calling transfer and waiting for receipt...")
    print(await facade.invoke(epicchain.transfer(source, destination, 10)))


async def example_transfer_other(epicchainxp: shared.EpicChainExpress):
    # This example shows how to transfer XEP-17 tokens for a contract that does not
    # have a dedicated wrapper like EpicChain and EpicPulse have.
    # Most of the setup is the same as the first example
    wallet = shared.user_wallet
    account = wallet.account_default

    # This is your interface for talking to the blockchain
    facade = ChainFacade(rpc_host=epicchainxp.rpc_host)
    facade.add_signer(
        sign_insecure_with_account(account, password="123"),
        Signer(account.script_hash),  # default scope is CALLED_BY_ENTRY
    )

    source = account.address
    destination = "XyPUJMm6PhmtvGM7D1NsYagEfyNbVT1NGB"

    # Use the generic Xep17 class to wrap the token and create a similar interface as before
    # The contract hash is that of our sample Xep17 token which is deployed in our epicchainxpress setup
    contract_hash = types.UInt160.from_string(
        "0x41ee5befd936c90f15893261abbd681f20ed0429"
    )
    token = Xep17Contract(contract_hash)
    # Now call it in the same fashion as before with the EpicChain
    print("Calling transfer and waiting for receipt...")
    print(await facade.invoke(token.transfer(source, destination, 10)))


if __name__ == "__main__":
    with shared.EpicChainExpress() as epicchainxp:
        asyncio.run(example_transfer_xpp(epicchainxp))
        asyncio.run(example_transfer_other(epicchainxp))
