// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StudentInfo {
    string public studentName;
    uint256 public studentID;
    constructor(string memory _initialName, uint256 _initialID){
        studentID=_initialID;
        studentName=_initialName;
    }
    function updateName(string memory _newName) public{
        studentName= _newName;
    }
    function updateID(uint256 _newID) public{
        studentID=_newID;
    }
}