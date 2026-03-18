// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;


contract StudentGrades {
    struct Subject {
        string subjectName;
        uint8 grade;
    }

    mapping(uint256 => Subject) public grades;

    function addOrUpdateGrade(uint256 _subjectCode, string memory _subjectName, uint8 _grade) public virtual {
        grades[_subjectCode] = Subject(_subjectName, _grade);
    }

    function getGrade(uint256 _subjectCode) public view returns (string memory, uint8) {
        Subject memory subj = grades[_subjectCode];
        return (subj.subjectName, subj.grade);
    }
}