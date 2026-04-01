// src/App.js
import { useState } from 'react';
import { ethers } from 'ethers';
import MyNFT_ABI from './utils/MyNFT.json';
import './App.css';

// ==================================================================
// !!! CẬP NHẬT 2 GIÁ TRỊ NÀY !!!
// Dán địa chỉ hợp đồng của SV từ Bước 1.3
const contractAddress = "0x376b8cE50066756c3dF2D723b4e49d7b7728bb47"; 
// Dán URL metadata của SV từ Bước 1.1
const metadataURI = "https://gateway.pinata.cloud/ipfs/bafkreicz35exm3uj53mz3k63d7s5knxldf4or6zrfcr3dwfyfokflxenr4";
// ==================================================================

// ##################################################################


function App() {
  

  const [walletAddress, setWalletAddress] = useState(null);
  const [mintingStatus, setMintingStatus] = useState(null);
  const [txHash, setTxHash] = useState(null);
// ##################################################################
  const [searchId, setSearchId] = useState("");
  const [searchedNFT, setSearchedNFT] = useState(null);
  // State cho Bộ sưu tập
  const [myCollection, setMyCollection] = useState([]);
  const [isLoadingCollection, setIsLoadingCollection] = useState(false);

  async function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
      try {
        // 1. ÉP METAMASK CHUYỂN SANG MẠNG SEPOLIA (ChainId: 0xaa36a7)
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: '0xaa36a7' }],
        });
      console.log('MetaMask is installed!');
      // try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        console.log('Connected account:', accounts[0]);
        setWalletAddress(accounts[0]);
      } catch (error) {
        console.error('User denied account access', error);
      }
    } else {
      console.log('Please install MetaMask!');
      alert('Please install MetaMask!');
    }
  }

  async function handleMint() {
    if (!walletAddress) {
      alert("Please connect your wallet first.");
      return;
    }
    
    if (typeof window.ethereum !== 'undefined') {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const nftContract = new ethers.Contract(contractAddress, MyNFT_ABI, signer);

      try {
        setMintingStatus('Minting... Vui lòng xác nhận giao dịch trên MetaMask.');
        setTxHash(null);

        // ################################################################## Frontend phí Mint
        const mintFee = ethers.parseEther("0.01"); 
        const tx = await nftContract.safeMint(walletAddress, metadataURI, { 
            value: mintFee 
        });

        // const tx = await nftContract.safeMint(walletAddress, metadataURI);
        // ##################################################################
        console.log('Transaction sent:', tx.hash);
        
        setMintingStatus('Đang chờ giao dịch được xác nhận...');
        await tx.wait();
        
        console.log('Transaction confirmed!');
        setMintingStatus('Mint thành công!');
        setTxHash(tx.hash);

      } catch (error) {
        console.error('Minting failed:', error);
        setMintingStatus(`Mint thất bại: ${error.message}`);
      }
    }
  } 

  async function handleSearchNFT() {
    try {
      if (!window.ethereum) return alert("Vui lòng cài MetaMask");

      const provider = new ethers.BrowserProvider(window.ethereum);
      const nftContract = new ethers.Contract(contractAddress, MyNFT_ABI, provider);

      // Bước 1: Gọi hàm view trên Contract để lấy Link file JSON
      const tokenUri = await nftContract.tokenURI(searchId);
      
      // Bước 2: Dùng fetch tải dữ liệu từ file JSON đó về
      const response = await fetch(tokenUri);
      const metadata = await response.json();
      if (metadata.image && metadata.image.startsWith("ipfs://")) {
        metadata.image = metadata.image.replace("ipfs://", "https://gateway.pinata.cloud/ipfs/");
      }

      // Bước 3: Lưu dữ liệu vào biến để đưa lên màn hình
      setSearchedNFT(metadata);

    } catch (error) {
      alert("Lỗi: Không tìm thấy NFT này! Đảm bảo bạn nhập đúng số thứ tự đã Mint.");
      console.error(error);
      setSearchedNFT(null);
    }
  }
  {/* ... */}
  {/* ... */}
  // ##################################################################
  // HÀM TẢI BỘ SƯU TẬP
  // ##################################################################
  async function loadMyCollection() {
    if (!walletAddress) {
      alert("Vui lòng kết nối ví trước!");
      return;
    }

    try {
      setIsLoadingCollection(true);
      setMyCollection([]); // Xóa dữ liệu cũ trước khi tải mới

      const provider = new ethers.BrowserProvider(window.ethereum);
      const nftContract = new ethers.Contract(contractAddress, MyNFT_ABI, provider);

      const balance = await nftContract.balanceOf(walletAddress);
      const totalNFTs = Number(balance);
      
      if (totalNFTs === 0) {
        setIsLoadingCollection(false);
        return; // Nếu không có NFT nào thì dừng
      }

      let tempCollection = [];

      for (let i = 0; i < totalNFTs; i++) {
        const tokenId = await nftContract.tokenOfOwnerByIndex(walletAddress, i);
        
        let tokenUri = await nftContract.tokenURI(tokenId);
        if (tokenUri.startsWith("ipfs://")) {
          tokenUri = tokenUri.replace("ipfs://", "https://gateway.pinata.cloud/ipfs/");
        }

        const response = await fetch(tokenUri);
        const metadata = await response.json();

        if (metadata.image && metadata.image.startsWith("ipfs://")) {
          metadata.image = metadata.image.replace("ipfs://", "https://gateway.pinata.cloud/ipfs/");
        }

        tempCollection.push({
          id: tokenId.toString(),
          name: metadata.name,
          description: metadata.description,
          image: metadata.image
        });
      }

      setMyCollection(tempCollection);
      setIsLoadingCollection(false);

    } catch (error) {
      console.error("Lỗi tải bộ sưu tập:", error);
      alert("Đã xảy ra lỗi khi tải bộ sưu tập. Xem console để biết chi tiết.");
      setIsLoadingCollection(false);
    }
    {/* ... */}
    {/* ... */}
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>My NFT DApp</h1>
        
        <button onClick={connectWallet} className="connect-button">
          {walletAddress 
            ? `Connected: ${walletAddress.substring(0, 6)}...${walletAddress.substring(38)}` 
            : 'Connect Wallet'}
        </button>

        {walletAddress && (
          <div className="mint-container">
            <button onClick={handleMint} className="mint-button">Mint My NFT</button>
            {mintingStatus && <p className="status-text">{mintingStatus}</p>}
            {txHash && (
              <p className="tx-link">
                Xem giao dịch: 
                <a href={`https://sepolia.etherscan.io/tx/${txHash}`} target="_blank" rel="noopener noreferrer"> Etherscan</a>
              </p>
            )}
          </div>
        )}
    
        {/* ================================================================== */}
        {/* GIAO DIỆN TÌM KIẾM NFT */}
        <div style={{ marginTop: "50px", borderTop: "2px solid #fff", paddingTop: "20px", width: "100%", maxWidth: "600px", display: "flex", flexDirection: "column", alignItems: "center" }}>
          <h2 style={{ color: "#fac337" }}>Search NFT</h2>
          
          <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
            <input 
              type="number" 
              placeholder="NFT ID (e.g., 0)" 
              onChange={(e) => setSearchId(e.target.value)} 
              style={{ padding: "10px", borderRadius: "5px", border: "none" }}
            />
            <button onClick={handleSearchNFT} style={{ padding: "10px 20px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none", borderRadius: "5px", fontWeight: "bold" }}>
              Search
            </button>
          </div>

          {searchedNFT && (
            <div style={{ border: "1px solid white", borderRadius: "10px", padding: "20px", width: "300px", backgroundColor: "rgba(255,255,255,0.1)" }}>
              <h3 style={{ marginTop: 0, color: "#61dafb" }}>{searchedNFT.name}</h3>
              <p style={{ fontSize: "16px", textAlign: "justify" }}><strong>Description:</strong> {searchedNFT.description}</p>
              <img src={searchedNFT.image} alt="NFT Artwork" style={{ width: "100%", borderRadius: "10px" }} />
            </div>
          )}
        </div>
        {/* ================================================================== */}
        {/* ... */}
        {/* ... */}
        {/* ################################################################## */}
        {/* HIỂN THỊ BỘ SƯU TẬP */}
        {walletAddress && (
          <div style={{ marginTop: "50px", borderTop: "2px solid #fff", paddingTop: "20px", width: "100%", maxWidth: "800px" }}>
            <h2>Bộ sưu tập của tôi</h2>
            
            <button 
              onClick={loadMyCollection} 
              disabled={isLoadingCollection}
              style={{ padding: "10px 20px", cursor: "pointer", backgroundColor: "#ffc107", color: "black", border: "none", borderRadius: "5px", fontWeight: "bold", marginBottom: "20px" }}
            >
              {isLoadingCollection ? "Đang tải dữ liệu..." : "Tải / Làm mới Bộ Sưu Tập"}
            </button>

            {myCollection.length === 0 && !isLoadingCollection && (
              <p>Bạn chưa sở hữu NFT nào trong bộ sưu tập này.</p>
            )}

            <div style={{ display: "flex", flexWrap: "wrap", gap: "20px", justifyContent: "center" }}>
              {myCollection.map((nft, index) => (
                <div key={index} style={{ border: "1px solid white", borderRadius: "10px", padding: "15px", width: "200px", backgroundColor: "rgba(255,255,255,0.1)" }}>
                  <img src={nft.image} alt={nft.name} style={{ width: "100%", borderRadius: "8px", height: "200px", objectFit: "cover" }} />
                  <h4 style={{ color: "#61dafb", margin: "10px 0 5px 0" }}>{nft.name}</h4>
                  <p style={{ margin: "0 0 10px 0", fontSize: "14px", color: "#ccc" }}>ID: {nft.id}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        {/* ################################################################## */}
        {/* ... */}
        {/* ... */}
      </header>
    </div>
  );
}

export default App;