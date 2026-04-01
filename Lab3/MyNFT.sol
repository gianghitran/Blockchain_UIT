// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts@v4.9.3/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@v4.9.3/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts@v4.9.3/access/Ownable.sol";
import "@openzeppelin/contracts@v4.9.3/utils/Counters.sol";

contract MyNFT is ERC721URIStorage, ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    uint256 public constant MAX_SUPPLY = 100;
    uint256 public mintFee = 0.00001 ether;

    constructor() ERC721("MyNFTCollection", "MNC") {}

    function safeMint(address to, string memory uri) public payable {
        require(_tokenIds.current() < MAX_SUPPLY, "Reach Max Supply (100 NFT)");
        
        require(msg.value >= mintFee, "Not enough Mint (0.00001 ETH)");

        uint256 tokenId = _tokenIds.current();
        _tokenIds.increment();
        
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    // owner rút tiền 
    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // CÁC HÀM OVERRIDE
    function _beforeTokenTransfer(address from, address to, uint256 firstTokenId, uint256 batchSize)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, firstTokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721Enumerable, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}