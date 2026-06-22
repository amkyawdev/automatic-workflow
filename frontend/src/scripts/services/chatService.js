/**
 * Chat Service - API Client for Chat
 */

const API_CONFIG = {
    baseUrl: '/api/v1'
};

class ChatService {
    constructor() {
        this.baseUrl = API_CONFIG.baseUrl;
    }

    getToken() {
        try {
            const stored = localStorage.getItem('autoflow_auth');
            if (stored) {
                const data = JSON.parse(stored);
                return data.token || '';
            }
        } catch (e) {}
        return '';
    }

    async sendMessage(message, conversationId = null) {
        const token = this.getToken();
        const response = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            },
            body: JSON.stringify({
                message,
                conversation_id: conversationId
            })
        });
        return response;
    }

    async getHistory(limit = 50) {
        const token = this.getToken();
        const response = await fetch(`${this.baseUrl}/chat/history?limit=${limit}`, {
            headers: {
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        });
        return response;
    }

    async getSuggestions() {
        const response = await fetch(`${this.baseUrl}/chat/suggestions`);
        return response;
    }

    async submitFeedback(messageId, helpful) {
        const token = this.getToken();
        const response = await fetch(`${this.baseUrl}/chat/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            },
            body: JSON.stringify({
                message_id: messageId,
                helpful
            })
        });
        return response;
    }
}

export const chatService = new ChatService();
