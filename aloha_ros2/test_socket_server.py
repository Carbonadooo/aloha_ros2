# server.py
import socket

HOST = '0.0.0.0'  # 监听所有网络接口
PORT = 8888

# 创建 TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"[SERVER] Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[SERVER] Received: {data.decode()}")
            conn.sendall(b"Message received by server!")