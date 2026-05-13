// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BadVault {
    mapping(address => uint) public balances;
    address public immutable owner;

    constructor() {
        owner = msg.sender;
    }

    function deposit() public payable {
        balances[tx.origin] += msg.value; // Lỗi: Sử dụng tx.origin
    }

    function withdraw() public {
        uint amount = balances[msg.sender];
        //###fix reen
        require(amount > 0, "Insufficient balance");
        balances[msg.sender] = 0;
        //### fix low level calls
        // (bool success, ) = msg.sender.call{value: amount}(""); // Lỗi: Unchecked return value (nếu version cũ) & Reentrancy
        payable(msg.sender).transfer(amount);
        // balances[msg.sender] = 0; // Lỗi: CEI pattern vi phạm
        //### fix suicide
        // require(success, "Transfer failed");
        //###
    }

    function des() public {
        //### fix access control
        require(msg.sender == owner, "Only owner can call this");
        selfdestruct(payable(owner));
        //###
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}
