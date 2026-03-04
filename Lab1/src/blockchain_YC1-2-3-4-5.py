
# -*- coding: utf-8 -*-
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import binascii

import requests
from flask import Flask, jsonify, request
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Blockchain:
    def __init__(self):
        """
        Hàm khởi tạo của lớp Blockchain.
        """
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Tạo khối nguyên thủy (genesis block)
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Thêm một node mới vào danh sách các node.
        :param address: Địa chỉ của node. Ví dụ: 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Chấp nhận URL dạng '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('URL không hợp lệ')

    def valid_chain(self, chain):
        """
        Kiểm tra xem một chuỗi blockchain có hợp lệ hay không.
        :param chain: Một chuỗi blockchain
        :return: True nếu hợp lệ, False nếu không.
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Kiểm tra mã băm của khối có đúng không
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Kiểm tra bằng chứng công việc có đúng không
            if not self.valid_proof(last_block['proof'], block['proof'], block['previous_hash']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Đây là thuật toán đồng thuận, nó giải quyết các xung đột
        bằng cách thay thế chuỗi của chúng ta bằng chuỗi dài nhất trong mạng.
        :return: True nếu chuỗi của chúng ta bị thay thế, False nếu không.
        """
        neighbours = self.nodes
        new_chain = None

        # Chúng ta chỉ tìm kiếm các chuỗi dài hơn chuỗi của mình
        max_length = len(self.chain)

        # Lấy và xác minh các chuỗi từ tất cả các node trong mạng
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Kiểm tra xem độ dài có lớn hơn và chuỗi có hợp lệ không
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Thay thế chuỗi của chúng ta nếu chúng ta phát hiện ra một chuỗi mới, dài hơn và hợp lệ
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Tạo một khối mới trong Blockchain.
        :param proof: Bằng chứng được đưa ra bởi thuật toán Proof of Work
        :param previous_hash: Mã băm của khối trước đó
        :return: Khối mới
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset danh sách giao dịch hiện tại
        self.current_transactions = []

        self.chain.append(block)
        return block
####################### YC3 #######################
    def get_balance(self, address):
        """
        Tính toán số dư của một địa chỉ bằng cách duyệt qua tất cả các khối và giao dịch.
        :param address: Địa chỉ cần kiểm tra số dư
        :return: Số dư của địa chỉ
        """
        balance = 0
        
        # Duyệt qua tất cả các khối trong chuỗi
        for block in self.chain:
            for transaction in block['transactions']:
                # Nếu địa chỉ là người nhận, cộng số coin
                if transaction['recipient'] == address:
                    balance += transaction['amount']
                # Nếu địa chỉ là người gửi (và không phải giao dịch thưởng), trừ số coin
                if transaction['sender'] == address:
                    balance -= transaction['amount']
        
        # Duyệt qua các giao dịch đang chờ (chưa được đào)
        for transaction in self.current_transactions:
            if transaction['recipient'] == address:
                balance += transaction['amount']
            if transaction['sender'] == address:
                balance -= transaction['amount']
        
        return balance
####################### YC3 #######################
    def new_transaction(self, sender, recipient, amount):
        """
        Tạo một giao dịch mới để đi vào khối được đào tiếp theo.
        :param sender: Địa chỉ của người gửi
        :param recipient: Địa chỉ của người nhận
        :param amount: Số lượng
        :return: Chỉ số của khối sẽ chứa giao dịch này
        """
####################### YC3 #######################
        # Kiểm tra số dư nếu không phải giao dịch thưởng (sender != "0")
        if sender != "0":
            balance = self.get_balance(sender)
            if balance < amount:
                return -1  # Số dư không đủ
