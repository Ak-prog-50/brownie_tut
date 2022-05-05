from brownie import FundMe
from ...utilities.helpers import get_account

fund_me = FundMe[-1]
account = get_account()

def fund():
    print(f"Contract address {fund_me}")
    entrance_fee = fund_me.getEntranceFee()
    print(f"Entrance Fee {entrance_fee}")
    print("\nFunding...")
    fund_me.fund({"from": account, "value": entrance_fee})
    print(f"Total Amount of {entrance_fee} has been funded!")


def withdraw():
    print(f"Contract address {fund_me}")
    print("\nWithdrawing Funds...")
    fund_me.withdraw({"from": account})
    print("\n\tSuccesfully withdrawed! If you got an error that's your problem!")

def main():
    fund()
    withdraw()