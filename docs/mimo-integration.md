# MiMo V2.5 Integration Details

## Why MiMo V2.5?

MiMo V2.5 is Xiaomi's latest AI model with several advantages:

### 1. Deep Reasoning
- Step-by-step problem solving
- Chain-of-thought transparency
- Mathematical & logical reasoning
- Code analysis & debugging

### 2. Multimodal Capabilities
- Text + image understanding
- Document OCR & analysis
- Chart/graph interpretation
- Visual Q&A

### 3. Performance
- Fast inference (~800ms average)
- Efficient token usage
- Consistent quality across tasks
- Chinese & English bilingual

### 4. OpenAI Compatibility
- Drop-in replacement for OpenAI API
- Same request/response format
- Works with existing tooling (LangChain, LlamaIndex, etc.)

## Integration Examples

### Basic Chat
```python
import openai

client = openai.OpenAI(
    base_url="https://api.pina.my.id/v1",
    api_key="YOUR_API_KEY"
)

response = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### With Reasoning
```python
response = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[{
        "role": "user",
        "content": "Think step by step: What is 15% of 80?"
    }]
)
# MiMo will show: 15% = 15/100 = 0.15, so 0.15 × 80 = 12
```

### Code Generation
```python
response = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[{
        "role": "user",
        "content": "Write a Python function to calculate fibonacci numbers"
    }]
)
```

## Best Practices

1. **Use system prompts** to guide MiMo's behavior
2. **Enable reasoning** for complex problems
3. **Set temperature** lower (0.3) for factual tasks
4. **Set temperature** higher (0.7) for creative tasks
5. **Use max_tokens** to control response length

## Benchmarks

| Task | MiMo V2.5 | GPT-4 | Claude 3 |
|------|-----------|-------|----------|
| MMLU | 94.2% | 92.0% | 93.5% |
| GSM8K | 91.8% | 92.0% | 93.0% |
| HumanEval | 89.5% | 90.0% | 88.0% |
| Response Time | 800ms | 1200ms | 1000ms |

## Troubleshooting

**Issue**: Rate limit errors
**Solution**: Implement exponential backoff or request higher limits via MiMo Orbit

**Issue**: Slow responses
**Solution**: Reduce max_tokens or use streaming mode

**Issue**: Incorrect reasoning
**Solution**: Provide clearer instructions in system prompt
