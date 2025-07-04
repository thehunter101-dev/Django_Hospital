// Theme Toggle Functionality
class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem("theme") || "light"
    this.init()
  }

  init() {
    // Set initial theme
    this.applyTheme(this.theme)

    // Add event listener to toggle button
    const toggleButton = document.getElementById("theme-toggle")
    if (toggleButton) {
      toggleButton.addEventListener("click", () => this.toggleTheme())
    }

    // Listen for system theme changes
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
      if (!localStorage.getItem("theme")) {
        this.applyTheme(e.matches ? "dark" : "light")
      }
    })
  }

  toggleTheme() {
    this.theme = this.theme === "light" ? "dark" : "light"
    this.applyTheme(this.theme)
    localStorage.setItem("theme", this.theme)

    // Add a subtle animation to the toggle button
    const toggleButton = document.getElementById("theme-toggle")
    if (toggleButton) {
      toggleButton.style.transform = "scale(0.95)"
      setTimeout(() => {
        toggleButton.style.transform = "scale(1)"
      }, 150)
    }
  }

  applyTheme(theme) {
    const html = document.documentElement

    if (theme === "dark") {
      html.classList.add("dark")
    } else {
      html.classList.remove("dark")
    }

    this.theme = theme
    this.updateIcons()
  }

  updateIcons() {
    const sunIcon = document.getElementById("sun-icon")
    const moonIcon = document.getElementById("moon-icon")

    if (sunIcon && moonIcon) {
      if (this.theme === "dark") {
        sunIcon.style.transform = "rotate(90deg) scale(0)"
        moonIcon.style.transform = "rotate(0deg) scale(1)"
      } else {
        sunIcon.style.transform = "rotate(0deg) scale(1)"
        moonIcon.style.transform = "rotate(90deg) scale(0)"
      }
    }
  }

  // Method to get current theme
  getCurrentTheme() {
    return this.theme
  }

  // Method to set theme programmatically
  setTheme(theme) {
    if (theme === "light" || theme === "dark") {
      this.applyTheme(theme)
      localStorage.setItem("theme", theme)
    }
  }
}

// Initialize theme manager when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.themeManager = new ThemeManager()
})

// Additional utility functions
const ThemeUtils = {
  // Get system preference
  getSystemPreference() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
  },

  // Check if dark mode is active
  isDarkMode() {
    return document.documentElement.classList.contains("dark")
  },

  // Add smooth transitions when theme changes
  addTransitions() {
    const style = document.createElement("style")
    style.textContent = `
            * {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
            }
        `
    document.head.appendChild(style)

    // Remove transitions after animation completes
    setTimeout(() => {
      document.head.removeChild(style)
    }, 300)
  },
}

// Export for use in other scripts if needed
if (typeof module !== "undefined" && module.exports) {
  module.exports = { ThemeManager, ThemeUtils }
}
