const http = require("http");
const os = require("os");

const port = Number(process.env.PORT || 3000);
const appVersion = process.env.APP_VERSION || "v1";

const server = http.createServer((req, res) => {
  if (req.url === "/healthz") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok" }));
    return;
  }

  if (req.url === "/") {
    const payload = {
      app: "lab5-nodeapp",
      version: appVersion,
      release: "v3",
      hostname: os.hostname(),
      time: new Date().toISOString()
    };
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(payload));
    return;
  }

  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "not_found" }));
});

server.listen(port, "0.0.0.0", () => {
  console.log(`lab5-nodeapp listening on port ${port} (${appVersion})`);
});

