/**
 * Auth Store - State Management for Authentication
 */

const AUTH_STORAGE_KEY = 'autoflow_auth';

class AuthStore {
    constructor() {
        this.user = null;
        this.token = null;
        this.listeners = [];
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem(AUTH_STORAGE_KEY);
            if (stored) {
                const data = JSON.parse(stored);
                this.token = data.token;
                this.user = data.user;
            }
        } catch (e) {
            console.error('Failed to load auth from storage:', e);
            this.logout();
        }
    }

    saveToStorage() {
        try {
            if (this.token && this.user) {
                localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify({
                    token: this.token,
                    user: this.user
                }));
            } else {
                localStorage.removeItem(AUTH_STORAGE_KEY);
            }
        } catch (e) {
            console.error('Failed to save auth to storage:', e);
        }
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.user, this.token));
    }

    isAuthenticated() {
        return !!this.token && !!this.user;
    }

    getUser() {
        return this.user;
    }

    getToken() {
        return this.token;
    }

    login(token, user) {
        this.token = token;
        this.user = user;
        this.saveToStorage();
        this.notify();
    }

    logout() {
        this.token = null;
        this.user = null;
        this.saveToStorage();
        this.notify();
    }

    updateUser(updates) {
        if (this.user) {
            this.user = { ...this.user, ...updates };
            this.saveToStorage();
            this.notify();
        }
    }

    getPlan() {
        return this.user?.plan || 'free';
    }

    getExecutionsLimit() {
        const limits = {
            free: 100,
            pro: Infinity,
            enterprise: Infinity
        };
        return limits[this.getPlan()] || 100;
    }

    getExecutionsUsed() {
        return this.user?.executionsUsed || 0;
    }

    incrementExecutions() {
        if (this.user) {
            this.user.executionsUsed = (this.user.executionsUsed || 0) + 1;
            this.saveToStorage();
            this.notify();
        }
    }
}

export const authStore = new AuthStore();
