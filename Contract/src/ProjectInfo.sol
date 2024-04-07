// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "../src/ExpertOracle.sol";

contract ProjectInfo{
    uint id;
    uint256 public investment;
    uint256 public performance;
    mapping(address => uint256) public advices;
    mapping(address => uint256) public valuations;

    ExpertOracle public expertOracle;
    address public creator;

    constructor(address _addressExpertOracle) {
        expertOracle = ExpertOracle(_addressExpertOracle);
        creator = msg.sender;
        expertOracle.createProject(address(this));
    }

    modifier onlyCreator() {
        require(msg.sender == creator);
        _;
    }

    function expertAdvice(uint256 _advice) public {
        if(expertOracle.isAddressInList(msg.sender)){
            advices[msg.sender] = _advice;
        }
    }

    function expertValuation(uint256 _valuation) public {
        if(expertOracle.isAddressInList(msg.sender)){
            valuations[msg.sender] = _valuation;
        }
    }

    function investmentDecide(uint256 _investment) public onlyCreator {
        investment = _investment;
    }
    
    function getInvestment() public view onlyCreator returns (uint256) {
        return investment;
    }

    function projectFeedback(uint256 _performance) public onlyCreator {
        performance = _performance;
    }

    function getPerformance() public view onlyCreator returns (uint256) {
        return performance;
    }

}
