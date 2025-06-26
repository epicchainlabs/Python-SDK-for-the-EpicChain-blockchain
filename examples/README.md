The modules in the root of this directory contain examples how to perform common actions on the EpicChain blockchain. 
The `shared` package contains all the test data and wallets to setup the private network and can be ignored.

```python
if __name__ == "__main__":
   with shared.EpicChainExpress() as epicchainxp:
        asyncio.run(example_airdrop(epicchainxp))
```

update this to include the epicchainxp executable path
```python
if __name__ == "__main__":
    with shared.EpicChainExpress.at("path_to_epicchainxp_executable") as epicchainxp:
        asyncio.run(example_airdrop(epicchainxp))
```