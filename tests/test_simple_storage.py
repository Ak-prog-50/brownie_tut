from brownie import SimpleStorage, accounts

# notes: Arrange, Act, Assert pattern in unit testing is used in here.

def test_deploy():
    # * 1. Arrange
    account = accounts[0]
    expected = 0

    # * 2. Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()

    # * 3. Assert
    assert starting_value == expected


def test_updating_storage():
    # * 1. Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # * 2. Act
    expected = 15
    txn = simple_storage.store(expected, {"from": account})
    txn.wait(1)

    # * 3. Assert
    assert expected == simple_storage.retrieve()
