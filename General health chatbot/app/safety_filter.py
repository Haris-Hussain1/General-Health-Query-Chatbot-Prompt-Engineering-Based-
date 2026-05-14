"""
Safety filtering module for the Health Chatbot.

This module provides keyword-based filtering to prevent harmful medical advice
from being delivered to users. It can be extended with advanced filtering mechanisms.
"""

class SafetyFilter:
    """
    Filters and validates user input and bot responses for safety concerns.
    
    This class implements multiple layers of safety checks to ensure the chatbot
    provides safe, informational content without harmful medical advice.
    """
    
    # Keywords that might indicate urgent medical situations
    URGENT_KEYWORDS = [
        'emergency', 'heart attack', 'stroke', 'severe pain', 'bleeding',
        'difficulty breathing', 'unconscious', 'suicide', 'self harm',
        'overdose', 'poison', 'severe burn', 'broken bone', 'seizure'
    ]
    
    # Topics that should be handled with special care and disclaimers
    SENSITIVE_TOPICS = [
        'mental health', 'depression', 'anxiety', 'medication',
        'diagnosis', 'treatment', 'prescription'
    ]
    
    # Keywords that indicate harmful medical advice in bot responses
    HARMFUL_ADVICE_KEYWORDS = [
        'i prescribe', 'here is a prescription', 'you should take',
        'you must take', 'take this medication', 'take this pill',
        'take this tablet', 'take this injection', 'inject this',
        'dosage is', 'the dosage is', 'mg of', 'milligram of'
    ]
    
    @staticmethod
    def check_urgency(user_message: str) -> tuple[bool, str]:
        """
        Check if the message indicates an urgent medical situation.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Tuple of (is_urgent, warning_message)
                - is_urgent: True if urgent situation detected
                - warning_message: Appropriate warning message for urgent situations
        """
        message_lower = user_message.lower()
        
        # Check for urgent keywords
        for keyword in SafetyFilter.URGENT_KEYWORDS:
            if keyword in message_lower:
                return True, (
                    "This appears to be an urgent medical situation. "
                    "Please call emergency services or go to the "
                    "nearest emergency room immediately."
                )
        
        return False, ""
    
    @staticmethod
    def filter_sensitive_content(user_message: str) -> str:
        """
        Add appropriate disclaimers for sensitive health topics.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Disclaimer message if topic is sensitive, empty string otherwise
        """
        message_lower = user_message.lower()
        
        # Check for sensitive topic keywords
        for topic in SafetyFilter.SENSITIVE_TOPICS:
            if topic in message_lower:
                return (
                    "Note: This is a sensitive health topic. "
                    "Please consult a qualified healthcare professional "
                    "for personalized advice."
                )
        
        return ""
    
    @staticmethod
    def validate_input(user_message: str) -> tuple[bool, str]:
        """
        Validate user input for basic safety and format concerns.
        
        Args:
            user_message: The user's input message
            
        Returns:
            Tuple of (is_valid, error_message)
                - is_valid: True if input is valid
                - error_message: Error message if invalid, empty string if valid
        """
        # Check for empty message
        if not user_message or not user_message.strip():
            return False, "Please enter a message."
        
        # Check for message length limit
        if len(user_message) > 2000:
            return False, "Message is too long. Please keep it under 2000 characters."
        
        return True, ""
    
    @staticmethod
    def filter_bot_response(bot_response: str) -> tuple[bool, str]:
        """
        Filter bot responses for potentially harmful medical advice.
        
        This method uses keyword-based filtering to detect and prevent:
        - Drug prescriptions
        - Dosage instructions
        - Clinical decisions
        - Definitive diagnoses
        
        Args:
            bot_response: The bot's generated response
            
        Returns:
            Tuple of (is_safe, filtered_response)
                - is_safe: True if response is safe, False if harmful content detected
                - filtered_response: Original response if safe, warning message if unsafe
        """
        response_lower = bot_response.lower()
        
        # Check for harmful advice keywords
        for keyword in SafetyFilter.HARMFUL_ADVICE_KEYWORDS:
            if keyword in response_lower:
                warning_message = (
                    "I apologize, but I cannot provide specific medical advice, "
                    "prescriptions, or dosage instructions. Please consult a qualified "
                    "healthcare professional for personalized medical guidance."
                )
                return False, warning_message
        
        # Response passed safety checks
        return True, bot_response
