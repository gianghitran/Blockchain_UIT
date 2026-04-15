// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Spammer {
    // Dùng call cấp thấp để không cần khai báo interface phức tạp
    function spam(address _poolAddress) public payable {
        for(uint i = 0; i < 50; i++) {
            // Chia nhỏ tiền nạp (ví dụ 0.001 ETH mỗi lần)
            (bool success, ) = _poolAddress.call{value: 0.001 ether}(
                abi.encodeWithSignature("deposit()")
            );
            require(success, "Call failed");
        }
    }

    receive() external payable {}
}