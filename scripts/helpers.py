from brownie import network, accounts, config, MockV3Aggregator, VRFCoordinatorV2

FORKED_MAINET_ENVIRONEMNTS = ("mainnet-fork-dev", )
LOCAL_NETWORKS = ("development", "local-ganache")
DECIMALS = 8
STARTING_ETHER = 1200 * 10 ** 8


def get_account():
    current_network = network.show_active()

    if (
        current_network in LOCAL_NETWORKS
        or current_network in FORKED_MAINET_ENVIRONEMNTS
    ):
        return accounts[0]

    if network.show_active() == "kovan":
        return accounts.add(config["wallets"]["from_key"])


def get_price_feed_address(account):
    current_network = network.show_active()

    price_feed_address = ""
    if current_network not in LOCAL_NETWORKS:
        price_feed_address = config["networks"][current_network]["eth_usd_price_feed"]
    else:
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(
                DECIMALS, STARTING_ETHER,
                {"from": account}
            )

        price_feed_address = MockV3Aggregator[-1].address

    print(f"Using {price_feed_address} for price-feed")
    return price_feed_address

def get_randomness_feed_address(account):
    current_network = network.show_active()

    randomness_feed_address = ""
    if current_network not in LOCAL_NETWORKS:
        randomness_feed_address = config["networks"][current_network]["randomness_feed"]
    else:
        if len(VRFCoordinatorV2) <= 0:
            VRFCoordinatorV2.deploy(
                DECIMALS, STARTING_ETHER,
                {"from": account}
            )

        randomness_feed_address = VRFCoordinatorV2[-1].address

    print(f"Using {randomness_feed_address} for randomness-feed")
    return randomness_feed_address
