from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8  #* 8 decimals are the default decimal count added in all Data Feed contracts.
STARTING_ETH_PRICE = 2000  #* starting input price for the contract's "answer" argument to convert to usd.

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
        MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_ETH_PRICE, "ether"), {"from": get_account()})
        print("Mocks Deployed!")
    elif(len(MockV3Aggregator) > 0):
        print("Mocks already deployed!")    

def get_pricefeed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        return MockV3Aggregator[-1].address
