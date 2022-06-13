from brownie import config, network, Lottery

from scripts.helpers import get_account, get_price_feed_address


def deploy():
    # Get variables
    account = get_account()
    current_network = network.show_active()
    price_feed_address = get_price_feed_address(account)
    print(f"Using {price_feed_address} for price-feed")

    # Do the actual develoyment
    fund_me = Lottery.deploy(
        50, price_feed_address,
        {"from": account},
        publish_source=config["networks"][current_network].get("verify")
    )

    print(f"Deployed contract at {fund_me.address}")


def main():
    deploy()
