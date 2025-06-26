"""
This example shows how to send tokens to multiple accounts in one go.
It will mint the "COZ Token"
"""
import asyncio
from epicchain.api.wrappers import ChainFacade, EpicChain, Xep17Contract
from epicchain.api.helpers.signing import sign_insecure_with_account
from epicchain.network.payloads.verification import Signer
from examples import shared


async def example_airdrop(epicchainxp: shared.EpicChainExpress):
    # This example shows how to airdrop XEP-17 tokens
    wallet = shared.user_wallet
    account = wallet.account_default

    # This is your interface for talking to the blockchain
    facade = ChainFacade(rpc_host=epicchainxp.rpc_host)
    facade.add_signer(
        sign_insecure_with_account(account, password="123"),
        Signer(account.script_hash),  # default scope is CALLED_BY_ENTRY
    )

    # Use the generic Xep17 class to wrap the token
    token = Xep17Contract(shared.coz_token_hash)
    balance = await facade.test_invoke(token.balance_of(account.address))
    print(f"Current token balance: {balance}")

    # First we have to mint the tokens to our own wallet
    # We do this by sending EpicChain to the contract
    # We increase the retry delay to match our local chain block production time
    epicchain = EpicChain()
    print("Minting once...", end="")
    receipt = await facade.invoke(
        epicchain.transfer(
            source=account.address, destination=shared.coz_token_hash, amount=100
        )
    )
    print(receipt.result)
    print("Minting twice...", end="")
    receipt = await facade.invoke(
        epicchain.transfer(
            source=account.address, destination=shared.coz_token_hash, amount=100
        )
    )

    print(receipt.result)

    balance = await facade.test_invoke(token.balance_of(account.address))
    print(f"New token balance: {balance}")

    # Now let's airdrop the tokens
    destination_addresses = [
        "XtxcQeNhLuNDucqAVynTwYBh2QHdDUyPzN",
        "XciXUD25yEsuMcxpq1eGoEZyLbstM3N1KE",
        "XsokdeQ3kXqsryRycSVd1cJ86tHJ8kn8uP",
        "XxBHmJuzGu8vnUnbB7ZWXWrS37hypTPwtB",
        "XkqcLP2QnBsHZnVnFxZ97fbsiEDAcB3bkZ",
    ]
    print("Airdropping 10 tokens and waiting for receipt")
    print(
        await facade.invoke(
            token.transfer_multi(account.address, destination_addresses, 10),
        )
    )


if __name__ == "__main__":
    with shared.EpicChainExpress() as epicchainxp:
        asyncio.run(example_airdrop(epicchainxp))
