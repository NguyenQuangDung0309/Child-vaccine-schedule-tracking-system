import socket
import threading
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 65432

class RPSClient:
    def __init__(self, master):
        self.master = master
        master.title("Rock-Paper-Scissors Client")
        self.result_var = tk.StringVar()
        self.create_widgets()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((HOST, PORT))
            self.result_var.set("Connected to server.")
            threading.Thread(target=self.listen_server, daemon=True).start()
        except Exception as e:
            self.result_var.set(f"Connection error: {e}")

    def create_widgets(self):
        tk.Label(self.master, text="Choose:").pack(pady=10)
        btn_frame = tk.Frame(self.master)
        btn_frame.pack()
        for choice in ["rock", "paper", "scissors"]:
            tk.Button(btn_frame, text=choice.capitalize(), width=10,
                      command=lambda c=choice: self.send_choice(c)).pack(side=tk.LEFT, padx=5)
        tk.Label(self.master, textvariable=self.result_var, fg="blue").pack(pady=20)

    def send_choice(self, choice):
        try:
            self.s.send(choice.encode())
            self.result_var.set(f"Waiting for result...")
        except Exception as e:
            self.result_var.set(f"Send error: {e}")

    def listen_server(self):
        while True:
            try:
                result = self.s.recv(1024).decode()
                print("Received from server:", result)  # Thêm dòng này để debug
                if result:
                    self.result_var.set(result)
                    # Hiển thị popup khi có kết quả
                    if "Result:" in result:
                        res = result.split("Result:")[1].strip()
                        if "Player1 wins" in res or "Player2 loses" in res:
                            messagebox.showinfo("Kết quả", "Player1 thắng!")
                        elif "Player2 wins" in res or "Player1 loses" in res:
                            messagebox.showinfo("Kết quả", "Player2 thắng!")
                        elif "Draw" in res:
                            messagebox.showinfo("Kết quả", "Hai bên hòa!")
            except Exception as e:
                self.result_var.set(f"Disconnected: {e}")
                break

def main():
    root = tk.Tk()
    app = RPSClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()