"""
Flask application entry point for the Health Chatbot.

This module initializes the Flask application, defines API routes,
and manages the chatbot instance lifecycle.
"""

from flask import Flask, render_template, request, jsonify
from config.settings import Config
from app.chatbot import HealthChatbot

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize chatbot instance (singleton pattern)
chatbot = HealthChatbot()


@app.route('/')
def index():
    """
    Render the main chat interface.
    
    Returns:
        Rendered HTML template for the chat interface
    """
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the frontend.
    
    Expects JSON payload with 'message' field.
    Returns JSON response with bot's reply and any warnings.
    
    Returns:
        JSON response containing:
            - response: The bot's response
            - warning: Any warning messages
            - error: Boolean indicating if an error occurred
    """
    print("=== /chat endpoint called ===")
    try:
        # Parse JSON request
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Extract and validate user message
        user_message = data.get('message', '').strip()
        print(f"User message: {user_message}")
        
        if not user_message:
            print("Empty message received")
            return jsonify({
                'response': 'Please enter a message.',
                'warning': '',
                'error': True
            }), 400
        
        print(f"Calling chatbot.process_message...")
        # Process message through chatbot pipeline
        result = chatbot.process_message(user_message)
        print(f"Result from chatbot: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"=== ERROR IN /chat ROUTE ===")
        print(f"Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        # Log error for debugging (in production, use proper logging)
        # For now, return a user-friendly error message
        return jsonify({
            'response': 'An error occurred while processing your message.',
            'warning': '',
            'error': True
        }), 500


@app.route('/clear', methods=['POST'])
def clear():
    """
    Clear the conversation history.
    
    Resets the chatbot's conversation history to start fresh.
    
    Returns:
        JSON response with status indicator
    """
    try:
        chatbot.clear_history()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error'}), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for monitoring.
    
    Used by monitoring systems to verify the application is running.
    
    Returns:
        JSON response with health status
    """
    print("=== /health endpoint called ===")
    return jsonify({'status': 'healthy', 'chatbot_initialized': chatbot is not None})


if __name__ == '__main__':
    """
    Run the Flask development server.
    
    In production, use a WSGI server like Gunicorn or uWSGI instead.
    """
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.FLASK_DEBUG
    )
