/**
 * Workflow Store - State Management for Workflows
 */

const STORAGE_KEY = 'autoflow_workflows';

class WorkflowStore {
    constructor() {
        this.workflows = [];
        this.listeners = [];
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                this.workflows = JSON.parse(stored);
            }
        } catch (e) {
            console.error('Failed to load workflows from storage:', e);
            this.workflows = [];
        }
    }

    saveToStorage() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(this.workflows));
        } catch (e) {
            console.error('Failed to save workflows to storage:', e);
        }
    }

    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    notify() {
        this.listeners.forEach(listener => listener(this.workflows));
    }

    getAll() {
        return [...this.workflows];
    }

    getById(id) {
        return this.workflows.find(w => w.id === id);
    }

    create(workflow) {
        const newWorkflow = {
            id: this.generateId(),
            ...workflow,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            status: 'draft',
            executions: 0,
            lastRun: null
        };
        this.workflows.push(newWorkflow);
        this.saveToStorage();
        this.notify();
        return newWorkflow;
    }

    update(id, updates) {
        const index = this.workflows.findIndex(w => w.id === id);
        if (index !== -1) {
            this.workflows[index] = {
                ...this.workflows[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            this.saveToStorage();
            this.notify();
            return this.workflows[index];
        }
        return null;
    }

    delete(id) {
        const index = this.workflows.findIndex(w => w.id === id);
        if (index !== -1) {
            this.workflows.splice(index, 1);
            this.saveToStorage();
            this.notify();
            return true;
        }
        return false;
    }

    updateStatus(id, status) {
        return this.update(id, { status });
    }

    recordExecution(id, result) {
        const workflow = this.getById(id);
        if (workflow) {
            return this.update(id, {
                executions: workflow.executions + 1,
                lastRun: new Date().toISOString(),
                lastResult: result
            });
        }
        return null;
    }

    getStats() {
        return {
            total: this.workflows.length,
            active: this.workflows.filter(w => w.status === 'active').length,
            totalExecutions: this.workflows.reduce((sum, w) => sum + w.executions, 0),
            successRate: this.calculateSuccessRate()
        };
    }

    calculateSuccessRate() {
        const completed = this.workflows.filter(w => w.lastResult);
        if (completed.length === 0) return 100;
        const successful = completed.filter(w => w.lastResult === 'success').length;
        return Math.round((successful / completed.length) * 100);
    }

    generateId() {
        return 'wf_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
    }
}

export const workflowStore = new WorkflowStore();
