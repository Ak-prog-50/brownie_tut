from brownie import network, config, accounts, MockV3Aggregator

DECIMALS = 18
STARTING_PRICE = 200000000000


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_pricefeed():
    if network.show_active() != "development":
        return config["networks"]["rinkeby"]["eth_usd_price_feed"]
    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        mockV3 = MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mocks Deployed!")
        return mockV3.address
