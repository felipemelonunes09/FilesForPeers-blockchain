import logging
import multiprocessing
from data.server import Server as DataLayerServer
from network.server import Server as NetworkLayerServer

def start_data_layer():
    server = DataLayerServer()
    server.start()
    
def start_network_layer():
    server = NetworkLayerServer()
    server.start()
    
if __name__ == "__main__":
    process_data = multiprocessing.Process(target=start_data_layer)
    process_data.start()
    
    process_network = multiprocessing.Process(target=start_network_layer)
    process_network.start()
    
        