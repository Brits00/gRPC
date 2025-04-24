import grpc
from concurrent import futures
import threading
import chat_pb2
import chat_pb2_grpc
import queue

class ChatServer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.clients = []  # Lista de filas de clientes
        self.lock = threading.Lock()

    def ReceiveMessage(self, request_iterator, context):
        client_queue = queue.Queue()

        # Adiciona novo cliente
        with self.lock:
            self.clients.append(client_queue)

        def receive_from_client():
            try:
                for msg in request_iterator:
                    print(f"{msg.sender}: {msg.text}")
                    # Repassa mensagem a todos os clientes conectados
                    with self.lock:
                        for q in self.clients:
                            q.put(msg)
            except:
                pass  # Cliente desconectado ou erro

        recv_thread = threading.Thread(target=receive_from_client, daemon=True)
        recv_thread.start()

        try:
            while True:
                msg = client_queue.get()
                yield msg
        except:
            pass
        finally:
            # Remove cliente da lista
            with self.lock:
                self.clients.remove(client_queue)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
