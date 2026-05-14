"""
Main chatbot module for the Health Chatbot application.

This module orchestrates the conversation flow by integrating prompt engineering,
safety filtering, and Gemini API communication to provide safe, helpful health information.
"""

import google.genai as genai
from google.genai import types
from config.settings import Config
from .prompt_engineering import PromptEngineer
from .safety_filter import SafetyFilter


class HealthChatbot:
    """
    Main chatbot class for health-related conversations.
    
    This class coordinates the entire conversation pipeline including input validation,
    safety checks, prompt construction, API communication, and response filtering.
    """
    
    def __init__(self):
        """
        Initialize the chatbot with Gemini client and configuration.
        
        Sets up the Gemini model, prompt engineer, safety filter, and conversation history.
        """
        # Initialize Gemini client with API key from environment
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        # Initialize supporting modules
        self.prompt_engineer = PromptEngineer()
        self.safety_filter = SafetyFilter()
        
        # Initialize conversation history
        self.conversation_history = []
    
    def process_message(self, user_message: str) -> dict:
        """
        Process a user message through the complete conversation pipeline.
        
        This method orchestrates the entire flow: input validation, urgency detection,
        prompt construction, API communication, response filtering, and history management.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Dictionary containing:
                - response: The bot's response or error message
                - warning: Any warning messages (urgent situations, sensitive topics, etc.)
                - error: Boolean indicating if an error occurred
        """
        # ==================== Input Validation ====================
        is_valid, validation_message = self.safety_filter.validate_input(user_message)
        if not is_valid:
            return {
                'response': validation_message,
                'warning': '',
                'error': True
            }
        
        # ==================== Urgency Detection ====================
        is_urgent, urgency_warning = self.safety_filter.check_urgency(user_message)
        if is_urgent:
            return {
                'response': urgency_warning,
                'warning': urgency_warning,
                'error': False
            }
        
        # ==================== Sensitive Topic Detection ====================
        sensitive_disclaimer = self.safety_filter.filter_sensitive_content(user_message)
        
        # ==================== Prompt Construction ====================
        system_prompt = self.prompt_engineer.build_system_prompt()
        user_prompt = self.prompt_engineer.build_user_prompt(
            user_message, 
            self.conversation_history
        )
        
        # ==================== API Communication & Response Generation ====================
        try:
            # Generate response using Gemini API
            bot_response = self._generate_response(system_prompt, user_prompt)
            
            # ==================== Response Filtering ====================
            is_safe, filtered_response = self.safety_filter.filter_bot_response(bot_response)
            
            if not is_safe:
                return {
                    'response': filtered_response,
                    'warning': 'Response was filtered for safety concerns.',
                    'error': False
                }
            
            # ==================== History Management ====================
            self._update_history(user_message, bot_response)
            
            return {
                'response': bot_response,
                'warning': sensitive_disclaimer,
                'error': False
            }
            
        except Exception as e:
            # Return user-friendly error message
            return {
                'response': "I apologize, but I'm having trouble connecting right now. Please try again later.",
                'warning': '',
                'error': True
            }
    
    def _generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send query to Gemini model and return response text.
        
        This method handles the actual API call to Google Gemini with proper configuration.
        
        Args:
            system_prompt: The system prompt defining AI behavior and constraints
            user_prompt: The user prompt with conversation context
            
        Returns:
            Generated response text from the model
            
        Raises:
            Exception: If API call fails (handled by caller)
        """
        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Generate response using Gemini API
        response = self.client.models.generate_content(
            model=Config.MODEL_NAME,
            contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
            )
        )
        return response.text
    
    def _update_history(self, user_message: str, bot_response: str):
        """
        Update conversation history with new message exchange.
        
        Appends both user and assistant messages to the history and enforces
        the maximum history length limit to manage memory usage.
        
        Args:
            user_message: The user's message
            bot_response: The bot's response
        """
        # Append user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Append assistant response to history
        self.conversation_history.append({
            'role': 'assistant',
            'content': bot_response
        })
        
        # Enforce maximum history length limit
        if len(self.conversation_history) > Config.MAX_HISTORY_LENGTH:
            # Keep only the most recent messages
            self.conversation_history = self.conversation_history[-Config.MAX_HISTORY_LENGTH:]
    
    def clear_history(self):
        """
        Clear the conversation history.
        
        Resets the conversation history to an empty state, useful for starting
        a new conversation or when requested by the user.
        """
        self.conversation_history = []
