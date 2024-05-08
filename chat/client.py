import socket
import threading
from tkinter import DISABLED, END, NORMAL, Button, Text, Tk, simpledialog

HOST = "127.0.0.1"
PORT = 8010


class Chat:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        tk = Tk()
        tk.withdraw()
        self.loading = False
        self.is_active = True

        self.name = simpledialog.askstring("Name", "What is your name?", parent=tk)
        self.room = simpledialog.askstring(
            "Room", "What chat room do you want to join?", parent=tk
        )

        thread = threading.Thread(target=self.connect)
        thread.start()

        self.window_chat()

    def window_chat(self):
        self.window = Tk()
        self.window.configure(bg="lightgray")
        self.window.title(f"Chat Room: {self.room}")

        self.message = Text(self.window)
        self.message.config(state=DISABLED)
        self.message.pack(padx=20, pady=20)

        self.input = Text(self.window, height=3)
        self.input.pack(padx=20, pady=20)

        self.send_button = Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(padx=20, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def send_message(self):
        message = self.input.get("1.0", END)
        self.client.send(message.encode())

    def on_closing(self):
        self.is_active = False
        self.window.destroy()
        self.client.close()

    def connect(self):
        while self.is_active:
            received_message = self.client.recv(1024).decode()
            if received_message == "What chat room do you want to join?":
                self.client.send(self.room.encode())
                self.client.send(self.name.encode())
            else:
                try:
                    self.message.config(state=NORMAL)
                    self.message.insert(END, received_message)
                    self.message.config(state=DISABLED)
                except:
                    pass


chat = Chat()
