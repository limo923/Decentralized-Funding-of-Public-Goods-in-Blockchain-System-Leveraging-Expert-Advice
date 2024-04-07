// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";

import "../src/ExpertOracle.sol";
import "../src/ProjectInfo.sol";

contract TestProjectInfo {

    function testExpertAdvice() public {
        ExpertOracle expertoracle = new ExpertOracle();
        address expertOracleAddress = address(expertoracle); 
        ProjectInfo projectInfo = new ProjectInfo(expertOracleAddress); 
        address newexpert = address(this);
        
        projectInfo.expertAdvice(100);
        assert(!(projectInfo.advices(address(this)) == 100));
        
        expertoracle.addExpert(newexpert);
        projectInfo.expertAdvice(1000);
        assert(projectInfo.advices(address(this)) == 1000);
    }

    function testExpertValuation() public {
        ExpertOracle expertoracle = new ExpertOracle();
        address expertOracleAddress = address(expertoracle); 
        ProjectInfo projectInfo = new ProjectInfo(expertOracleAddress); 
        address newexpert = address(this);
        
        projectInfo.expertValuation(100);
        assert(!(projectInfo.valuations(address(this)) == 100));
        
        expertoracle.addExpert(newexpert);
        projectInfo.expertValuation(1000);
        assert(projectInfo.valuations(address(this)) == 1000);
    }

    function testInvestmentDecide() public {
        ExpertOracle expertoracle = new ExpertOracle();
        address expertOracleAddress = address(expertoracle);
        ProjectInfo projectInfo = new ProjectInfo(expertOracleAddress); 
        
        projectInfo.investmentDecide(500);
        assert(projectInfo.getInvestment() == 500);
    }

    function testProjectFeedback() public {
        ExpertOracle expertoracle = new ExpertOracle();
        address expertOracleAddress = address(expertoracle);
        ProjectInfo projectInfo = new ProjectInfo(expertOracleAddress); 
        
        projectInfo.projectFeedback(1000);
        assert(projectInfo.getPerformance() == 1000);
    }

}