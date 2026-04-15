// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract EtherStore_ManualLock {
    bool internal locked; // Biến cờ khóa

    // Định nghĩa modifier để chặn gọi lại
    modifier noReentrant() {
        require(!locked, "No re-entrancy");
        locked = true; // Khóa lại trước khi chạy hàm
        _;
        locked = false; // Mở khóa sau khi chạy xong
    }

    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // Áp dụng modifier vào đây
    function withdraw() public noReentrant {
        uint bal = balances[msg.sender];
        require(bal > 0);
        // LỖ HỔNG: Gửi tiền trước khi cập nhật số dư
        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send Ether");
        balances[msg.sender] = 0;
    }
}