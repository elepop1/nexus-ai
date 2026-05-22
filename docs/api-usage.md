# MiMo V2.5 API Usage Guide

## Authentication

All requests require Bearer token authentication:

```bash
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Chat Completions

```bash
curl -X POST https://api.pina.my.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum computing"}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

### With Reasoning

For complex problems, MiMo V2.5 can show step-by-step reasoning:

```bash
curl -X POST https://api.pina.my.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [
      {"role": "user", "content": "Solve step by step: If a train travels at 60km/h for 2.5 hours, how far does it go?"}
    ]
  }'
```

## Response Format

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "mimo-v2.5-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The answer is 150km. Here's the reasoning..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 401 | Invalid API key |
| 429 | Rate limit exceeded |
| 500 | Server error |

## Rate Limits

- Free tier: 60 requests/minute
- With MiMo Orbit credits: Higher limits based on allocation