####################### YC3 #######################
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Tạo mã băm SHA-256 của một khối.
        :param block: Khối
        """
        # Chúng ta phải đảm bảo rằng Dictionary được sắp xếp, nếu không chúng ta sẽ có các mã băm không nhất quán
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Thuật toán Proof of Work đơn giản:
         - Tìm một số p' sao cho hash(pp') có 4 số 0 ở đầu
         - p là proof của khối trước, p' là proof mới
        :param last_block: Khối cuối cùng
        :return: Bằng chứng công việc (proof)
        """
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    def get_mining_reward(self):
        """
        Tính toán phần thưởng đào khối dựa trên chiều dài chuỗi hiện tại.
        Công thức: R = 1 / (2^n) với n là mức thưởng (length // 10)
        """
        # Lấy chiều dài chuỗi chia lấy phần nguyên cho 10 để ra mức thưởng n
        n = len(blockchain.chain) // 10
        # Tính R theo công thức
        R = 1 / (2 ** n)
        return R
    
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Xác thực bằng chứng: hash(last_proof, proof, last_hash) có chứa 4 số 0 ở đầu không?
        :param last_proof: Proof trước đó
        :param proof: Proof hiện tại
        :param last_hash: Mã băm của khối trước đó
        :return: True nếu đúng, False nếu sai.
        """
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # Thay đổi độ khó bằng cách tăng số lượng số '0' ở đầu
        return guess_hash[:5] == "00000"

    @staticmethod
    def verify_signature(sender_public_key, signature, transaction_string):
        """
        Kiểm tra chữ ký số của giao dịch.
        """
        try:
            # Chuyển đổi public key từ dạng hex sang đối tượng RSA
            public_key = RSA.import_key(binascii.unhexlify(sender_public_key))
            # Băm chuỗi dữ liệu giao dịch
            h = SHA256.new(transaction_string.encode('utf8'))
            # Xác thực chữ ký
            pkcs1_15.new(public_key).verify(h, binascii.unhexlify(signature))
            return True
        except (ValueError, TypeError):
            return False
    

# Khởi tạo Node
app = Flask(__name__)

# Tạo một địa chỉ duy nhất toàn cầu cho node này
node_identifier = str(uuid4()).replace('-', '')

# Khởi tạo Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # Chạy thuật toán PoW để lấy proof tiếp theo...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Chúng ta phải nhận phần thưởng cho việc tìm ra proof.
    # Người gửi là "0" để biểu thị rằng node này đã đào một coin mới.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=blockchain.get_mining_reward(),
    )

    # Tạo khối mới bằng cách thêm nó vào chuỗi
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Một khối mới đã được tạo (mined)",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200



# @app.route('/transactions/new', methods=['POST'])
# def new_transaction():
#     values = request.get_json()

#     # Kiểm tra các trường bắt buộc có trong dữ liệu POST không
#     required = ['sender', 'recipient', 'amount']
#     if not all(k in values for k in required):
#         return 'Thiếu giá trị', 400

#     # Tạo một giao dịch mới
#     index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
# ####################### YC3 #######################
#     # Kiểm tra nếu giao dịch thất bại do số dư không đủ
#     if index == -1:
#         response = {'message': 'Số dư không đủ'}
#         return jsonify(response), 400
# ####################### YC3 #######################
#     response = {'message': f'Giao dịch sẽ được thêm vào khối {index}'}
#     return jsonify(response), 201
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount', 'signature', 'sender_public_key']
    if not all(k in values for k in required):
        return 'Thiếu giá trị', 400

    sender = values['sender']
    recipient = values['recipient']
    amount = values['amount']
    signature = values['signature']
    sender_pub_key = values['sender_public_key']

    # Chuỗi dữ liệu phải khớp 100% với lúc ký ở API /wallet/sign
    transaction_string = f"{sender}{recipient}{amount}"

    # Xác thực chữ ký
    if not blockchain.verify_signature(sender_pub_key, signature, transaction_string):
        return jsonify({'message': 'Lỗi: Chữ ký không hợp lệ!'}), 400

    # Nếu hợp lệ, đưa giao dịch vào blockchain
    index = blockchain.new_transaction(sender, recipient, amount)
    
    if index is False: 
        return jsonify({'message': 'Số dư không đủ'}), 400

    response = {'message': f'Giao dịch hợp lệ và sẽ được thêm vào khối {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Lỗi: Vui lòng cung cấp một danh sách node hợp lệ", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Các node mới đã được thêm vào',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Chuỗi của chúng ta đã được thay thế',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Chuỗi của chúng ta là chính xác',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


############# YC 5
@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    """Tạo một cặp khóa Public/Private Key RSA mới"""
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()

    response = {
        'private_key': binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.export_key(format='DER')).decode('ascii')
    }
    return jsonify(response), 200

@app.route('/wallet/sign', methods=['POST'])
def sign_transaction():
    values = request.get_json()
    required = ['private_key', 'sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Thiếu giá trị', 400

    private_key_hex = values['private_key']
    sender = values['sender']
    recipient = values['recipient']
    amount = values['amount']

    transaction_string = f"{sender}{recipient}{amount}"
    h = SHA256.new(transaction_string.encode('utf8'))

    try:
        private_key = RSA.import_key(binascii.unhexlify(private_key_hex))
        signature = pkcs1_15.new(private_key).sign(h)
        signature_hex = binascii.hexlify(signature).decode('ascii')
        
        return jsonify({'signature': signature_hex}), 200
    except Exception as e:
        return jsonify({'message': 'Lỗi khi ký', 'error': str(e)}), 400
    
    
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)