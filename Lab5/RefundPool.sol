// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RefundPool {
    address[] public users;
    mapping(address => uint) public balances;

    function deposit() external payable {
        users.push(msg.sender);
        balances[msg.sender] += msg.value;
    }

    function refundAll() external {
        // Vòng lặp này sẽ tốn quá nhiều gas nếu mảng users quá lớn
        for (uint i = 0; i < users.length; i++) {
            address user = users[i];
            uint amount = balances[user];
            balances[user] = 0;
            (bool success, ) = user.call{value: amount}("");
            require(success);
        }
    }
}