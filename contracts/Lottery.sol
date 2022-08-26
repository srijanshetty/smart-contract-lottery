// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
  enum LotteryState {
    OPEN,
    CLOSED,
    CALCULATING_WINNER
  }

  // constants
  uint256 internal randomnessFee;
  bytes32 internal keyHash;

  uint256 public usdEntryFee;

  AggregatorV3Interface internal priceFeed;

  // Current state of the game
  address payable[] public players;
  address payable public recentWinner;
  uint256 public recentRandomNumber;
  LotteryState public lotteryState;

  constructor(
    uint256 _usdEntryFee,
    address _priceFeed,
    address _vrfCordinator,
    address _linkToken,
    uint256 _randomnessFee,
    bytes32 _keyHash
  ) VRFConsumerBase(
    _vrfCordinator,
    _linkToken
  ) {
    usdEntryFee = _usdEntryFee * 10**18;
    priceFeed = AggregatorV3Interface(_priceFeed);

    lotteryState = LotteryState.CLOSED;

    randomnessFee = _randomnessFee;
    keyHash = _keyHash;
  }

  function entranceFee() public view returns(uint256) {
    (,int256 answer,,,) = priceFeed.latestRoundData();

    // We get 8 decimals for ETH/USD, normalize to 18 digits of Wei
    uint256 adjustedPrice = uint256(answer * 10 ** 10);

    uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
    return costToEnter;
  }

  function enter() public payable {
    // require the entrance fee
    require(msg.value >= entranceFee(), "Insufficient entry fee");
    players.push(payable(msg.sender));
  }

  function startLottery() public onlyOwner {
    require(lotteryState == LotteryState.CLOSED, "Can't start a new lottery yet");
    lotteryState = LotteryState.OPEN;
  }

  function endLottery() public onlyOwner {
    lotteryState = LotteryState.CALCULATING_WINNER;

    // Request randomness
    requestRandomness(keyHash, randomnessFee);
  }

  function fulfillRandomness(bytes32 _requestId, uint256 _randomNumber) internal override {
    require(lotteryState == LotteryState.CALCULATING_WINNER, "Invalid state");
    require(_randomNumber > 0, "Invalid random number");
    recentRandomNumber = _randomNumber;

    // Caculate a random winner
    uint256 winnerIndex = _randomNumber % players.length;
    recentWinner = players[winnerIndex];

    // Transfer all the assets
    recentWinner.transfer(address(this).balance);

    // Invalidate all state
    players = new address payable[](0);
    lotteryState = LotteryState.OPEN;
  }
}
