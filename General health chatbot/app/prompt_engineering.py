"""
Prompt engineering module for the Health Chatbot.

This module constructs and manages prompts to ensure the AI behaves as a safe,
helpful medical assistant that provides informational content only.
"""

class PromptEngineer:
    """
    Handles prompt construction and engineering for the health chatbot.
    
    This class provides structured prompts to ensure the AI behaves as a safe,
    helpful medical assistant that provides informational content only.
    """
    
    # System prompt defining AI behavior and constraints
    SYSTEM_PROMPT = """You are a helpful and friendly medical assistant chatbot. Your role is to provide general health information and guidance to users.

RESPONSE STYLE:
- Keep responses simple, clear, and easy to understand
- Be friendly, empathetic, and supportive in all interactions
- Use plain language - avoid complex medical jargon
- Provide informational content only - not medical advice
- Be concise while being helpful

STRICTLY PROHIBITED:
- NEVER diagnose medical conditions or diseases
- NEVER prescribe medications or recommend specific treatments
- NEVER provide dangerous medical advice that could harm users
- NEVER suggest alternatives to professional medical care
- NEVER make predictions about health outcomes

REQUIRED BEHAVIORS:
- Always recommend consulting a healthcare professional for specific medical concerns
- If a question seems urgent or serious, immediately encourage seeking emergency medical attention
- Focus on preventive care, wellness tips, and general health education
- Provide general information about symptoms, conditions, and treatments for educational purposes
- Include disclaimers when discussing medical topics
- Redirect users to appropriate medical resources when needed

EXAMPLE APPROACH:
Instead of: "You have diabetes, take metformin."
Say: "Diabetes is a condition that affects blood sugar levels. Common treatments include lifestyle changes and medications. Please consult a doctor for proper diagnosis and treatment."

Instead of: "Take this herbal supplement for your headache."
Say: "Some people find relief from headaches through rest, hydration, or over-the-counter pain relievers. For persistent headaches, please see a healthcare provider."""
    
    @staticmethod
    def build_system_prompt() -> str:
        """
        Build and return the system prompt.
        
        Returns:
            The system prompt string that defines AI behavior
        """
        return PromptEngineer.SYSTEM_PROMPT
    
    @staticmethod
    def build_user_prompt(user_message: str, conversation_history: list) -> str:
        """
        Build the user prompt with conversation context.
        
        Args:
            user_message: The current user message
            conversation_history: List of previous message exchanges with 'role' and 'content' keys
            
        Returns:
            Formatted prompt string with conversation context
        """
        # If no history, return just the user message
        if not conversation_history:
            return user_message
        
        # Build conversation context from history
        context_lines = []
        for msg in conversation_history:
            role = 'User' if msg['role'] == 'user' else 'Assistant'
            context_lines.append(f"{role}: {msg['content']}")
        
        context = "\n".join(context_lines)
        
        # Combine context with current message
        return f"{context}\n\nUser: {user_message}"
