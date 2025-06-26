# 🚀 Getting Started with Raptor SDK

**Raptor** is the official Python SDK for interacting with the [EpicChain](https://epic-chain.org) blockchain. It abstracts away the complexities of crafting raw transactions, building data structures, or speaking directly to the EpicChain Virtual Machine—while remaining flexible enough for power users to get full control when needed.

Whether you're querying balances or executing advanced smart contract logic, Raptor empowers you to do it all with clean, Pythonic code.

---

## 🧠 Why Use Raptor?

* ✔️ Simplifies smart contract interaction.
* ✔️ Fully async and optimized for modern Python.
* ✔️ Works across **Linux, macOS, and Windows**.
* ✔️ Easily extensible with support for custom contracts and advanced blockchain features.
* ✔️ Speaks directly to EpicChain via **JSON-RPC** nodes.

> 🔗 A list of public RPC servers is available on the [EpicChain RPC Docs](https://github.com/epicchainlabs).

---

## ✅ Requirements

Before getting started, ensure the following:

* **Python**: `3.10` (Raptor is optimized for 3.10+ async syntax)
* **Operating System**: Linux, macOS, or Windows
* **Internet Connection**: To access EpicChain nodes

---

## 📦 Installation

You can install Raptor from PyPI or from source.

### 📥 Install from PyPI

\=== "UNIX/macOS"

```bash
pip install epicchain-raptor
```

\=== "Windows"

```bash
python -m pip install epicchain-raptor
```

### 🛠️ Install from Source (for contributors or cutting-edge development)

\=== "UNIX/macOS"

```bash
git clone https://github.com/epicchainlabs/epicchain-raptor.git
cd epicchain-raptor
python -m venv venv
source venv/bin/activate
pip install -e .
```

\=== "Windows"

```bash
git clone https://github.com/epicchainlabs/epicchain-raptor.git
cd epicchain-raptor
python -m venv venv
venv\Scripts\activate
python -m pip install -e .
```

> 🧪 `-e .` installs the SDK in **editable mode**, perfect for development and debugging.

---

## ⚡ Quick Example: Check a Balance

Let’s run a simple script to fetch the **EpicChain (XPR)** token balance of an account.

```python
import asyncio
from epicchain.api.wrappers import ChainFacade, EpicChain

async def main():
    facade = ChainFacade.node_provider_mainnet()
    epicchain = EpicChain()
    balance = await facade.test_invoke(
        epicchain.balance_of("Xh5PTE1MZpLspvPiR5MgAdoSJEVX1mxwjU")
    )
    print(f"EpicChain Balance: {balance}")

if __name__ == "__main__":
    asyncio.run(main())
```

📝 **Explanation**:

* `ChainFacade.node_provider_mainnet()` sets up the connection to the MainNet RPC.
* `EpicChain()` loads the smart contract wrapper for the EpicChain token.
* `test_invoke()` performs a **free, read-only** blockchain query—no XPP required.
* The wallet address in the example is just a placeholder. Replace it with your own.

> 🔒 Don’t worry, this doesn’t expose private keys or cost xpp. You’re just reading data.

---

## 🎯 What’s Next?

Now that you've installed Raptor and tested your first query, you're ready to explore more:

* ✅ Learn how to [interact with smart contracts](#interacting-with-smart-contracts)
* 🔁 Try your first [token transfer](#modifying-chain-state)
* 🧪 Dive into [examples and utilities](https://github.com/epicchainlabs/Python-SDK-for-the-EpicChain-blockchain/tree/main/examples)
* 💼 Load wallets and sign transactions
* ⚙️ Build and deploy your own contracts

---

Start building the future.
Start with **EpicChain.**