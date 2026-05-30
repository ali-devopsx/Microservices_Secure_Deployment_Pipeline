/**
 * Dark Mode Toggle - identity/static/js/darkmode.js
 * 
 * This script handles the dark/light mode toggle functionality.
 * 
 * Features:
 * - Toggle button click handler to switch between dark and light modes
 * - Check localStorage for persisted theme preference
 * - Apply/remove 'light-mode' class on body element
 * - CSS variables automatically adapt based on body class selector
 * - Persist user choice in localStorage
 * 
 * Integration:
 * - The HTML navbar contains a theme-toggle button with ID 'themeToggle'
 * - CSS file (style.css) defines color variables for both modes
 * - Body.classList toggle manages the visual theme switching
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    
    // Check if user has a saved theme preference in localStorage
    const savedTheme = localStorage.getItem('theme');
    
    // Apply saved theme or default to dark mode
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        if (themeToggle) {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
    } else {
        document.body.classList.remove('light-mode');
        if (themeToggle) {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
    }
    
    // Add click handler to theme toggle button
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Toggle the light-mode class
            document.body.classList.toggle('light-mode');
            
            // Update localStorage to persist the choice
            if (document.body.classList.contains('light-mode')) {
                localStorage.setItem('theme', 'light');
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                localStorage.setItem('theme', 'dark');
                themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            }
        });
    }
});
