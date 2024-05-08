import socket
import threading

HOST = "127.0.0.1"
PORT = 8010

created_rooms = {}


def broadcast(client: socket, message: str | bytes, room: str):
    for member in created_rooms[room]:
        if isinstance(message, str):
            message = message.encode()
        member.send(message)


def sendMessage(name: str, room: str, client: socket):
    while True:
        message = client.recv(1024).decode()
        message = f"{name}: {message}"
        broadcast(client, message, room)

        if message == "exit":
            client.close()
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen()

    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send(b"What chat room do you want to join?")
        room = client.recv(1024).decode()

        client.send(b"What is your username?")
        name = client.recv(1024).decode()

        if room not in created_rooms.keys():
            created_rooms[room] = []

        created_rooms[room].append(client)

        message = f"{name} has joined {room} chat room. Total members: {len(created_rooms[room])}"
        broadcast(client, message, room)

        thread = threading.Thread(target=sendMessage, args=(name, room, client))
        thread.start()


if __name__ == "__main__":
    main()
