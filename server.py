import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

clients = []
choices = {}

def handle_client(conn, addr):
    print(f"Client {addr} connected.")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            choices[addr] = data
            if len(choices) == 2:
                addr1, addr2 = list(choices.keys())
                choice1, choice2 = choices[addr1], choices[addr2]
                result1, result2 = get_result(choice1, choice2)
                # Gửi kết quả cho từng client với Player1/Player2
                msg1 = f"Player1: {choice1}, Player2: {choice2}, Result: {result1}"
                msg2 = f"Player1: {choice1}, Player2: {choice2}, Result: {result2}"
                clients[0].send(msg1.encode())
                clients[1].send(msg2.encode())
                choices.clear()
        except:
            break
    conn.close()

def get_result(choice1, choice2):
    if choice1 == choice2:
        return ("Draw", "Draw")
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    if wins[choice1] == choice2:
        return ("Player1 wins", "Player2 loses")
    else:
        return ("Player1 loses", "Player2 wins")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server started, waiting for players...")
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()