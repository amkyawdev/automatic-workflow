/**
 * Main Application Entry Point
 * Automatic Workflow
 */

import { ChatWidget } from '../../components/chat/ChatWidget.js';
import { Toast } from '../../components/common/Toast.js';
import { workflowStore } from '../stores/workflowStore.js';
import { authStore } from '../stores/authStore.js';
import { uiStore } from '../stores/uiStore.js';

class App {
    constructor() {
        this.chatWidget = null;
        this.toastContainer = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initChatWidget();
        this.initStores();
        this.checkAuth();
        console.log('Automatic Workflow initialized');
    }

    setupEventListeners() {
        // Chat toggle button
        const chatToggle = document.getElementById('chat-toggle');
        if (chatToggle) {
            chatToggle.addEventListener('click', () => this.toggleChat());
        }

        // Login button
        const loginBtn = document.getElementById('login-btn');
        if (loginBtn) {
            loginBtn.addEventListener('click', () => this.handleLogin());
        }

        // Modal close buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-close') || 
                e.target.classList.contains('modal-cancel') ||
                e.target.classList.contains('modal-overlay')) {
                this.closeAllModals();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
        });

        // New workflow button
        const newWorkflowBtn = document.getElementById('new-workflow-btn');
        if (newWorkflowBtn) {
            newWorkflowBtn.addEventListener('click', () => this.openWorkflowModal());
        }

        // Connect buttons
        document.querySelectorAll('.connect-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const service = e.target.dataset.service;
                this.openConnectModal(service);
            });
        });
    }

    initChatWidget() {
        const chatWidget = document.getElementById('chat-widget');
        const chatClose = document.getElementById('chat-close');
        
        if (chatWidget) {
            this.chatWidget = new ChatWidget({
                container: chatWidget,
                apiEndpoint: '/api/v1/chat'
            });

            if (chatClose) {
                chatClose.addEventListener('click', () => this.toggleChat());
            }
        }
    }

    initStores() {
        // Initialize stores from localStorage
        workflowStore.loadFromStorage();
        authStore.loadFromStorage();
    }

    checkAuth() {
        const isAuthenticated = authStore.isAuthenticated();
        const loginBtn = document.getElementById('login-btn');
        
        if (isAuthenticated && loginBtn) {
            loginBtn.textContent = 'Dashboard';
            loginBtn.onclick = () => {
                window.location.href = 'dashboard.html';
            };
        }
    }

    toggleChat() {
        if (this.chatWidget) {
            this.chatWidget.toggle();
        }
    }

    handleLogin() {
        // Redirect to login or open auth modal
        window.location.href = 'dashboard.html';
    }

    openWorkflowModal() {
        const modal = document.getElementById('workflow-modal');
        if (modal) {
            modal.classList.remove('hidden');
            uiStore.setModalOpen(true);
        }
    }

    openConnectModal(service) {
        const modal = document.getElementById('connect-modal');
        const title = document.getElementById('modal-title');
        
        if (modal && title) {
            title.textContent = `Connect ${service}`;
            modal.dataset.service = service;
            modal.classList.remove('hidden');
            uiStore.setModalOpen(true);
        }
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.add('hidden');
        });
        uiStore.setModalOpen(false);
    }

    showToast(message, type = 'info') {
        if (!this.toastContainer) {
            this.toastContainer = Toast.createContainer();
            document.body.appendChild(this.toastContainer);
        }
        Toast.show(this.toastContainer, message, type);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

// Export for use in other modules
export { App };
