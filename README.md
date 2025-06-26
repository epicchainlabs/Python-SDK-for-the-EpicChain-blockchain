# EpicChain Python SDK

## Overview

The **EpicChain Python SDK** is a powerful development framework designed to simplify interaction with the **EpicChain blockchain** using Python. This SDK gives developers full access to blockchain features such as smart contract deployment and execution, wallet and key management, blockchain data querying, and transaction handling — all in a highly modular and secure fashion.

Whether you're building a DApp backend, managing digital assets, or deploying smart contracts for finance, governance, identity, or gaming, this SDK delivers a flexible and developer-centric approach to EpicChain development.

---

## Core Features

### ✅ Smart Contract Deployment

Deploy XEF-compiled contracts with manifest files using a simple Python API. Supports contract metadata, parameter configuration, and permission control.

### ✅ Contract Invocation

Call smart contract functions and receive on-chain results using signed transactions or test invocations for non-persistent simulations.

### ✅ Contract Upgrade System

Replace an existing deployed contract with an upgraded logic version, preserving its state and address while enhancing behavior.

### ✅ Safe Destruction

Programmatically destroy a contract to remove it from the blockchain and free up network resources.

### ✅ Wallet & Account Integration

Generate new wallets, import existing keys, securely store credentials, and authorize transactions on behalf of multiple users or roles.

### ✅ Real-Time Blockchain Access

Query block details, transaction histories, state variables, and events emitted by smart contracts — in real-time.

---

## Getting Started

### Installation

Install the SDK via pip:

```bash
pip install epicchain-python-sdk
```

Or for local development:

```bash
git clone https://github.com/epicchainlabs/epicchain-python-sdk.git
cd epicchain-python-sdk
python setup.py install
```

---

## Smart Contract Lifecycle: Full Working Samples

### 🔹 Contract v1: Add +1 Function

This version implements a simple contract with one function: `add(x)`, which returns `x + 1`.

```python
import asyncio
from epicchain.api.wrappers import GenericContract, ChainFacade
from epicchain.api.helpers.signing import sign_insecure_with_account
from epicchain.api.helpers import unwrap
from epicchain.contracts import xef, manifest
from epicchain.network.payloads.verification import Signer

# Load contract files
xef_v1 = xef.XEF.from_file("contracts/contract_v1.xef")
manifest_v1 = manifest.ContractManifest.from_file("contracts/contract_v1.manifest.json")

async def deploy_contract_v1(facade, signer):
    print("Deploying Contract v1...")
    receipt = await facade.invoke(GenericContract.deploy(xef_v1, manifest_v1))
    contract_hash = receipt.result
    print(f"Contract deployed at: {contract_hash}")
    return GenericContract(contract_hash)
```

---

### 🔹 Call `add(1)` on Contract v1

```python
async def call_add(contract, facade, input_value):
    print(f"Calling `add({input_value})`...", end=" ")
    result = await facade.test_invoke(contract.call_function("add", [input_value]))
    print("Result:", unwrap.as_int(result))
```

---

### 🔹 Contract v2: Add +2 Function (Upgrade)

This version replaces the `add` function logic with `x + 2`.

```python
xef_v2 = xef.XEF.from_file("contracts/contract_v2.xef")
manifest_v2 = manifest.ContractManifest.from_file("contracts/contract_v2.manifest.json")

async def update_contract(contract, facade):
    print("Updating to Contract v2...", end=" ")
    await facade.invoke(contract.update(xef=xef_v2, manifest=manifest_v2))
    print("Done.")
```

---

### 🔹 Destroying the Contract

```python
async def destroy_contract(contract, facade):
    print("Destroying contract...", end=" ")
    await facade.invoke(contract.destroy())
    print("Contract destroyed.")
```

---

### 🔹 Full Lifecycle Runner

```python
async def main():
    from examples import shared
    wallet = shared.user_wallet
    account = wallet.account_default

    facade = ChainFacade(rpc_host=shared.EpicChainExpress().rpc_host)
    facade.add_signer(
        sign_insecure_with_account(account, password="123"),
        Signer(account.script_hash)
    )

    contract = await deploy_contract_v1(facade, account)
    await call_add(contract, facade, 1)  # Expect result: 2

    await update_contract(contract, facade)
    await call_add(contract, facade, 1)  # Expect result: 3

    await destroy_contract(contract, facade)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Multiple Contract Samples

### Sample A: Math Contract (add, subtract)

A smart contract that performs multiple arithmetic operations:

```python
# contract_math.xef with functions: add(a, b), subtract(a, b)

result = await facade.test_invoke(contract.call_function("add", [5, 2]))
print("5 + 2 =", unwrap.as_int(result))

result = await facade.test_invoke(contract.call_function("subtract", [10, 3]))
print("10 - 3 =", unwrap.as_int(result))
```

---

### Sample B: Storage Contract

A contract that stores and retrieves values using keys.

```python
# contract_store.xef with set_value(key, val) and get_value(key)

await facade.invoke(contract.call_function("set_value", ["username", "Xmoohad"]))
result = await facade.test_invoke(contract.call_function("get_value", ["username"]))
print("Stored username:", unwrap.as_str(result))
```

---

### Sample C: Token Contract

A standard token contract implementing balance tracking.

```python
# contract_token.xef with functions: balance_of(address), transfer(to, amount)

await facade.invoke(contract.call_function("transfer", [receiver_address, 100]))
balance = await facade.test_invoke(contract.call_function("balance_of", [receiver_address]))
print("New Balance:", unwrap.as_int(balance))
```

---

## Use Cases & Integrations

* **Decentralized Applications**: Create robust dApps powered by EpicChain contracts.
* **Fintech & Payments**: Handle token transfers, microtransactions, and DeFi logic.
* **Gaming & NFTs**: Issue and manage digital game assets.
* **Document Verification**: Hash, anchor, and verify real-world files or IDs on-chain.
* **Cross-Chain Interactions**: Extend EpicChain to operate with other ecosystems.

---

## Contribution

We invite developers, auditors, and engineers to contribute to the SDK:

* Improve support for async workflows.
* Add new wrappers and examples.
* Suggest enhancements or performance improvements.

Follow the guide in `CONTRIBUTING.md`.

---

## Support

For assistance, questions, or suggestions:

* 📧 Email: `support@epic-chain.org`
* 🛠 GitHub: [Submit issues](https://github.com/epicchainlabs/Python-SDK-for-the-EpicChain-blockchain/issues)
* 📚 Docs & API Reference: Coming soon at `https://epic-chain.org/docs,`

---

## License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for full terms.

