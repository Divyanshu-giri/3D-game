// Boss Alert System - Handles boss appearance notifications
class BossAlert {
    constructor() {
        this.alertElement = null;
        this.isActive = false;
        this.currentBoss = null;
    }

    setup() {
        this.createAlertElement();
    }

    createAlertElement() {
        this.alertElement = document.getElementById('boss-alert');
        if (!this.alertElement) {
            this.alertElement = document.createElement('div');
            this.alertElement.id = 'boss-alert';
            this.alertElement.style.position = 'absolute';
            this.alertElement.style.top = '50%';
            this.alertElement.style.left = '50%';
            this.alertElement.style.transform = 'translate(-50%, -50%)';
            this.alertElement.style.color = '#ff4136';
            this.alertElement.style.fontSize = '2.5rem';
            this.alertElement.style.fontWeight = 'bold';
            this.alertElement.style.textAlign = 'center';
            this.alertElement.style.textShadow = '0 0 20px rgba(255, 65, 54, 0.8)';
            this.alertElement.style.zIndex = '20';
            this.alertElement.style.display = 'none';
            
            document.body.appendChild(this.alertElement);
        }
    }

    showBossAlert(bossName, bossType = 'fire') {
        this.currentBoss = bossName;
        this.isActive = true;
        
        // Set alert color based on boss type
        let color, shadowColor;
        switch (bossType) {
            case 'fire':
                color = '#ff4136';
                shadowColor = 'rgba(255, 65, 54, 0.8)';
                break;
            case 'water':
                color = '#0074D9';
                shadowColor = 'rgba(0, 116, 217, 0.8)';
                break;
            case 'wind':
                color = '#7FDBFF';
                shadowColor = 'rgba(127, 219, 255, 0.8)';
                break;
            case 'earth':
                color = '#3D9970';
                shadowColor = 'rgba(61, 153, 112, 0.8)';
                break;
            default:
                color = '#ff4136';
                shadowColor = 'rgba(255, 65, 54, 0.8)';
        }
        
        this.alertElement.style.color = color;
        this.alertElement.style.textShadow = `0 0 20px ${shadowColor}`;
        
        // Show alert with animation
        this.alertElement.textContent = `${bossName.toUpperCase()} APPROACHING!`;
        this.alertElement.style.display = 'block';
        
        // Add animation
        this.alertElement.style.animation = 'bossAlertPulse 2s infinite';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideBossAlert();
        }, 5000);
        
        // Play sound effect (placeholder)
        this.playBossSound();
    }

    hideBossAlert() {
        if (this.isActive) {
            this.alertElement.style.display = 'none';
            this.alertElement.style.animation = '';
            this.isActive = false;
            this.currentBoss = null;
        }
    }

    updateBossStatus(healthPercent) {
        if (this.isActive && this.currentBoss) {
            const status = healthPercent > 70 ? 'DOMINATING' : 
                          healthPercent > 30 ? 'ENGAGED' : 'WEAKENED';
            
            this.alertElement.textContent = `${this.currentBoss.toUpperCase()} - ${status} (${Math.round(healthPercent)}%)`;
        }
    }

    bossDefeated() {
        if (this.isActive && this.currentBoss) {
            this.alertElement.textContent = `${this.currentBoss.toUpperCase()} DEFEATED!`;
            this.alertElement.style.color = '#2ECC40';
            this.alertElement.style.textShadow = '0 0 20px rgba(46, 204, 64, 0.8)';
            
            setTimeout(() => {
                this.hideBossAlert();
            }, 3000);
            
            // Play victory sound
            this.playVictorySound();
        }
    }

    playBossSound() {
        // Placeholder for boss sound effect
        console.log('Playing boss alert sound');
        // In a real implementation, this would play an audio file
        try {
            // const audio = new Audio('assets/sounds/boss_alert.mp3');
            // audio.volume = 0.5;
            // audio.play();
        } catch (error) {
            console.log('Sound playback not available');
        }
    }

    playVictorySound() {
        // Placeholder for victory sound effect
        console.log('Playing victory sound');
        try {
            // const audio = new Audio('assets/sounds/victory.mp3');
            // audio.volume = 0.5;
            // audio.play();
        } catch (error) {
            console.log('Sound playback not available');
        }
    }

    // Add CSS animations for boss alerts
    addAlertStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes bossAlertPulse {
                0%, 100% {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                    text-shadow: 0 0 20px currentColor;
                }
                50% {
                    opacity: 0.7;
                    transform: translate(-50%, -50%) scale(1.1);
                    text-shadow: 0 0 30px currentColor, 0 0 40px currentColor;
                }
            }
            
            @keyframes bossAlertShake {
                0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
                25% { transform: translate(-50%, -50%) rotate(1deg); }
                50% { transform: translate(-50%, -50%) rotate(-1deg); }
                75% { transform: translate(-50%, -50%) rotate(1deg); }
            }
            
            .boss-alert-emergency {
                animation: bossAlertPulse 0.5s infinite, bossAlertShake 0.5s infinite !important;
            }
        `;
        document.head.appendChild(style);
    }

    // Emergency alert for critical boss situations
    showEmergencyAlert(message) {
        this.alertElement.textContent = message;
        this.alertElement.style.color = '#FF4136';
        this.alertElement.classList.add('boss-alert-emergency');
        this.alertElement.style.display = 'block';
        
        setTimeout(() => {
            this.alertElement.classList.remove('boss-alert-emergency');
            this.hideBossAlert();
        }, 3000);
    }

    // Cleanup
    dispose() {
        if (this.alertElement && this.alertElement.parentElement) {
            this.alertElement.parentElement.removeChild(this.alertElement);
        }
    }
}

export { BossAlert };
