from brownie import FundMe, config, network
from ...utilities.helpers import get_account, get_pricefeed


def deploy_fund_me():
    account = get_account()
    price_feed_addresss = get_pricefeed()
    fund_me = FundMe.deploy(
        price_feed_addresss,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
