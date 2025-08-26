// HUD System - Handles health, resources, and other UI elements
class HUD {
    constructor() {
        this.healthElement = null;
        this.resourcesElement = null;
        this.bossHealthElement = null;
        this.healthBar = null;
        this.bossHealthBar = null;
        this.isVisible = true;
    }

    setup() {
        this.createHealthDisplay();
        this.createResourceDisplay();
        this.createBossHealthDisplay();
        this.update(100, 0); // Initial values
    }

    createHealthDisplay() {
        const healthContainer = document.createElement('div');
        healthContainer.className = 'ui-panel';
        healthContainer.innerHTML = `
            <div>Health</div>
            <div class="health-bar">
                <div class="health-fill" style="width: 100%"></div>
            </div>
            <div id="health-value">100</div>
        `;
        
        document.getElementById('ui').appendChild(healthContainer);
        this.healthBar = healthContainer.querySelector('.health-fill');
        this.healthElement = healthContainer.querySelector('#health-value');
    }

    createResourceDisplay() {
        const resourceContainer = document.createElement('div');
        resourceContainer.className = 'ui-panel';
        resourceContainer.innerHTML = `
            <div>Resources</div>
            <div class="resource-counter" id="resources-value">0</div>
        `;
        
        document.getElementById('ui').appendChild(resourceContainer);
        this.resourcesElement = resourceContainer.querySelector('#resources-value');
    }

    createBossHealthDisplay() {
        const bossHealthContainer = document.createElement('div');
        bossHealthContainer.className = 'ui-panel';
        bossHealthContainer.style.display = 'none'; // Hidden by default
        bossHealthContainer.innerHTML = `
            <div>Pyros</div>
            <div class="health-bar">
                <div class="health-fill boss-health-fill" style="width: 100%"></div>
            </div>
            <div id="boss-health-value">100%</div>
        `;
        
        document.getElementById('ui').appendChild(bossHealthContainer);
        this.bossHealthBar = bossHealthContainer.querySelector('.boss-health-fill');
        this.bossHealthElement = bossHealthContainer.querySelector('#boss-health-value');
    }

    update(health, resources) {
        this.updateHealth(health);
        this.updateResources(resources);
    }

    updateHealth(health) {
        const healthPercent = Math.max(0, Math.min(100, health));
        this.healthBar.style.width = `${healthPercent}%`;
        this.healthElement.textContent = Math.round(healthPercent);
        
        // Change color based on health level
        if (healthPercent > 70) {
            this.healthBar.style.background = 'linear-gradient(90deg, #4CAF50, #8BC34A)';
        } else if (healthPercent > 30) {
            this.healthBar.style.background = 'linear-gradient(90deg, #FF9800, #FFC107)';
        } else {
            this.healthBar.style.background = 'linear-gradient(90deg, #F44336, #FF5252)';
        }
    }

    updateResources(resources) {
        this.resourcesElement.textContent = resources.toLocaleString();
        
        // Pulse animation when resources change
        this.resourcesElement.style.animation = 'none';
        setTimeout(() => {
            this.resourcesElement.style.animation = 'pulse 0.5s';
        }, 10);
    }

    showBossHealth(healthPercent) {
        const bossContainer = this.bossHealthBar.parentElement.parentElement;
        bossContainer.style.display = 'block';
        this.updateBossHealth(healthPercent);
    }

    updateBossHealth(healthPercent) {
        const percent = Math.max(0, Math.min(100, healthPercent));
        this.bossHealthBar.style.width = `${percent}%`;
        this.bossHealthElement.textContent = `${Math.round(percent)}%`;
        
        // Boss health bar color (always red-orange for fire boss)
        this.bossHealthBar.style.background = 'linear-gradient(90deg, #ff6b35, #ff4136)';
    }

    hideBossHealth() {
        const bossContainer = this.bossHealthBar.parentElement.parentElement;
        bossContainer.style.display = 'none';
    }

    showMessage(message, duration = 3000) {
        const messageElement = document.createElement('div');
        messageElement.className = 'ui-panel';
        messageElement.style.position = 'absolute';
        messageElement.style.top = '50%';
        messageElement.style.left = '50%';
        messageElement.style.transform = 'translate(-50%, -50%)';
        messageElement.style.zIndex = '20';
        messageElement.style.textAlign = 'center';
        messageElement.textContent = message;
        messageElement.style.animation = 'fadeInOut 2s ease-in-out';
        
        document.getElementById('ui').appendChild(messageElement);
        
        setTimeout(() => {
            if (messageElement.parentElement) {
                messageElement.parentElement.removeChild(messageElement);
            }
        }, duration);
    }

    toggleVisibility() {
        this.isVisible = !this.isVisible;
        document.getElementById('ui').style.display = this.isVisible ? 'block' : 'none';
    }

    // Add CSS animations
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            
            @keyframes fadeInOut {
                0% { opacity: 0; transform: translate(-50%, -60%); }
                20% { opacity: 1; transform: translate(-50%, -50%); }
                80% { opacity: 1; transform: translate(-50%, -50%); }
                100% { opacity: 0; transform: translate(-50%, -40%); }
            }
            
            .boss-health-fill {
                background: linear-gradient(90deg, #ff6b35, #ff4136) !important;
            }
        `;
        document.head.appendChild(style);
    }

    // Cleanup
    dispose() {
        const ui = document.getElementById('ui');
        while (ui.firstChild) {
            ui.removeChild(ui.firstChild);
        }
    }
}

export { HUD };
