/**
 * Notification Store - State Management for Toast Notifications
 */

class NotificationStore {
    constructor() {
        this.notifications = [];
        this.listeners = [];
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.notifications));
    }

    add(notification) {
        const newNotification = {
            id: this.generateId(),
            timestamp: new Date().toISOString(),
            autoDismiss: true,
            duration: 5000,
            ...notification
        };
        this.notifications.push(newNotification);
        this.notify();
        return newNotification.id;
    }

    remove(id) {
        this.notifications = this.notifications.filter(n => n.id !== id);
        this.notify();
    }

    clear() {
        this.notifications = [];
        this.notify();
    }

    success(message, options = {}) {
        return this.add({ type: 'success', message, ...options });
    }

    error(message, options = {}) {
        return this.add({ type: 'error', message, autoDismiss: false, ...options });
    }

    warning(message, options = {}) {
        return this.add({ type: 'warning', message, ...options });
    }

    info(message, options = {}) {
        return this.add({ type: 'info', message, ...options });
    }

    generateId() {
        return 'notif_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
    }
}

export const notificationStore = new NotificationStore();
