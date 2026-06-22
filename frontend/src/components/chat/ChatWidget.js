/**
 * ChatWidget Component
 */

import { chatStore } from '../../scripts/stores/chatStore.js';
import { chatService } from '../../scripts/services/chatService.js';

export class ChatWidget {
    constructor(options = {}) {
        this.container = options.container;
        this.apiEndpoint = options.apiEndpoint || '/api/v1/chat';
        this.isOpen = false;
        this.messages = [];
        
        this.init();
    }

    init() {
        this.messagesContainer = this.container?.querySelector('#chat-messages');
        this.inputField = this.container?.querySelector('#chat-input');
        this.sendButton = this.container?.querySelector('#chat-send');
        this.suggestionsContainer = this.container?.querySelector('.chat-suggestions');
        
        this.setupEventListeners();
        this.loadMessages();
    }

    setupEventListeners() {
        // Send button
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.sendMessage());
        }

        // Enter to send
        if (this.inputField) {
            this.inputField.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        // Suggestion chips
        if (this.suggestionsContainer) {
            this.suggestionsContainer.querySelectorAll('.suggestion-chip').forEach(chip => {
                chip.addEventListener('click', () => {
                    const text = chip.textContent;
                    if (this.inputField) {
                        this.inputField.value = text;
                        this.sendMessage();
                    }
                });
            });
        }

        // Subscribe to store updates
        chatStore.subscribe((messages) => {
            this.messages = messages;
            this.renderMessages();
        });
    }

    loadMessages() {
        this.messages = chatStore.getAll();
        this.renderMessages();
    }

    toggle() {
        this.isOpen = !this.isOpen;
        if (this.isOpen) {
            this.container?.classList.remove('hidden');
        } else {
            this.container?.classList.add('hidden');
        }
    }

    show() {
        this.isOpen = true;
        this.container?.classList.remove('hidden');
    }

    hide() {
        this.isOpen = false;
        this.container?.classList.add('hidden');
    }

    async sendMessage() {
        const content = this.inputField?.value?.trim();
        if (!content) return;

        // Add user message
        chatStore.addUserMessage(content);
        this.clearInput();

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Call chat API
            const response = await chatService.sendMessage(content);
            this.hideTypingIndicator();
            
            if (response.ok) {
                const data = await response.json();
                chatStore.addBotMessage(data.message);
            } else {
                chatStore.addBotMessage('Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            this.hideTypingIndicator();
            chatStore.addBotMessage('Sorry, I could not connect to the server. Please check your connection.');
        }
    }

    clearInput() {
        if (this.inputField) {
            this.inputField.value = '';
        }
    }

    showTypingIndicator() {
        if (!this.messagesContainer) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot typing';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dots">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        `;
        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typing = this.messagesContainer?.querySelector('#typing-indicator');
        if (typing) {
            typing.remove();
        }
    }

    renderMessages() {
        if (!this.messagesContainer) return;

        this.messagesContainer.innerHTML = this.messages.map(msg => this.renderMessage(msg)).join('');
        this.scrollToBottom();
    }

    renderMessage(message) {
        const time = new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        return `
            <div class="chat-message ${message.role}">
                <div class="message-content">${this.escapeHtml(message.content)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }
}
