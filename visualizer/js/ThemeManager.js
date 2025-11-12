/**
 * Theme Manager - Handles dark/light mode
 */

export class ThemeManager {
    constructor() {
        this.currentTheme = 'light';
        this.storageKey = 'algorithm-visualizer-theme';
    }

    /**
     * Initialize theme from storage or system preference
     */
    init() {
        // Check stored preference
        const storedTheme = localStorage.getItem(this.storageKey);

        if (storedTheme) {
            this.setTheme(storedTheme);
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            this.setTheme('dark');
        }

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem(this.storageKey)) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    /**
     * Toggle between light and dark themes
     */
    toggle() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    /**
     * Set specific theme
     */
    setTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(this.storageKey, theme);

        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }

    /**
     * Get current theme
     */
    getTheme() {
        return this.currentTheme;
    }
}
