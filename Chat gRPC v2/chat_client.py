import grpc
import chat_pb2
import chat_pb2_grpc

def generate_messages(sender):
    while True:
        try:
            text = input()
            if text:
                yield chat_pb2.Message(sender=sender, text=text)
        except KeyboardInterrupt:
            break

def receive_messages(stub, sender):
    responses = stub.ReceiveMessage(generate_messages(sender))
    try:
        for msg in responses:
            print(f"{msg.sender}: {msg.text}")
    except grpc.RpcError as e:
        print(f"Erro: {e}")

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatStub(channel)
    sender = input("Digite seu nome: ")
    print("Conectado. Envie mensagens:")
    receive_messages(stub, sender)

if __name__ == '__main__':
    main()
