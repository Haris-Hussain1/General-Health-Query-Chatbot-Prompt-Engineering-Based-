/**
 * Frontend JavaScript for the Health Chatbot application.
 * 
 * This module handles the chat interface, API communication, and DOM manipulation
 * for a smooth user experience.
 */

// ==================== DOM Element References ====================
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const clearButton = document.getElementById('clear-button');
const chatMessages = document.getElementById('chat-messages');
const warningBanner = document.getElementById('warning-banner');

// ==================== State Management ====================
let isProcessing = false;

// ==================== Event Listeners ====================
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await sendMessage();
});

clearButton.addEventListener('click', () => {
    clearChat();
});

// Allow sending message with Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// ==================== Message Handling ====================
/**
 * Send a message to the chatbot API and handle the response.
 * 
 * This function manages the entire message flow: validation, UI updates,
 * API communication, and error handling.
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    // Validate input and prevent duplicate requests
    if (!message || isProcessing) {
        return;
    }
    
    // Set processing state
    isProcessing = true;
    sendButton.disabled = true;
    
    // Add user message to chat interface
    addMessage(message, 'user');
    userInput.value = '';
    
    // Show typing indicator for better UX
    showTypingIndicator();
    
    try {
        // Send message to backend API
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response to chat interface
        addMessage(data.response, 'bot');
        
        // Display warning if present
        if (data.warning) {
            showWarning(data.warning);
        }
        
    } catch (error) {
        // Handle API errors gracefully
        removeTypingIndicator();
        addMessage('Sorry, there was an error processing your message. Please try again.', 'bot');
    }
    
    // Reset processing state
    isProcessing = false;
    sendButton.disabled = false;
    userInput.focus();
}

/**
 * Parse markdown formatting in text.
 * 
 * @param {string} text - The text to parse
 * @returns {string} - HTML with markdown formatting applied
 */
function parseMarkdown(text) {
    // Escape HTML to prevent XSS
    let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Parse bold text (**text**)
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Parse italic text (*text*)
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Parse bullet points (* item)
    html = html.replace(/^\* (.+)$/gm, '<li>$1</li>');
    
    // Wrap lists
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    // Convert line breaks to <br> (but not inside lists)
    html = html.replace(/\n/g, '<br>');
    
    // Fix line breaks around lists
    html = html.replace(/<br><ul>/g, '<ul>');
    html = html.replace(/<\/ul><br>/g, '</ul>');
    html = html.replace(/<li><br>/g, '<li>');
    html = html.replace(/<br><\/li>/g, '</li>');
    
    return html;
}

/**
 * Add a message to the chat interface.
 * 
 * @param {string} content - The message content
 * @param {string} type - The message type ('user' or 'bot')
 */
function addMessage(content, type) {
    // Create message container
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    // Create content container
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Parse markdown for bot messages
    if (type === 'bot') {
        contentDiv.innerHTML = parseMarkdown(content);
    } else {
        contentDiv.textContent = content;
    }
    
    // Assemble message
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ==================== UI Helpers ====================
/**
 * Display a typing indicator while waiting for bot response.
 */
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;
    
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Remove the typing indicator from the chat interface.
 */
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

/**
 * Display a warning message in the warning banner.
 * 
 * @param {string} message - The warning message to display
 */
function showWarning(message) {
    warningBanner.textContent = message;
    warningBanner.classList.add('show');
    
    // Auto-hide warning after 10 seconds
    setTimeout(() => {
        warningBanner.classList.remove('show');
    }, 10000);
}

// ==================== Chat Management ====================
/**
 * Clear the chat history and reset the interface.
 * 
 * This function calls the backend API to clear conversation history
 * and resets the frontend to its initial state.
 */
async function clearChat() {
    // Prevent clearing while processing a message
    if (isProcessing) {
        return;
    }
    
    try {
        // Clear conversation history on backend
        await fetch('/clear', {
            method: 'POST',
        });
        
        // Reset chat interface to initial state
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    Hello! I'm your health assistant. How can I help you today?
                </div>
            </div>
        `;
        
        // Hide warning banner
        warningBanner.classList.remove('show');
        
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}
