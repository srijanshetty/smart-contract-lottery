// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
  enum LotteryState {
    OPEN,
    CLOSED,
    CALCULATING_WINNER
  }

  address[] public players;

  uint256 public usdEntryFee;
  LotteryState public lotteryState;

  AggregatorV3Interface internal priceFeed;

  constructor(uint256 _usdEntryFee, address _priceFeed) {
    usdEntryFee = _usdEntryFee * 10**18;
    priceFeed = AggregatorV3Interface(_priceFeed);

    lotteryState = LotteryState.CLOSED;
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
    players.push(msg.sender);
  }

  function startLottery() public onlyOwner {
    require(lotteryState == LotteryState.CLOSED, "Can't start a new lottery yet");
    lotteryState = LotteryState.OPEN;
  }

  function endLottery() public onlyOwner {
    lotteryState = LotteryState.CLOSED;
  }
}
