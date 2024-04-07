// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.19;

import "forge-std/Test.sol";

import "../src/ExpertOracle.sol";

contract TestExpertOracle is Test {
    ExpertOracle public expertoracle;
    
    function setUp() public {
        expertoracle = new ExpertOracle();
    }

    function testReputationUpdate() public {
        // Setup
        address[] memory newexperts = new address[](2);
        newexperts[0] = address(0x123);
        newexperts[1] = address(0x456);

        uint256[] memory newReputations = new uint256[](2);

        newReputations[0] = 100;
        newReputations[1] = 200;

        expertoracle.addExpert(newexperts[0]);
        expertoracle.addExpert(newexperts[1]);
        
        // Execute reputationUpdate function
        expertoracle.reputationUpdate(newexperts, newReputations);
        
        // Assert reputations are updated correctly
        uint256 reputation1 = expertoracle.reputations(address(0x123));
        uint256 reputation2 = expertoracle.reputations(address(0x456));

        assertEq(reputation1, 100);
        assertEq(reputation2, 200);
    }

}
