import socket
import threading
import time
import json

# from joystick_controller import joystickConroller
from controller.protocol import GCS_CMD, GCS_Packet

import numpy as np
import sounddevice as sd

from core.config import settings
# Client handler thread class for managing an individual connection.
class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, server, timeout=10):
        """
        :param client_socket: The socket object for this client.
        :param client_address: The client's (ip, port) tuple.
        :param server: Reference to the TCPServer instance (to allow removal from active list).
        :param timeout: Maximum seconds allowed with no received data before considering the client inactive.
        """
        super().__init__(daemon=True)
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server
        self.timeout = timeout
        self.last_active = time.time()
        self.active = True

    def run(self):
        print(f"[{self.client_address}] Handler thread started.")
        try:
            while self.active:
                # Set a short timeout on the recv call to allow checking for activity.
                self.client_socket.settimeout(1.0)
                try:
                    data = self.client_socket.recv(1024)
                except socket.timeout:
                    data = None

                if data:
                    # Update the timestamp for last activity.
                    self.last_active = time.time()
                    message = data.decode().strip()
                    print(f"[{self.client_address}] Received: {message}")
                    audio_data = np.frombuffer(b''.join(data), dtype=np.int16)
                    sd.play(audio_data, settings.VOICE_SAMPLE_RATE)
                    sd.wait()  # Wait for playback to finish 

                    # (Optional) Process the message or echo it back:
                    # response = {"cmd":5, "data":None}
                    # self.send(response)
                else:
                    # If no data is received, check for inactivity.
                    if time.time() - self.last_active > self.timeout:
                        print(f"[{self.client_address}] Inactive for more than {self.timeout} seconds.")
                        break
                # Small sleep to prevent busy looping.
                time.sleep(0.1)
        except Exception as e:
            print(f"[{self.client_address}] Exception: {e}")
        finally:
            self.cleanup()

    def send(self, data:dict):
        try:
            self.client_socket.sendall(json.dumps(data).encode())
        except Exception as e:
            print(f"Wrong Dict packet: {data}")

    def cleanup(self):
        self.active = False
        try:
            self.client_socket.close()
        except Exception as e:
            print(f"[{self.client_address}] Error closing socket: {e}")
        # Notify the server that this client is done.
        self.server.remove_client(self.client_address)
        print(f"[{self.client_address}] Connection closed.")

# TCP Server class.
class TCPServer:
    def __init__(self, host='0.0.0.0', port=9000, client_timeout=10):
        """
        :param host: Host interface to bind (default is all interfaces).
        :param port: Port number to listen on.
        :param client_timeout: Inactivity timeout for clients.
        """
        self.host = host
        self.port = port
        self.client_timeout = client_timeout
        self.server_socket = None
        self.clients:dict[ClientHandler] = {}      # Dictionary to store active clients { client_address: ClientHandler }
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        """Starts the TCP server and begins accepting connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of address after server restart.
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        # Set a timeout so that accept() doesn’t block forever.
        self.server_socket.settimeout(1.0)

        print(f"TCPServer listening on {self.host}:{self.port}")

        # Start a monitoring thread (optional) to check overall client health.
        monitor_thread = threading.Thread(target=self.monitor_clients, daemon=True)
        monitor_thread.start()

        while self.running:
            try:
                client_sock, client_addr = self.server_socket.accept()
                print(f"Accepted connection from {client_addr}")
                # Create and start a client handler thread.
                handler = ClientHandler(client_sock, client_addr, self, timeout=self.client_timeout)
                with self.lock:
                    self.clients[client_addr] = handler
                handler.start()
            except socket.timeout:
                continue  # Timeout is used to check the self.running flag periodically.
            except Exception as e:
                print(f"Error accepting connections: {e}")

    def sendData(self, data:dict):
        try:
            with self.lock:
                active_clients = list(self.clients.keys())
                for c in active_clients:
                        client = self.clients.get(c, None)
                        if client:
                            client.send(data)
        except Exception as e:
            print(f"Error in sending data (type: {type(data)}): {data}")

    def remove_client(self, client_address):
        """Remove a client from the active clients list."""
        with self.lock:
            if client_address in self.clients:
                del self.clients[client_address]
                print(f"Removed client: {client_address}")

    def monitor_clients(self):
        """Periodically prints the status of connected clients."""
        while self.running:
            time.sleep(0.2)
            data = joystickController.cmd.model_dump(by_alias=True)
            data = GCS_Packet(cmd=GCS_CMD.JOYSTICK_VAL, data=data)
            with self.lock:
                active_clients = list(self.clients.keys())

            self.sendData(data.model_dump())

            print(f"Active clients: {active_clients}")

    def stop(self):
        """Stop the server and all client threads."""
        self.running = False
        try:
            self.server_socket.close()
        except Exception as e:
            print(f"Error closing server socket: {e}")
        with self.lock:
            for addr, handler in list(self.clients.items()):
                handler.active = False
                try:
                    handler.client_socket.close()
                except Exception as e:
                    print(f"Error closing client {addr} socket: {e}")
        print("TCPServer stopped.")

# Example usage:
if __name__ == "__main__":
    server = TCPServer(host='0.0.0.0', port=9000, client_timeout=10)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server interrupted by user.")
    finally:
        server.stop()
        joystickController.stop()
