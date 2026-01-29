# RunPod LangChain Integration

A custom LangChain chat model for integrating RunPod serverless endpoints with LangChain.

## 🚀 Features

- ✅ Full LangChain `BaseChatModel` compatibility
- ✅ Support for all message types (System, Human, AI)
- ✅ LCEL chain support
- ✅ Parameter customization (temperature, max_tokens, stop sequences)
- ✅ Proper response parsing from RunPod format
- ✅ Multi-turn conversation support

## 📦 Installation (pypi)
```bash
pip install runpod-langchain
```


## 📦 Installation (github)

### Prerequisites

```bash
pip install langchain-core requests python-dotenv
```

### Setup

1. Copy the `runpod_langchain` directory to your project
2. Create a `.env` file with your RunPod credentials:

```env
RUNPOD_ENDPOINT_ID=your-endpoint-id
RUNPOD_API_KEY=your-api-key
```

## 🎯 Usage

### Basic Usage

```python
from runpod_langchain import RunPodChatModel
import os

llm = RunPodChatModel(
    endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
    api_key=os.getenv("RUNPOD_API_KEY"),
    max_tokens=512,
    temperature=0.7
)

response = llm.invoke("What is Python?")
print(response.content)
```

### With Message Types

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is machine learning?")
]

response = llm.invoke(messages)
print(response.content)
```

### LCEL Chains (Recommended)

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"input": "Tell me a joke"})
```

### Multi-turn Conversations

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

conversation = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My name is Alice.")
]

response1 = llm.invoke(conversation)

# Continue conversation
conversation.append(AIMessage(content=response1.content))
conversation.append(HumanMessage(content="What's my name?"))

response2 = llm.invoke(conversation)
```

### Override Parameters

```python
# Override default parameters per request
response = llm.invoke(
    "Write something creative",
    max_tokens=100,
    temperature=1.0
)
```

## 📁 Project Structure

```
runpod_langchain/
├── __init__.py          # Package initialization
├── chat_model.py        # RunPodChatModel implementation
examples.py              # Usage examples
README.md               # This file
```

## 🔧 API Reference

### RunPodChatModel

**Parameters:**
- `endpoint_id` (str): Your RunPod endpoint ID
- `api_key` (str): Your RunPod API key
- `max_tokens` (int, default=512): Maximum tokens to generate
- `temperature` (float, default=0.7): Sampling temperature (0.0-2.0)

**Methods:**
- `invoke(messages, **kwargs)`: Generate a response
- `_generate(messages, stop, run_manager, **kwargs)`: Internal generation method

**Supported kwargs in invoke:**
- `max_tokens`: Override default max tokens
- `temperature`: Override default temperature
- `stop`: List of stop sequences

## 🎓 Examples

Run the examples file:

```bash
python examples.py
```

This will run 5 different examples showing various usage patterns.

## 🔍 How It Works

1. **Message Conversion**: Converts LangChain messages to prompt format
2. **API Call**: Makes POST request to RunPod serverless endpoint
3. **Response Parsing**: Extracts text from RunPod's response format
4. **LangChain Integration**: Returns properly formatted ChatResult

### RunPod Response Format

RunPod typically returns responses in this format:

```python
[{
    'choices': [{
        'tokens': ['token1', 'token2', ...]
    }],
    'usage': {
        'input': 10,
        'output': 50
    }
}]
```

The `RunPodChatModel` automatically parses this and extracts the text.

## 🐛 Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'langchain.chains'`:
- You only need `langchain-core`, not the full `langchain` package
- Use LCEL chains instead of legacy `LLMChain`

### Response Format Issues

If responses look wrong:
- Check that your RunPod endpoint returns the expected format
- Modify `_extract_text()` method if your endpoint uses a different format

### API Errors

If you get 404 or authentication errors:
- Verify your `RUNPOD_ENDPOINT_ID` is correct
- Verify your `RUNPOD_API_KEY` is correct
- Ensure you're using a **serverless endpoint**, not a vLLM pod

## 📝 Notes

- This integration is designed for **RunPod serverless endpoints**
- For vLLM pods, use `ChatOpenAI` instead
- Streaming is not currently supported (serverless endpoints typically don't support it)
- Async methods are not implemented

## 🤝 Contributing

Feel free to extend this implementation with:
- Streaming support (if your endpoint supports it)
- Async methods (`_agenerate`)
- Additional error handling
- Custom response parsers

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [RunPod Documentation](https://docs.runpod.io/)
- [LangChain Custom Chat Models](https://python.langchain.com/docs/modules/model_io/chat/custom_chat_model)
