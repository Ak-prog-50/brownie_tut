from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8  #* 8 decimals are the default decimal count added in all Data Feed contracts.
STARTING_PRICE = 200000000000  #* starting price in USD.
# notes: MockV3Aggregator can't fetch the Eth/Usd price so STARTING_PRICE acts like the
# notes: fake USD value of 1 ETHER.

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if (len(MockV3Aggregator) <= 0):
        # ! Until previous commit Web3.toWei() has been used.
        # ! That's wrong. B'cos the second parameter of the contract 
        # ! requires a mock ETH/USD price.
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mocks Deployed!")
    elif(len(MockV3Aggregator) > 0):
        print("Mocks already deployed!")    

def get_pricefeed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        return MockV3Aggregator[-1].address
