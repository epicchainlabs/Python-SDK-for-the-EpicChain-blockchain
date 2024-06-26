## Why are consensus committee only functions not wrapped?
The group of users that can make use of this is _very_ limited. By ommitting these functions the API list stays short and
relevant to the biggest group of users. Those who do wish to use these functions can always use the generic 
`call_function()` method on the contract of choice to call them.

## Why is the native ContractManagement contract not wrapped?
The contract `deploy`, `update` and `destroy` functionality is already part of the `GenericContract` base class used in 
all contract wrappers.

## Why is the native Ledger contract not wrapped?
All information that can be obtained from the `Ledger` contract can also be obtained using the `EpicRpcClient`. In some 
cases the `Ledger` contract returns even incomplete data. For example `Ledger.GetBlock` returns a `TrimmedBlock` without
transactions as opposed to `EpicRpcClient.get_block()` which returns the complete block. The `Ledger` contract is really
intended to be consumed by smart contracts.

## Why does the IJson interface consume and produce dictionaries?
This was originally used in the full node version of Mamba. However, it seems like the standard in the Python community
 if judged by looking at popular packages/frameworks like `requests` and `aiohttp`. Also, frameworks like `FastAPI`, 
 `Django` and `Flask` all have ways of consuming a `dict` when returning a json response. It seems like the best choice 
 for these reasons. 

## How do I prevent 'error: "as_none" of "StackItem" does not return a value' when type checking with MyPy?
The `mypy` team made an unfortunate choice to include a restriction on something that is actually a code style choice.
They [refuse](https://github.com/python/mypy/issues/6549) to change the default behaviour despite the raised complaints 
and other type checkers like pyright not falling over this. The error can be disabled with 
`--disable-error-code func-returns-value` or by adding it to your configuration file i.e. for `pyproject.toml` use 
```toml
[tool.mypy]
disable_error_code = "func-returns-value"
```
