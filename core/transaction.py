from enum import Enum
from core.ISerializable import ISerializable
import datetime
import hashlib
import json
import globals

class Transaction(ISerializable): 
    class TransactionCode(Enum):
        HOLD_STAKE  = 1
        UPLOAD      = 2
        DOWNLOAD    = 3

    def __init__(self, code: TransactionCode, peer_id: str) -> None:
        self.code                           = code
        self.timestamp: datetime.datetime   = None
        self.hash: str                      = ""
        self.peer_id                        = peer_id
        super().__init__()
        
    def generate_timestamp(self) -> None:
        self.timestamp = datetime.datetime.now()
        
    def generate_hash(self) -> None:
        hash = hashlib.sha256(json.dumps(self.serialize()).encode(globals.ENCODING))
        dig = hash.hexdigest()
        self.hash = dig
        
    def confirm(self) -> dict:
        self.generate_timestamp()
        self.generate_hash()
        return self.serialize()

    def serialize(self) -> dict[str, object]:
        return {
            "transactionHash": self.hash,
            "TransactionCode": self.code.value
        }

class HoldStakeTransaction(Transaction):
    def __init__(self, peer_id: str, stake: int, ip: str, port: int) -> None:
        self.stake = stake
        self.ip = ip
        self.port = port
        super().__init__(code=Transaction.TransactionCode.HOLD_STAKE, peer_id=peer_id)
    
    def serialize(self) -> dict[str, object]:
        return {
            **super().serialize(),
            "stake": self.stake,
            "ip": self.ip,
            "port": self.port
        } 

class UploadTransaction(Transaction):
    def __init__(self, peer_id: str, file_name: str, transaction_cost: int) -> None:
        self.file_name = file_name
        self.transaction_cost = transaction_cost
        super().__init__(Transaction.TransactionCode.UPLOAD, peer_id)
    
    def serialize(self) -> dict[str, object]:
        return {
            **super().serialize(),
            "file_name": self.file_name,
            "transaction_cost": self.transaction_cost
        }
        
class DownloadTransaction(Transaction):
    def __init__(self, peer_id: str, file_name: str, receiver: str, cost: int, reward: int) -> None:
        super().__init__(Transaction.TransactionCode.DOWNLOAD, peer_id)
        self.file_name = file_name
        self.receiver = receiver
        self.cost = cost
        self.reward = reward
        
    def serialize(self) -> dict[str, object]:
        return {
            **super().serialize(),
            "file_name": self.file_name,
            "receiver": self.receiver,
            "cost": self.cost,
            "reward": self.reward
        }

def create_transaction(code: int, payload: dict) -> HoldStakeTransaction | UploadTransaction | DownloadTransaction:
    if code == Transaction.TransactionCode.HOLD_STAKE.value:
        return HoldStakeTransaction(**payload)
    elif code == Transaction.TransactionCode.UPLOAD.value:
        return UploadTransaction(**payload)
    elif code == Transaction.TransactionCode.DOWNLOAD.value:
        return DownloadTransaction(**payload)