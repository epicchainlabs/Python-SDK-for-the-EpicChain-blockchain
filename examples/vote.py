"""
This example shows how to vote for your favourite consensus node
"""
import asyncio
from epicchain.api.wrappers import ChainFacade, EpicChain
from epicchain.api.helpers.signing import sign_insecure_with_account
from epicchain.network.payloads.verification import Signer
from examples import shared


async def example_vote(epicchainxp: shared.EpicChainExpress):
    wallet = shared.user_wallet
    account = wallet.account_default

    # This is your interface for talking to the blockchain
    facade = ChainFacade(rpc_host=epicchainxp.rpc_host)
    facade.add_signer(
        sign_insecure_with_account(account, password="123"),
        Signer(account.script_hash),
    )

    # Dedicated EpicChain native contract wrapper
    epicchain = EpicChain()
    # get a list of candidates that can be voted on
    candidates = await facade.test_invoke(epicchain.candidates_registered())
    # the example chain only has 1 candidate, use that
    candidate_pk = candidates[0].public_key

    voter = account.address

    print("Casting vote and waiting for receipt...")
    receipt = await facade.invoke(epicchain.candidate_vote(voter, candidate_pk))
    print(f"Success? {receipt.result}")


if __name__ == "__main__":
    with shared.EpicChainExpress() as epicchainxp:
        asyncio.run(example_vote(epicchainxp))
