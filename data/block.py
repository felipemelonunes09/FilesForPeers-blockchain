from typing import Self

class Block():
    class Header():
        def __init__(self, data: dict[str, object]) -> None:
                self.validatorPeerId                :str = data["validatorPeerId"]
                self.validatorPublicKey             :str = data["validatorPublicKey"]
                self.validatorVerificationSequence  :str = data["validatorVerificationSequence"]
                self.lastHash                       :str = data["lastHash"]
                self.lastHashTimestamp              :str = data["lastHashTimestamp"]
                self.blockNumber                    :str = data["blockNumber"]
                self.timestamp                      :str = data["timestamp"]
                self.stakeFee                       :str = data["stakeFee"]
                
                self.blockHash: str = ""
            
        def to_dict(self) -> dict:
            return {
                "validatorPeerId": self.validatorPeerId,
                "validatorPublicKey": self.validatorPublicKey,
                "validatorVerificationSequence": self.validatorVerificationSequence,
                "lastHash": self.lastHash,
                "lastHashTimestamp": self.lastHashTimestamp,
                "blockNumber": self.blockNumber,
                "timestamp": self.timestamp,
                "stakeFee": self.stakeFee,
                "blockHash": self.blockHash
            }
    class Payload():
        def __init__(self, data: dict[str, object]) -> None:
            self.sequence        = data["sequence"]
            self.transactions    = data["transactions"]

        def to_dict(self) -> dict:
            return {
                "sequence": self.sequence,
                "transactions": self.transactions
            }

    def __init__(self, header: Header, payload: Payload) -> None:
        self.__header = header
        self.__payload = payload
    def to_dict(self) -> dict:
        return {
            "__header": self.__header.to_dict(),
            "payload": self.__payload.to_dict()
        }
        
    def get_header(self) -> dict:
        return self.__header.to_dict()
    
    def get_payload(self) -> dict:
        return self.__payload.to_dict()
        
    def set_block_hash(self, hash: str) -> Self:
        self.__header.blockHash = hash
        
    def get_block_hash(self) -> str:
        return self.__header.blockHash
    
    def get_last_hash(self) -> str:
        return self.__header.lastHash
        
        