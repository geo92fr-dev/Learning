/* =============================================================================
   SYSTÈME DE SÉLECTION DE THÈMES
   Gestion dynamique des palettes de couleurs
   ============================================================================= */

class ThemeManager {
    constructor() {
        this.themes = {
            'default': {
                name: 'Défaut',
                file: 'variables.css',
                icon: '🎨',
                description: 'Palette originale équilibrée'
            },
            'classic': {
                name: 'Classique',
                file: 'variables-classic.css',
                icon: '📚',
                description: 'Style sobre et professionnel'
            },
            'modern': {
                name: 'Moderne',
                file: 'variables-modern.css',
                icon: '✨',
                description: 'Style gaming avec effets visuels'
            }
        };
        
        this.currentTheme = localStorage.getItem('selected-theme') || 'default';
        this.init();
    }
    
    init() {
        this.setupThemeSelector();
        this.loadTheme(this.currentTheme);
        this.setupKeyboardShortcuts();
        this.updateSVGColors();
    }
    
    setupThemeSelector() {
        // Utiliser le select existant dans le header
        const selector = document.getElementById('theme-selector');
        if (!selector) {
            console.warn('Sélecteur de thème introuvable');
            return;
        }
        
        // Configurer la valeur actuelle
        selector.value = this.currentTheme;
        
        selector.addEventListener('change', (e) => {
            const selectedTheme = e.target.value;
            this.switchTheme(selectedTheme);
        });
    }
    
    createToast() {
        const toast = document.createElement('div');
        toast.className = 'theme-toast';
        toast.id = 'theme-toast';
        document.body.appendChild(toast);
    }
    
    setupKeyboardShortcuts() {
        // Écouter les raccourcis clavier
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 't') {
                e.preventDefault();
                this.cycleTheme();
            }
        });
    }
    
    cycleTheme() {
        const themeKeys = Object.keys(this.themes);
        const currentIndex = themeKeys.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % themeKeys.length;
        const nextTheme = themeKeys[nextIndex];
        this.switchTheme(nextTheme);
    }
    
    switchTheme(themeId) {
        if (!this.themes[themeId] || themeId === this.currentTheme) return;
        
        const previousTheme = this.currentTheme;
        this.currentTheme = themeId;
        
        // Sauvegarder le choix
        localStorage.setItem('selected-theme', themeId);
        
        // Charger le nouveau thème
        this.loadTheme(themeId);
        
        // Mettre à jour l'interface
        this.updateActiveOption(themeId);
        
        // Afficher une notification
        this.showToast(previousTheme, themeId);
        
        // Mettre à jour les couleurs SVG si nécessaire
        this.updateSVGColors();
    }
    
    loadTheme(themeId) {
        const theme = this.themes[themeId];
        if (!theme) return;
        
        // Supprimer l'ancien fichier de variables
        const oldLink = document.querySelector('link[href*="variables"]');
        if (oldLink) {
            oldLink.remove();
        }
        
        // Charger le nouveau fichier de variables
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = `styles/${theme.file}`;
        link.setAttribute('data-theme', themeId);
        
        // Insérer avant base.css
        const baseLink = document.querySelector('link[href*="base.css"]');
        if (baseLink) {
            baseLink.parentNode.insertBefore(link, baseLink);
        } else {
            document.head.appendChild(link);
        }
        
        // Ajouter la classe de thème au body pour les styles spécifiques
        document.body.className = document.body.className.replace(/theme-\w+/g, '');
        document.body.classList.add(`theme-${themeId}`);
    }
    
    updateActiveOption(themeId) {
        // Mettre à jour la valeur du select
        const selector = document.getElementById('theme-selector');
        if (selector) {
            selector.value = themeId;
        }
    }
    
    showToast(fromTheme, toTheme) {
        const themeName = this.themes[toTheme]?.name || toTheme;
        const themeIcon = this.themes[toTheme]?.icon || '🎨';
        
        // Simple notification dans la console
        console.log(`Thème changé vers: ${themeIcon} ${themeName}`);
    }
    
    updateSVGColors() {
        // Attendre que les nouvelles variables CSS soient appliquées
        setTimeout(() => {
            const root = document.documentElement;
            const computedStyle = getComputedStyle(root);
            
            // Récupérer les nouvelles couleurs
            const colors = {
                primary: computedStyle.getPropertyValue('--primary').trim(),
                mathPositive: computedStyle.getPropertyValue('--math-positive').trim(),
                mathNegative: computedStyle.getPropertyValue('--math-negative').trim(),
                mathNeutral: computedStyle.getPropertyValue('--math-neutral').trim(),
                mathHighlight: computedStyle.getPropertyValue('--math-highlight').trim()
            };
            
            // Appliquer aux éléments SVG
            document.querySelectorAll('svg line, svg polygon').forEach(el => {
                if (el.getAttribute('stroke') === '#67c7ff' || el.hasAttribute('data-primary')) {
                    el.setAttribute('stroke', colors.primary);
                }
                if (el.getAttribute('fill') === '#67c7ff' || el.hasAttribute('data-primary')) {
                    el.setAttribute('fill', colors.primary);
                }
            });
            
            document.querySelectorAll('svg circle, svg text').forEach(el => {
                const fill = el.getAttribute('fill');
                if (fill === '#ff6b6b' || el.hasAttribute('data-negative')) {
                    el.setAttribute('fill', colors.mathNegative);
                }
                if (fill === '#ff9f43' || el.hasAttribute('data-neutral')) {
                    el.setAttribute('fill', colors.mathNeutral);
                }
                if (fill === '#10ac84' || el.hasAttribute('data-positive')) {
                    el.setAttribute('fill', colors.mathPositive);
                }
                if (fill === '#00d2d3' || el.hasAttribute('data-highlight')) {
                    el.setAttribute('fill', colors.mathHighlight);
                }
            });
        }, 100);
    }
    
    // Méthode publique pour changer de thème depuis l'extérieur
    setTheme(themeId) {
        this.switchTheme(themeId);
    }
    
    // Méthode pour obtenir le thème actuel
    getCurrentTheme() {
        return this.currentTheme;
    }
    
    // Méthode pour obtenir la liste des thèmes disponibles
    getAvailableThemes() {
        return this.themes;
    }
}

// Initialiser le gestionnaire de thèmes
let themeManager;

document.addEventListener('DOMContentLoaded', function() {
    themeManager = new ThemeManager();
    
    // Rendre accessible globalement pour le débogage
    window.themeManager = themeManager;
    
    console.log('🎨 Gestionnaire de thèmes initialisé');
    console.log('💡 Raccourcis : Ctrl+Shift+1/2/3 pour changer de thème');
});

// Export pour utilisation dans d'autres scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}