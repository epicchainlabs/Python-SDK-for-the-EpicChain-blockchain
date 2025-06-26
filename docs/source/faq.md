# ❓ Frequently Asked Questions (Smart Contract SDK)

This section addresses some of the most common questions regarding design decisions and usage patterns in the EpicChain Python SDK. Whether you're curious about missing wrappers or MyPy errors, this guide provides clear, developer-focused answers.

---

## 🏛 Why Aren’t Consensus Committee Functions Wrapped?

> **Short answer:** Because very few people can use them.

The **consensus committee** consists of privileged nodes or actors on the EpicChain network. Their smart contract functions are meant for internal governance and low-level protocol operations.

By omitting these from standard wrappers, we:

* Keep the SDK clean, focused, and user-friendly.
* Avoid confusion among everyday developers who don’t need or have access to these features.

> 🔧 **Need them anyway?**
> You can still use them via the flexible `call_function()` method:

```python
contract.call_function("committee_vote", [args])
```

---

## 🧱 Why Isn’t the Native `ContractManagement` Contract Wrapped?

The core actions of this contract—`deploy`, `update`, and `destroy`—are already integrated into the base `GenericContract` class.

This means:

* Any contract wrapper you use (including custom ones) inherits these methods automatically.
* You don’t need a separate wrapper just for contract deployment or modification.

> 🧠 **Tip:** Use `contract.deploy()`, `contract.update()`, or `contract.destroy()` directly on your smart contract wrapper object.

---

## 📒 Why Is the Native `Ledger` Contract Not Wrapped?

The native `Ledger` contract is **not user-friendly** or complete for external use. Its methods are primarily intended for smart contracts themselves—not for external SDK consumers.

For example:

* `Ledger.GetBlock` returns a **trimmed block** (without transactions).
* `EpicRpcClient.get_block()` returns the **full block**, including all transactions.

Because `EpicRpcClient` provides **more complete and consistent** access to blockchain data, there’s **no practical need** to wrap `Ledger` in the SDK.

> 🔍 **Bottom line:** Use `EpicRpcClient` for data retrieval from the chain. Leave `Ledger` to the contracts.

---

## 🔄 Why Does the `IJson` Interface Use Python Dictionaries?

While this may seem like an arbitrary choice, it’s rooted in **Python community standards**:

* Popular libraries like `requests`, `aiohttp`, `FastAPI`, `Django`, and `Flask` all standardize on using `dict` objects to handle JSON payloads.
* Dictionaries provide simplicity, flexibility, and seamless integration with most frameworks and serializers.

This makes the SDK easier to integrate into web servers, backend systems, and JSON-based APIs.

> 💬 **In short:** Using `dict` aligns with Python’s ecosystem and best practices.

---

## 🧪 How Do I Fix the MyPy Error: `"as_none" of "StackItem" does not return a value`?

This is a known limitation of **MyPy**, and not an actual code bug.

MyPy enforces that every function must **explicitly return a value**, even if it’s just `None`. However, many developers and other tools (like `pyright`) consider this unnecessary for simple functions like `as_none()`.

### 🔧 Solution:

Add the following configuration to disable the error:

#### Option 1: CLI

```bash
mypy --disable-error-code func-returns-value
```

#### Option 2: `pyproject.toml`

```toml
[tool.mypy]
disable_error_code = "func-returns-value"
```

> 🛠 This won’t impact runtime behavior and will keep your type checking smooth.