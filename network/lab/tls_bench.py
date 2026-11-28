import csv, socket, ssl, statistics, sys, time
HOST, PORT, N = "127.0.0.1", 4433, 100
host = sys.argv[1] if len(sys.argv) > 1 else HOST
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.load_verify_locations("cert.pem")
ctx.check_hostname = False  # lab only
times = []
version = cipher = None
for _ in range(N):
    t0 = time.perf_counter()
    with socket.create_connection((host, PORT)) as sock:
        with ctx.wrap_socket(sock, server_hostname="localhost") as tls:
            times.append((time.perf_counter() - t0) * 1000)
            tls.sendall(b"ping")
            tls.recv(2)
            version, cipher = tls.version(), tls.cipher()[0]
s = sorted(times)
print(f"TLS version : {version}")
print(f"cipher      : {cipher}")
print(f"handshakes  : {N}")
print(f"median (ms) : {statistics.median(times):.3f}")
print(f"p95 (ms)    : {s[int(0.95 * N) - 1]:.3f}")
with open("tls_baseline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["run", "handshake_ms"])
    for i, t in enumerate(times, 1):
        w.writerow([i, f"{t:.3f}"])
print("saved tls_baseline.csv")
