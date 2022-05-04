// SPDX-License-Identifier: MIT

pragma solidity >=0.8.9 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract FundMe {
    using SafeMath for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    AggregatorV3Interface public priceFeedRinkeby;

    constructor() {
        priceFeedRinkeby = AggregatorV3Interface(address(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e));  //maybe no need to explicit say address()
    }

    function fund() payable public {
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns(uint256){
        return priceFeedRinkeby.version();
    }

    function getPrice() public view returns(uint256){
       (,int256 answer,,,) = priceFeedRinkeby.latestRoundData();
       return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 _weiAmount) public view returns(uint256) {
        uint256 ethToUsd = getPrice();
        uint256 weiAmountInUsd = (ethToUsd * _weiAmount) / 1000000000000000000;
        // uint256 weiAmountInUsd = (ethToUsd / 1000000000000000000);
        return weiAmountInUsd;
    }
}
