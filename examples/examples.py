"""
Example usage of RunPodChatModel with LangChain
"""

import os
from dotenv import load_dotenv
from runpod_langchain import RunPodChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def example_basic_usage():
    """Example 1: Basic usage"""
    print("\n" + "="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    llm = RunPodChatModel(
        endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
        api_key=os.getenv("RUNPOD_API_KEY"),
        max_tokens=512,
        temperature=0.7
    )
    
    response = llm.invoke("What is Python programming?")
    print(f"Response: {response.content}")


def example_with_messages():
    """Example 2: Using message types"""
    print("\n" + "="*60)
    print("Example 2: Using Message Types")
    print("="*60)
    
    llm = RunPodChatModel(
        endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
        api_key=os.getenv("RUNPOD_API_KEY")
    )
    
    messages = [
        SystemMessage(content="You are a helpful coding assistant."),
        HumanMessage(content="Explain what a Python decorator is in simple terms.")
    ]
    
    response = llm.invoke(messages)
    print(f"Response: {response.content}")


def example_lcel_chain():
    """Example 3: Using LCEL chains"""
    print("\n" + "="*60)
    print("Example 3: LCEL Chain")
    print("="*60)
    
    llm = RunPodChatModel(
        endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
        api_key=os.getenv("RUNPOD_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that explains technical concepts clearly."),
        ("human", "{topic}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({"topic": "What is REST API?"})
    print(f"Result: {result}")


def example_conversation():
    """Example 4: Multi-turn conversation"""
    print("\n" + "="*60)
    print("Example 4: Multi-turn Conversation")
    print("="*60)
    
    llm = RunPodChatModel(
        endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
        api_key=os.getenv("RUNPOD_API_KEY")
    )
    
    # Build conversation
    conversation = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="My favorite color is blue.")
    ]
    
    # First response
    response1 = llm.invoke(conversation)
    print(f"Assistant: {response1.content}")
    
    # Continue conversation
    conversation.extend([
        response1,
        HumanMessage(content="What's my favorite color?")
    ])
    
    response2 = llm.invoke(conversation)
    print(f"Assistant: {response2.content}")


def example_parameter_override():
    """Example 5: Override parameters"""
    print("\n" + "="*60)
    print("Example 5: Parameter Override")
    print("="*60)
    
    llm = RunPodChatModel(
        endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
        api_key=os.getenv("RUNPOD_API_KEY"),
        max_tokens=100,
        temperature=0.7
    )
    
    # Override for a more creative response
    response = llm.invoke(
        "Write a creative sentence about artificial intelligence.",
        max_tokens=50,
        temperature=1.0
    )
    print(f"Creative response: {response.content}")
    
    # Override for a more deterministic response
    response = llm.invoke(
        "What is 2+2?",
        temperature=0.1
    )
    print(f"Deterministic response: {response.content}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("RunPod LangChain Integration - Examples")
    print("="*60)
    
    # Check environment variables
    if not os.getenv("RUNPOD_ENDPOINT_ID"):
        print("❌ ERROR: RUNPOD_ENDPOINT_ID not set in .env file")
        return
    
    if not os.getenv("RUNPOD_API_KEY"):
        print("❌ ERROR: RUNPOD_API_KEY not set in .env file")
        return
    
    try:
        example_basic_usage()
        example_with_messages()
        example_lcel_chain()
        example_conversation()
        example_parameter_override()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()