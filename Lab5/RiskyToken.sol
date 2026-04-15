// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RiskyToken {
    mapping(address => uint256) public balances;

    constructor() {
        balances[msg.sender] = 1000; // Mint cho deployer
    }

    function batchTransfer(address[] calldata receivers, uint256 value) external {
        // LỖ HỔNG NẰM Ở ĐÂY
        uint256 totalAmount;
        
        // Sử dụng unchecked cho phép nhân để tối ưu gas nhưng gây nguy hiểm
        unchecked {
            totalAmount = receivers.length * value;
        }

        require(balances[msg.sender] >= totalAmount, "Insufficient balance");

        balances[msg.sender] -= totalAmount;
        for (uint i = 0; i < receivers.length; i++) {
            balances[receivers[i]] += value;
        }
    }
}