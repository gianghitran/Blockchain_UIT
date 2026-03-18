// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./StudentGrades.sol";
contract Event_AC is StudentGrades{
    address public owner;
    constructor(){
        owner=msg.sender;
    }
    event GradeUpdated(uint256 indexed subjectCode, string newName, uint8 newGrade);
    function addOrUpdateGrade(uint256 _subjectCode, string memory _subjectName, uint8 _grade) public override {
        require(msg.sender == owner, "Only the owner can call this function.");
        super.addOrUpdateGrade(_subjectCode, _subjectName, _grade);
        emit GradeUpdated(_subjectCode, _subjectName, _grade);
    }

}