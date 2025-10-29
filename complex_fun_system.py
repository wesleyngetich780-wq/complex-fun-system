import threading
import http.server
import socketserver
import time
import random
import json

# ---------- Worker (Background Task) ----------
class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.results = []
        self.running = True

    def run(self):
        while self.running:
            # Simulate doing some computation
            n = random.randint(5, 20)
            matrix = [[random.random() for _ in range(n)] for _ in range(n)]
            total = sum(sum(row) for row in matrix)
            avg = total / (n * n)
            self.results.append({"size": n, "average": avg, "time": time.strftime("%H:%M:%S")})
            time.sleep(2)  # pause between tasks

    def stop(self):
        self.running = False


# ---------- Simple Web Server ----------
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            html = """
            <html>
                <head><title>Complex Fun System</title></head>
                <body style='font-family:sans-serif;'>
                    <h2>Complex Fun System ✅</h2>
                    <p>Refresh to see new computation results.</p>
                    <ul id='results'></ul>
                    <script>
                        async function load() {
                            const res = await fetch('/data');
                            const data = await res.json();
                            let html = '';
                            for (let d of data.slice(-10)) {
                                html += `<li>Time: ${d.time}, Matrix: ${d.size}x${d.size}, Avg: ${d.average.toFixed(4)}</li>`;
                            }
                            document.getElementById('results').innerHTML = html;
                        }
                        load();
                        setInterval(load, 3000);
                    </script>
                </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        elif self.path == "/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(worker.results).encode("utf-8"))
        else:
            self.send_error(404)


# ---------- Main ----------
if __name__ == "__main__":
    PORT = 8000
    worker = Worker()
    worker.start()

    print(f"Server running on http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

    print("Stopping worker...")
    worker.stop()
    worker.join()
    print("Stopped.")

