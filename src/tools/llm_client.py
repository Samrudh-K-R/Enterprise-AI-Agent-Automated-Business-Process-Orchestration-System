"""
LLM Client for Enterprise Agent.
Handles communication with LLM providers (e.g., OpenAI) and provides mock fallbacks.
"""

import os
from typing import Dict, Any, Optional, List
from loguru import logger

class LLMClient:
    """Client for interacting with Large Language Models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize LLM Client.
        
        Args:
            api_key: API Key for the provider. If None, checks os.environ.
            model: Model identifier.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.use_mock = not self.api_key
        
        if self.use_mock:
            logger.warning("No API key found. Using MOCK LLM mode.")
        else:
            logger.info(f"LLM Client initialized with model: {self.model}")
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                logger.error("OpenAI package not installed. Falling back to mock.")
                self.use_mock = True

    def query(self, prompt: str, system_prompt: str = "You are a helpful enterprise assistant.") -> str:
        """
        Query the LLM.
        
        Args:
            prompt: User prompt.
            system_prompt: System instruction.
            
        Returns:
            LLM response string.
        """
        if self.use_mock:
            return self._mock_response(prompt)
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM query failed: {e}")
            return f"Error: Unable to process request. ({str(e)})"

    def _mock_response(self, prompt: str) -> str:
        """Generate a mock response based on keywords."""
        prompt_lower = prompt.lower()
        
        if "summary" in prompt_lower or "summarize" in prompt_lower:
            return "This is a simulated summary of the provided content. In a real scenario, the LLM would analyze the text and provide a concise overview."
        
        if "email" in prompt_lower:
            return "Subject: Re: Business Inquiry\n\nDear User,\n\nThis is a generated email draft based on your request. It follows professional standards.\n\nBest regards,\nEnterprise Agent"
            
        if "analysis" in prompt_lower or "analyze" in prompt_lower:
            return "Analysis Result:\n1. Key Trend: Positive growth observed.\n2. Risk Factor: Low.\n3. Recommendation: Proceed with the current strategy."
            
        return f"I received your request: '{prompt}'. (Mock Mode: Configure an API key to get real AI responses)"
