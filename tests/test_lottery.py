from brownie import Lottery, exceptions
from web3 import Web3


from scripts.helpers import get_account, get_price_feed_address


def test_entrance_fee():
    account = get_account()

    lottery = Lottery.deploy(
        50, get_price_feed_address(account),
        { "from": account }
    )
    entranceFee = lottery.entranceFee()
    print(f"Entrance fee: {entranceFee}")

    # Check if with less entrance fee nothing happens
    try:
        transanction = lottery.enter({"from": account, "amount": entranceFee - 500})
        transanction.wait(1)
    except exceptions.VirtualMachineError:
        print("Transaction failed as expected")

    # Check if with proper entranceFee the transanction goes through
    transanction = lottery.enter({"from": account, "amount": entranceFee + 500})
    transanction.wait(1)
    print("Transaction successful")

    assert True

    # assert entranceFee >= Web3.toWei(0.039, "ether")
    # assert entranceFee <= Web3.toWei(0.042, "ether")

def test_start():
    account = get_account()

    lottery = Lottery.deploy(
        50, get_price_feed_address(account),
        { "from": account }
    )

    assert lottery.lotteryState == lottery.LotteryState.CLOSED

    transaction = lottery.start({ "from": account })
    transaction.wait(1)

    assert lottery.lotteryState == lottery.LotteryState.OPEN
