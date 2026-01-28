"""
RunPod Chat Model for LangChain

A custom LangChain chat model that integrates with RunPod serverless endpoints.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from typing import List, Optional, Any
from pydantic import Field
import requests


class RunPodChatModel(BaseChatModel):
    """
    Custom LangChain chat model for RunPod serverless endpoints.
    
    This model allows you to use RunPod serverless endpoints with LangChain's
    chat model interface, enabling seamless integration with chains, agents,
    and other LangChain components.
    
    Attributes:
        endpoint_id (str): Your RunPod endpoint ID
        api_key (str): Your RunPod API key
        max_tokens (int): Maximum number of tokens to generate (default: 512)
        temperature (float): Sampling temperature for generation (default: 0.7)
    
    Example:
        >>> from runpod_langchain import RunPodChatModel
        >>> import os
        >>> 
        >>> llm = RunPodChatModel(
        ...     endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
        ...     api_key=os.getenv("RUNPOD_API_KEY"),
        ...     max_tokens=512,
        ...     temperature=0.7
        ... )
        >>> 
        >>> response = llm.invoke("What is Python?")
        >>> print(response.content)
    """
    
    endpoint_id: str = Field(description="RunPod endpoint ID")
    api_key: str = Field(description="RunPod API key")
    max_tokens: int = Field(default=512, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    
    @property
    def _llm_type(self) -> str:
        """Return the type of language model."""
        return "runpod-chat"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Generate a response from the RunPod endpoint.
        
        Args:
            messages: List of messages in the conversation
            stop: Optional list of stop sequences
            run_manager: Optional callback manager
            **kwargs: Additional parameters to override defaults
            
        Returns:
            ChatResult containing the generated response
            
        Raises:
            ValueError: If the API request fails or returns an error
        """
        # Convert messages to prompt format
        prompt = self._messages_to_prompt(messages)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Build input data with parameters
        input_data = {
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
        }
        
        if stop:
            input_data["stop"] = stop
        
        data = {'input': input_data}
        
        try:
            response = requests.post(
                f'https://api.runpod.ai/v2/{self.endpoint_id}/runsync',
                headers=headers,
                json=data,
                timeout=300  # 5 minute timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract the output
            output = result.get('output', str(result))
            
            # Handle potential error responses
            if isinstance(output, dict) and 'error' in output:
                raise ValueError(f"RunPod error: {output['error']}")
            
            # Parse the response format and extract text
            text_content = self._extract_text(output)
            
            message = AIMessage(content=text_content)
            generation = ChatGeneration(message=message)
            
            return ChatResult(generations=[generation])
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request to RunPod failed: {str(e)}")
    
    def _extract_text(self, output: Any) -> str:
        """
        Extract text from RunPod's response format.
        
        RunPod typically returns responses in the format:
        [{'choices': [{'tokens': ['text1', 'text2', ...]}], 'usage': {...}}]
        
        This method handles various response formats and extracts the actual text.
        
        Args:
            output: The output from RunPod API
            
        Returns:
            Extracted text as a string
        """
        try:
            # If output is a list
            if isinstance(output, list) and len(output) > 0:
                first_item = output[0]
                
                # Check if it has 'choices'
                if isinstance(first_item, dict) and 'choices' in first_item:
                    choices = first_item['choices']
                    
                    if isinstance(choices, list) and len(choices) > 0:
                        first_choice = choices[0]
                        
                        # Extract tokens
                        if isinstance(first_choice, dict) and 'tokens' in first_choice:
                            tokens = first_choice['tokens']
                            
                            # Join all tokens into a single string
                            if isinstance(tokens, list):
                                return ''.join(str(token) for token in tokens)
            
            # If we couldn't parse it, return as string
            return str(output)
            
        except Exception as e:
            # Fallback to string representation
            print(f"Warning: Could not parse output format: {e}")
            return str(output)
    
    def _messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        """
        Convert LangChain messages to a prompt string.
        
        Args:
            messages: List of BaseMessage objects
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                prompt_parts.append(f"System: {message.content}")
            elif isinstance(message, HumanMessage):
                prompt_parts.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                prompt_parts.append(f"Assistant: {message.content}")
            else:
                prompt_parts.append(message.content)
        
        return "\n".join(prompt_parts)
    
    @property
    def _identifying_params(self) -> dict:
        """
        Return identifying parameters for the model.
        
        Used for logging and debugging purposes.
        """
        return {
            "endpoint_id": self.endpoint_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }