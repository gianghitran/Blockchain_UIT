// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract RefundPool_Secure {
    mapping(address => uint) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // Không còn hàm refundAll
    // User phải tự gọi hàm này -> Tránh DoS
    function withdraw() external {
        uint amount = balances[msg.sender];
        require(amount > 0);
        balances[msg.sender] = 0;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
    }
}