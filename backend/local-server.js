const http = require("http");
const { handler } = require("./index");

const PORT = process.env.PORT || 3001;

const server = http.createServer(async (req, res) => {
  // Read body
  let bodyChunks = [];
  req.on("data", (chunk) => bodyChunks.push(chunk));
  req.on("end", async () => {
    const rawBody = Buffer.concat(bodyChunks).toString();

    const [pathname, search] = req.url.split("?");
    const queryStringParameters = {};
    if (search) {
      new URLSearchParams(search).forEach((v, k) => {
        queryStringParameters[k] = v;
      });
    }

    // Mock API Gateway Event
    const event = {
      httpMethod: req.method,
      rawPath: pathname,
      path: pathname,
      queryStringParameters,
      headers: req.headers,
      body: rawBody || null,
      requestContext: {
        http: {
          method: req.method,
          path: pathname,
        },
      },
    };

    try {
      const response = await handler(event);
      res.writeHead(response.statusCode, response.headers || {});
      res.end(response.body || "");
    } catch (err) {
      console.error("Local server error:", err);
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: err.message }));
    }
  });
});

server.listen(PORT, () => {
  console.log(`QuizForge Local API Server running at http://localhost:${PORT}`);
  console.log(`- Categories: http://localhost:${PORT}/categories`);
  console.log(`- Health:     http://localhost:${PORT}/health`);
});
