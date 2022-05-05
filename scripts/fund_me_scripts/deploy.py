from brownie import FundMe
from ...utilities.get_account import get_account

def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from": account})
    print(f"Contract deployed to {fund_me.address}")

def main():
    deploy_fund_me()