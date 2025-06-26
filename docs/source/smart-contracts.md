# 🚀 Smart Contracts on EpicChain

Welcome to the powerful world of **smart contracts** on the **EpicChain** blockchain! This guide will walk you through everything from foundational concepts to actual token transfers—complete with code, examples, and expert tips.

Whether you're a seasoned blockchain developer or a curious newcomer, this document will guide you step-by-step on how to interact with smart contracts using the [EpicChain Python SDK](https://github.com/epicchainlabs/Python-SDK-for-the-EpicChain-blockchain).

---

## 📘 Overview

First, we’ll establish the **mental model** of interacting with blockchains and smart contracts. If you're already familiar with EpicChain or how blockchains typically work, feel free to jump to the [Interacting with Smart Contracts](#interacting-with-smart-contracts) section.

From there, we’ll:

* Explore what smart contracts actually are.
* Learn how to communicate with them using EpicChain Python SDK wrappers.
* See real-world examples including a complete **XEP-17 token transfer**.

By the end of this guide, you’ll be confident in performing both read and write operations with smart contracts, and ready to explore more [examples](https://github.com/epicchainlabs/Python-SDK-for-the-EpicChain-blockchain/tree/main/examples) from our GitHub repository.

---

## 💡 What Are Smart Contracts?

Smart contracts are **programs deployed on the blockchain**. They execute code and hold state, allowing you to automate logic like token transfers, governance, or data storage.

Some key points:

* They're **not hosted locally**, but run on the **EpicChain Virtual Machine (XVM)**.
* They offer a **public API**—you interact with them by invoking exposed functions.
* Smart contract code is **compiled** into a format the blockchain understands. Python can't talk to them directly, so a **translation layer** is required.

That’s where the **EpicChain Python SDK** comes in—it bridges Python and the EpicChain VM seamlessly.

---

## 🤝 Interacting with Smart Contracts

The EpicChain SDK provides **two layers** for interacting with smart contracts:

1. **Contract Wrappers**: Prebuilt interfaces that make calling contract methods feel like calling regular Python functions.
2. **ChainFacade**: A powerful network handler that sends transactions and invokes smart contract methods.

Here’s a basic example that queries the token symbol of the EpicChain token:

```python
facade = ChainFacade.node_provider_mainnet()
epicchain = epicchainToken()
await facade.test_invoke(epicchain.symbol())
```

### 🔍 Explanation

* `facade`: Configures a connection to the EpicChain MainNet.
* `epicchain.symbol()`: Constructs EpicChain VM instructions.
* `test_invoke()`: Executes the call as a read-only query, costing **zero XPP**.

> 🧠 **Remember:**
>
> * `test_invoke()` is for **read-only** operations.
> * `invoke()` is used to **change state**, and consumes **XPP** (the EpicChain native token).

> 💡 **Pro Tip:**
> Use `invoke_fast()` or `invoke_multi()` for advanced scenarios. Check the [API docs](https://github.com/epicchainlabs) for details.

---

## 🧰 Contract Wrappers

Wrappers live in `epicchain.api.wrappers` and simplify interaction with common smart contract types on the EpicChain network.

EpicChain includes several **native contracts**, such as:

* `EpicChain` (XPR)
* `EpicPulse` (XPP)
* `PolicyContract`
* `RoleContract`

For standardized tokens like XEP-17, you can use generic wrappers:

```python
from epicchain.core import types
from epicchain.api.wrappers import XEP17Contract

contract_hash = types.UInt160.from_string("0x56199aa066633745de4d603e6477881455c08243")
ttm = XEP17Contract(contract_hash)
```

You can now do:

```python
await ttm.transfer(...)
await ttm.balance_of(...)
```

> 🛠 **Advanced Tip:**
> For custom smart contracts, use `GenericContract` or build your own wrapper on top of it.

---

## 🧭 Wrapper Class Hierarchy

Visualizing the smart contract class structure:

![Wrapper Class Hierarchy](wrapper-hierarchy.png)

* 🟨 **Yellow**: Specialized wrappers like `EpicChain`, `EpicPulse`.
* ⚪ **White**: Internal building blocks—rarely used directly.

---

## 🔄 Modifying Chain State

Now let’s go deeper. Interacting with smart contracts to **change blockchain state** (like transferring tokens) involves building a transaction and signing it.

Below is a **real-world example** of transferring 10 `EpicChain (XPR)` tokens:

```python
import asyncio
from epicchain.api.wrappers import ChainFacade, EpicChain
from epicchain.api.helpers.signing import sign_insecure_with_account
from epicchain.network.payloads.verification import Signer
from epicchain.wallet.wallet import Wallet

async def main():
    epicchain = EpicChain()

    wallet = Wallet.from_file("./mywallet.json")
    account = wallet.account_default

    facade = ChainFacade.node_provider_mainnet()
    facade.add_signer(
        sign_insecure_with_account(account, password="123"),
        Signer(account.script_hash)
    )

    destination = "XsokdeQ3kXqsryRycSVd1cJ86tHJ8kn8uP"
    print(await facade.invoke(epicchain.transfer(account.address, destination, 10)))

if __name__ == "__main__":
    asyncio.run(main())
```

### 🔐 Wallet Setup

You must:

* Own a funded account with both XPR and XPP.
* Load it via `Wallet.from_file(...)`.

```python
wallet = Wallet.from_file("./mywallet.json")
account = wallet.account_default
```

> 💡 **Tip:** Use `facade.estimate_epicpulse()` to preview the xpp fee (in XPP) before sending the transaction.

### 🧱 Configuring the Facade

```python
facade = ChainFacade.node_provider_mainnet()
facade.add_signer(
    sign_insecure_with_account(account, password="123"),
    Signer(account.script_hash)
)
```

* Adds signing capability so the facade can approve and send state-changing transactions.
* The default signer scope is `CALLED_BY_ENTRY` for added security.

> ℹ️ **Note:**
>
> * `test_invoke()` adds a signer automatically with restricted scope.
> * You can add **multiple signers**, but only the first pays the fee.

---

### 📨 Sending the Transfer

```python
print(await facade.invoke(epicchain.transfer(account.address, destination, 10)))
```

This will:

1. Construct the VM instructions to transfer tokens.
2. Sign and broadcast the transaction.
3. Wait for confirmation and return a receipt.

Example receipt:

```python
InvokeReceipt(
    tx_hash="6197...862a",
    included_in_block=18419,
    confirmations=3,
    epicpulse_consumed=9977750,
    state=HALT,
    exception=None,
    notifications=[
        Notification(
            contract="d2a4cff319130161...",
            event_name="Transfer",
            state=[<from>, <to>, <amount>]
        )
    ],
    result=True
)
```

> 🔁 **Need Speed?**
> Use `invoke_fast()` if you want a transaction ID instantly without waiting for the receipt.

---

## ✅ What’s Next?

After mastering this:

* Try deploying your own contract.
* Explore interaction with **multi-signature wallets**, **NFTs**, or **governance contracts**.
* Follow [more examples](https://github.com/epicchainlabs/Python-SDK-for-the-EpicChain-blockchain/tree/main/examples) and build the future with EpicChain.

---

## 📎 TL;DR

| Task             | Method                 | Notes            |
| ---------------- | ---------------------- | ---------------- |
| Read data        | `test_invoke()`        | Free             |
| Write data       | `invoke()`             | Costs XPP        |
| Estimate fees    | `estimate_epicpulse()` | Optional helper  |
| Wait for receipt | `invoke()`             | Default behavior |
| Get tx hash only | `invoke_fast()`        | No receipt wait  |

---

Ready to build the next generation of decentralized applications?
Start coding with EpicChain today. 💥