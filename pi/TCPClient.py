import sys
from Log import Log  
from pi.control import ClientCom 
from connect import run

def main(server_address, server_port, key):
    drone  = run()

    log = Log()
    log.write(["hello from client"])

    # Connect to the server
    try:
        client = ClientCom(server_address, server_port, log, drone)
        client.start()
        print("Connected to server")

        # Send key to server and check for response
        client.send_data(key)
        client.join()  # Wait for the thread to finish

    except Exception as e:
        log.write([f"Error: {str(e)}"])
        print(f"Failed to connect to server: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python tcp_client.py <server address> <server port> <key>")
    else:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
