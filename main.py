import time
import logging
import multiprocessing
from data.server import Server as DataLayerServer
from network.server import Server as NetworkLayerServer
from consensus.server import Server as ConsensusServer

def start_data_layer():
    server = DataLayerServer()
    server.start()
    
def start_network_layer():
    server = NetworkLayerServer()
    server.start()
    
def start_consesus_layer():
    server = ConsensusServer()
    server.start()
    
if __name__ == "__main__":
    process_data = multiprocessing.Process(target=start_data_layer)
    process_data.start()
    
    process_network = multiprocessing.Process(target=start_network_layer)
    process_network.start()
    
    time.sleep(2)
    
    process_consensus = multiprocessing.Process(target=start_consesus_layer)
    process_consensus.start()

    
        