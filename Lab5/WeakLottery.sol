// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract WeakLottery {
    function play() public payable {
        require(msg.value == 0.1 ether);
        // Random yếu dựa trên timestamp
        uint256 random = uint256(keccak256(abi.encodePacked(block.timestamp, msg.sender))) % 2;
        
        if (random == 1) {
            // Thắng: Trả lại tiền + thưởng
            payable(msg.sender).transfer(0.2 ether);
        }
    }
    
    // Nạp tiền vào quỹ thưởng
    receive() external payable {}
}