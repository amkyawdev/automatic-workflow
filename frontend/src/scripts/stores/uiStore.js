/**
 * UI Store - State Management for UI Components
 */

class UIStore {
    constructor() {
        this.loading = false;
        this.modalOpen = false;
        this.sidebarOpen = true;
        this.theme = 'light';
        this.listeners = [];
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.getState()));
    }

    getState() {
        return {
            loading: this.loading,
            modalOpen: this.modalOpen,
            sidebarOpen: this.sidebarOpen,
            theme: this.theme
        };
    }

    setLoading(loading) {
        this.loading = loading;
        this.notify();
    }

    isLoading() {
        return this.loading;
    }

    setModalOpen(open) {
        this.modalOpen = open;
        this.notify();
    }

    isModalOpen() {
        return this.modalOpen;
    }

    toggleSidebar() {
        this.sidebarOpen = !this.sidebarOpen;
        this.notify();
    }

    setSidebarOpen(open) {
        this.sidebarOpen = open;
        this.notify();
    }

    isSidebarOpen() {
        return this.sidebarOpen;
    }

    setTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        this.notify();
    }

    getTheme() {
        return this.theme;
    }

    toggleTheme() {
        this.setTheme(this.theme === 'light' ? 'dark' : 'light');
    }
}

export const uiStore = new UIStore();
