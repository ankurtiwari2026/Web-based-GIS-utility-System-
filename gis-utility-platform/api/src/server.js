import app from './app.js';

const port = Number(process.env.API_PORT || 8080);

app.listen(port, '0.0.0.0', () => {
  console.log(`[api] listening on port ${port}`);
});

