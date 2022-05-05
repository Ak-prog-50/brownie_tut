from brownie import FundMe
import pytest

from brownie import network, config, accounts, MockV3Aggregator, exceptions

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



def test_funding_and_withdraw():
    account = get_account()
    price_feed_addr = get_pricefeed()
    fund_me = FundMe.deploy(price_feed_addr, {"from": account})
    entrance_fee = fund_me.getEntranceFee()

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    account = get_account()
    price_feed_addr = get_pricefeed()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = FundMe.deploy(price_feed_addr, {"from": account})
    bad_actor = accounts.add()
    print(f"\n\tfund_me{fund_me}")
    print(f"\n\tfund_me{account, accounts}")
    print(f"\n\tfund_me{network}")
    fund_me.withdraw({"from": bad_actor})
