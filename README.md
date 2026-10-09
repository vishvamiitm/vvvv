# eShopCo Vercel latency metrics API

## Deploy
1. Upload these files to a GitHub repository.
2. Import the repository into https://vercel.com/new
3. Deploy with the default settings.
4. The POST endpoint is `https://YOUR-PROJECT.vercel.app/api/index`.

## Test
POST JSON:
```json
{"regions":["apac","emea"],"threshold_ms":180}
```

The response is keyed by region and contains `avg_latency`, `p95_latency`,
`avg_uptime`, and `breaches`. `breaches` counts latency values strictly
greater than the supplied threshold.

CORS permits requests from any origin for POST and OPTIONS.
