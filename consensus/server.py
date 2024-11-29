
from queue import Queue

import json
import logging
import socket
import threading
from typing import Callable
import globals
import yaml

class Server():
    
    logger: logging.Logger              = logging.getLogger(__name__)
    configuration: dict[str, object]    = dict()
    
    blocks: list[dict[str, dict]]       = list()
    
    queue: Queue[tuple[int, dict, tuple[str, int], socket.socket]] = Queue()
    
    class RequestBlockchainChunk(threading.Thread):
        def __init__(self) -> None:
            super().__init__()
            self.__data_address = (Server.configuration["blockchain"]["data"]["ip"], Server.configuration["blockchain"]["data"]["port"])
            self.__encoded_message_data = json.dumps({"message_type": 4}).encode(globals.ENCODING)
            
        def run(self) -> None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.__data_address)
            sock.sendall(self.__encoded_message_data)
            bin = sock.recv(1024)
            data = json.loads(bin.decode(globals.ENCODING))
            Server.blocks = data['result']
            return super().run()
        
    class ClientThreadConnection(threading.Thread):
        def __init__(self, connection: socket.socket, address: tuple[str, int]) -> None:
            self.__conn = connection
            self.__address = address
            super().__init__()

        def run(self) -> None:
            return super().run()
        
    class Server():
        logger: logging.Logger              = logging.getLogger(__name__)
        configuration: dict[str, object]    = dict()
        blocks: list[dict[str, dict]]       = list()
        queue: Queue[dict]                  = Queue()
        
        class RequestBlockchainChunk(threading.Thread):
            def __init__(self) -> None:
                super().__init__()
                self.__data_address = (Server.configuration["blockchain"]["data"]["ip"], Server.configuration["blockchain"]["data"]["port"])
                self.__encoded_message_data = json.dumps({"message_type": 4}).encode(globals.ENCODING)
                
            def run(self) -> None:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(self.__data_address)
                    sock.sendall(self.__encoded_message_data)
                    bin = sock.recv(1024)
                    data = json.loads(bin.decode(globals.ENCODING))
                    Server.blocks = data['result']
                except Exception as e:
                    Server.logger.error(f"Error requesting blockchain chunk: {e}")
                finally:
                    return super().run()
            
        class ClientThreadConnection(threading.Thread):
            def __init__(self, connection: socket.socket, address: tuple[str, int]) -> None:
                self.__conn = connection
                self.__address = address
                super().__init__()

            def run(self) -> None:
                alive = True
                while alive:
                    bin = self.__conn.recv(1024)
                    if len(bin) > 2:
                        segmented_data = bin.split("b\n")
                        for data in segmented_data:
                            data = data.decode(globals.ENCODING)
                            message: dict = json.loads(data)
                            message_type = message.get("message_type")
                            message_data = message.get("message_data")
                            
                            if message_type == Server.MessageType.CLOSE.value:
                                alive = False
                                self.__conn.close()
                            else:
                                Server.queue.put((message_type, message_data, self.__address, self.__conn))
                self.__conn.close()
    
        def __init__(self) -> None:
            Server.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.FileHandler("./logs/ConsensusLayer.log")
            handler.setFormatter(formatter)
            Server.logger.addHandler(handler)
            self.logger.info("ConsensusServer initialization")
            self.__read_config()
            
        def start(self) -> None:
            self.logger.info("ConsensusServer Started")
            thread = Server.RequestBlockchainChunk()
            thread.start()
            self.run()
    
        def run(self) -> None:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((
                    Server.configuration["blockchain"]["consensus"]["ip"],
                    Server.configuration["blockchain"]["consensus"]["port"]
                ))
                sock.listen(3)

                while True:
                    conn, addr = sock.accept()
                    self.logger.info(f"Connection from {addr}")
                    client_thread = Server.ClientThreadConnection(conn, addr)
                    client_thread.start()
            
        
        def __read_config():
            with open(globals.CONFIG_FILE, 'r') as file:
                Server.configuration = yaml.safe_load(file)
    