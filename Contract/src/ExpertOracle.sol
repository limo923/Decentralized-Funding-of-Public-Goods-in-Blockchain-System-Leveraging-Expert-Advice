// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ExpertOracle{
    address[] public projectlist;
    address[] public experts;
    mapping(address => uint256) public reputations;
    address public creator;

    constructor() {
        creator = msg.sender;
    }

    modifier onlyCreator() {
        require(msg.sender == creator);
        _;
    }

    function createProject(address _projectAddress) public {
        projectlist.push(_projectAddress);
    }

    function addExpert(address _address) public {
        experts.push(_address);
    }

    function isAddressInList(address _address) public view returns (bool) {
        for (uint i = 0; i < experts.length; i++) {
            if (experts[i] == _address) {
                return true;
            }
        }
        return false;
    }
    
    function reputationUpdate(address[] calldata _experts, uint256[] calldata _newreputations) public onlyCreator() {
        for (uint i = 0; i < experts.length; i++){
            if(isAddressInList(_experts[i])){
                reputations[_experts[i]] = _newreputations[i];
            }
        }
    }

}
