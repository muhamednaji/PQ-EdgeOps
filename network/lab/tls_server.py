import socket, ssl, threading
HOST, PORT = "127.0.0.1", 4433
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.load_cert_chain("cert.pem", "key.pem")

def handle(conn):
    try:
        with ctx.wrap_socket(conn, server_side=True) as tls:
            tls.recv(16)
            tls.sendall(b"ok")
    except (ssl.SSLError, OSError):
        pass

with socket.socket() as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(64)
    print(f"TLS server listening on {HOST}:{PORT}")
    while True:
        c, _ = srv.accept()
        threading.Thread(target=handle, args=(c,), daemon=True).start()
