from brownie import network, accounts, config, MockV3Aggregator

FORKED_MAINET_ENVIRONEMNTS = ("mainnet-fork-dev", )
LOCAL_NETWORKS = ("development", "local-ganache")
DECIMALS = 8
STARTING_ETHER = 1200 * 10 ** 8


def get_account(index=None, id=None):
    # Fetch from local accounts
    if index is not None:
        return accounts[index]

    # Fetch from brownie configuration
    if id is not None:
        return accounts.load(id)

    # Default values
    current_network = network.show_active()
    if (
        current_network in LOCAL_NETWORKS
        or current_network in FORKED_MAINET_ENVIRONEMNTS
    ):
        return accounts[0]

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

def get_contract(cont):
    """
    Grab contracts or deploy them

    Args:
        cont (str): Contract name

    Returns:
        Contract: Contract instance
    """
