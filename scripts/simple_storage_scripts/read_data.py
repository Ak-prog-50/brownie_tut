from brownie import SimpleStorage, accounts, config

# notes: Simple Storage object is an array object containing deployed contracts
print(f"length of Simple Storage : {len(SimpleStorage)}")


def read_contract():
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())  # no need to specify call() or transact() in here.


def main():
    read_contract()
