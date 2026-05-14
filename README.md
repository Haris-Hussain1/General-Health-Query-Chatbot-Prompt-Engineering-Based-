# Health Chatbot

A production ready web based health assistant chatbot built with Flask and Google Gemini API. The chatbot provides general health information while maintaining strict safety protocols to prevent harmful medical advice.

## Project Overview

The Health Chatbot is an intelligent conversational AI system designed to assist users with general health-related queries. It leverages Google's Gemini API for natural language processing and implements multiple safety layers to ensure responsible AI deployment in healthcare contexts.

## Features

- **Intelligent Conversations**: Natural language processing powered by Google Gemini API
- **Safety Filtering**: Multi-layer safety system to prevent harmful medical advice
- **Prompt Engineering**: Structured prompts ensuring appropriate AI behavior
- **Responsive UI**: Modern, mobile-friendly web interface
- **Conversation History**: Maintains context for multi-turn conversations
- **Urgency Detection**: Identifies emergency situations and directs users to appropriate care
- **Real-time Interaction**: Asynchronous communication without page reloads

## Technologies Used

### Backend
- **Flask 3.0.0**: Python web framework
- **Google Generative AI 0.3.2**: Gemini API integration
- **python-dotenv 1.0.0**: Environment configuration management

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Fetch API for async communication

### Architecture
- **Modular Design**: Separated concerns across multiple modules
- **Configuration Management**: Centralized settings via environment variables
- **Safety Layers**: Input validation, urgency detection, and response filtering

## Architecture

### Project Structure
```
General health chatbot/
├── app/                          # Chatbot logic modules
│   ├── __init__.py
│   ├── chatbot.py               # Main chatbot class with Gemini integration
│   ├── prompt_engineering.py    # System prompt construction
│   └── safety_filter.py         # Input validation and response filtering
├── config/                       # Configuration management
│   ├── __init__.py
│   └── settings.py              # Environment-based settings
├── static/                       # Frontend assets
│   ├── css/
│   │   └── style.css           # Responsive styling
│   └── js/
│       └── chat.js             # Frontend logic
├── templates/                    # HTML templates
│   └── index.html              # Main chat interface
├── .env                         # Environment variables (API keys)
├── main.py                      # Flask application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

### Data Flow
```
User Input → Safety Filter (Input Validation) 
           → Safety Filter (Urgency Check)
           → Prompt Engineering (System & User Prompts)
           → Gemini API (Response Generation)
           → Safety Filter (Response Filtering)
           → User Response
```

### Module Responsibilities

**app/chatbot.py**
- Orchestrates the conversation flow
- Integrates all modules for unified operation
- Manages conversation history
- Handles API communication with Gemini

**app/prompt_engineering.py**
- Constructs system prompts defining AI behavior
- Builds user prompts with conversation context
- Ensures consistent, safe AI responses

**app/safety_filter.py**
- Validates user input for safety concerns
- Detects urgent medical situations
- Filters bot responses for harmful content
- Implements keyword-based safety checks

**config/settings.py**
- Manages environment configuration
- Centralizes API keys and model settings
- Provides configuration for scalability

**main.py**
- Flask application setup
- Route definitions for API endpoints
- Error handling and response formatting

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd "General health chatbot"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Open `.env` file and replace placeholder with your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your_secret_key_here
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`

### API Endpoints

- `GET /` - Renders the main chat interface
- `POST /chat` - Processes chat messages (expects JSON: `{"message": "user text"}`)
- `POST /clear` - Clears conversation history
- `GET /health` - Health check endpoint for monitoring

## Safety Protocols

The chatbot implements multiple safety layers:

1. **Input Validation**: Checks for empty messages and length limits
2. **Urgency Detection**: Identifies emergency medical situations
3. **Sensitive Topic Handling**: Adds disclaimers for sensitive health topics
4. **Response Filtering**: Prevents prescriptions, dosage instructions, and clinical decisions
5. **Prompt Engineering**: System prompts explicitly prohibit harmful medical advice

## Future Improvements

- **Advanced Filtering**: Implement ML-based content filtering for enhanced safety
- **User Authentication**: Add user accounts and personalized health profiles
- **Multi-language Support**: Expand to support multiple languages
- **Database Integration**: Store conversation history for analysis and improvement
- **Medical Knowledge Base**: Integrate verified medical databases for accurate information
- **Voice Interface**: Add speech-to-text and text-to-speech capabilities
- **Mobile Application**: Develop native mobile apps for iOS and Android
- **Analytics Dashboard**: Implement usage analytics and performance monitoring
- **Rate Limiting**: Add API rate limiting for production deployment
- **Caching**: Implement response caching for common queries

## License

This project is developed for educational purposes. Ensure compliance with healthcare AI regulations and guidelines in your jurisdiction before deployment in production environments.

## Disclaimer

This chatbot provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
