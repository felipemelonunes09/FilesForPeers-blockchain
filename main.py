import logging
import multiprocessing
from data.server import Server as DataLayerServer
from network import Server as NetworkLayerServer

def start_data_layer():
    server = DataLayerServer()
    server.start()
    
def start_network_layer():
    server = NetworkLayerServer()
    server.start()
    


if __name__ == "__main__":
    process = multiprocessing.Process(target=start_data_layer)
    process.start()
        