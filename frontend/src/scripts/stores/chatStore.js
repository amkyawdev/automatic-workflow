/**
 * Chat Store - State Management for Chat Messages
 */

const CHAT_STORAGE_KEY = 'autoflow_chat';

class ChatStore {
    constructor() {
        this.messages = [];
        this.listeners = [];
        this.isTyping = false;
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem(CHAT_STORAGE_KEY);
            if (stored) {
                this.messages = JSON.parse(stored);
            }
        } catch (e) {
            console.error('Failed to load chat from storage:', e);
            this.messages = [];
        }
    }

    saveToStorage() {
        try {
            // Only keep last 50 messages
            const messagesToSave = this.messages.slice(-50);
            localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(messagesToSave));
        } catch (e) {
            console.error('Failed to save chat to storage:', e);
        }
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.messages));
    }

    getAll() {
        return [...this.messages];
    }

    addMessage(message) {
        const newMessage = {
            id: this.generateId(),
            timestamp: new Date().toISOString(),
            ...message
        };
        this.messages.push(newMessage);
        this.saveToStorage();
        this.notify();
        return newMessage;
    }

    addUserMessage(content) {
        return this.addMessage({
            role: 'user',
            content
        });
    }

    addBotMessage(content) {
        return this.addMessage({
            role: 'assistant',
            content
        });
    }

    setTyping(isTyping) {
        this.isTyping = isTyping;
        this.notify();
    }

    getTyping() {
        return this.isTyping;
    }

    clear() {
        this.messages = [];
        this.saveToStorage();
        this.notify();
    }

    generateId() {
        return 'msg_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
    }
}

export const chatStore = new ChatStore();
