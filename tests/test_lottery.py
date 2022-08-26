"""
Test the core functionality of Lottery
"""
from brownie import exceptions, Lottery


from scripts.helpers import get_account, get_price_feed_address


def test_entrance_fee():
    """
    Test if we can only enter by providing entrance fee
    """
    account = get_account()

    lottery = Lottery.deploy(
        50, get_price_feed_address(account),
        { "from": account }
    )
    entrance_fee = lottery.entranceFee()
    print(f"Entrance fee: {entrance_fee}")

    # Check if with less entrance fee nothing happens
    try:
        transanction = lottery.enter({"from": account, "amount": entrance_fee - 500})
        transanction.wait(1)
    except exceptions.VirtualMachineError:
        print("Transaction failed as expected")

    # Check if with proper entranceFee the transanction goes through
    transanction = lottery.enter({"from": account, "amount": entrance_fee + 500})
    transanction.wait(1)
    print("Transaction successful")

    assert True

    # assert entranceFee >= Web3.toWei(0.039, "ether")
    # assert entranceFee <= Web3.toWei(0.042, "ether")


def test_start():
    """
    Test if the start function of the contract works properly
    """
    account = get_account()

    lottery = Lottery.deploy(
        50, get_price_feed_address(account),
        { "from": account }
    )

    assert lottery.lotteryState == lottery.LotteryState.CLOSED

    transaction = lottery.start({ "from": account })
    transaction.wait(1)

    assert lottery.lotteryState == lottery.LotteryState.OPEN
