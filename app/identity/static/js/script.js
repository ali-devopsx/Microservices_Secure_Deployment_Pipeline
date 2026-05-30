/**
 * JavaScript for Digital Identity Portfolio
 * Features:
 * 1. Typing effect for the name "Ali Mahmoud"
 * 2. Intersection Observer for scroll-triggered fade-in/fade-out animations
 * 3. Smooth scroll interactions
 */

// ===== TYPING EFFECT =====
/**
 * Simulates a continuous looping typing effect for the subtitle in the hero section.
 * Animation cycle: Type characters → Wait → Delete all characters → Wait → Repeat
 * 
 * The text is taken from the 'data-text' attribute of the #typed-subtitle element.
 * Each cycle consists of:
 * 1. Typing phase: Display characters one by one (60-150ms per character)
 * 2. Wait phase: Pause for 2 seconds after typing completes
 * 3. Delete phase: Remove characters one by one (40ms per character)
 * 4. Wait phase: Pause for 1 second before retyping
 * 5. Loop back to step 1
 */
function initTypingEffect() {
    const typedSubtitle = document.getElementById('typed-subtitle');
    if (!typedSubtitle) {
        return;
    }

    const fullText = typedSubtitle.dataset.text || 'IT Linux Engineer | DevOps Engineer | Cybersecurity Analyst';
    let isDeleting = false;
    let currentIndex = 0;

    /**
     * Main typing animation loop
     * Handles both typing and deleting phases with appropriate delays
     */
    function type() {
        // Determine if we should continue typing or start deleting
        if (!isDeleting) {
            // TYPING PHASE: Add characters to the text
            if (currentIndex < fullText.length) {
                typedSubtitle.textContent += fullText[currentIndex];
                currentIndex++;
                const delay = Math.random() * 90 + 60; // Random delay 60-150ms
                setTimeout(type, delay);
            } else {
                // Typing complete, wait before deleting
                isDeleting = true;
                setTimeout(type, 2000); // Wait 2 seconds
            }
        } else {
            // DELETING PHASE: Remove characters from the text
            if (currentIndex > 0) {
                typedSubtitle.textContent = fullText.substring(0, currentIndex - 1);
                currentIndex--;
                const delay = 40; // Consistent 40ms for deletion
                setTimeout(type, delay);
            } else {
                // Deletion complete, prepare to retype
                isDeleting = false;
                setTimeout(type, 1000); // Wait 1 second before retyping
            }
        }
    }

    // Start the typing loop after initial delay
    setTimeout(type, 250);
}

// ===== SCROLL FADE-IN/FADE-OUT ANIMATION =====
/**
 * Uses Intersection Observer API to detect when sections enter/leave the viewport.
 * When a section enters the viewport (scrolling down), it fades in.
 * When a section leaves the viewport (scrolling up), it fades out.
 * This creates a dynamic, scroll-triggered animation effect.
 */
function initScrollFadeEffect() {
    // Get all elements with the 'fade-in' class
    const fadeElements = document.querySelectorAll('.fade-in');

    // Create an Intersection Observer with specific options
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            // Check if the element is currently visible in the viewport
            if (entry.isIntersecting) {
                // Element is in viewport: add 'visible' class to trigger fade-in
                entry.target.classList.add('visible');
            } else {
                // Element is out of viewport: remove 'visible' class to trigger fade-out
                entry.target.classList.remove('visible');
            }
        });
    }, {
        // Observer options
        threshold: 0.1,  // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px'  // Trigger slightly before the element fully enters viewport
    });

    // Start observing each fade-in element
    fadeElements.forEach(element => {
        observer.observe(element);
    });
}

// ===== SMOOTH SCROLL INTERACTION (Optional Enhancement) =====
/**
 * Adds additional interactivity and smooth animations to various elements.
 * This function enhances the user experience with hover effects and transitions.
 */
function initInteractions() {
    // Add click handlers to project cards (optional)
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'scale(1.02)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'scale(1)';
        });
    });

    // Add animations to skill cards
    const skillCards = document.querySelectorAll('.skill-card');
    skillCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Add animations to timeline content
    const timelineContents = document.querySelectorAll('.timeline-content');
    timelineContents.forEach(content => {
        content.addEventListener('mouseenter', () => {
            content.style.transform = 'scale(1.05)';
        });
        content.addEventListener('mouseleave', () => {
            content.style.transform = 'scale(1)';
        });
    });
}

// ===== PAGE INITIALIZATION =====
/**
 * Initialize all effects when the DOM is fully loaded.
 * This ensures all elements are available before we try to interact with them.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize typing effect for the name
    initTypingEffect();

    // Initialize scroll fade-in/fade-out animation
    initScrollFadeEffect();

    // Initialize additional interactions
    initInteractions();

    // Initialize navbar scroll effect
    initNavbarScrollEffect();

    // Initialize smooth scroll for navigation links
    initSmoothScrollLinks();
});

// ===== NAVBAR SCROLL EFFECT =====
/**
 * Add visual feedback to navbar when user scrolls down the page
 * The navbar background becomes more opaque and visible when scrolled
 */
function initNavbarScrollEffect() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ===== SMOOTH SCROLL FOR NAVIGATION LINKS =====
/**
 * Smooth scroll to sections when clicking navbar links
 * Prevents default link behavior and uses smooth scroll API
 */
function initSmoothScrollLinks() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            
            // Only handle hash-only links (e.g., #about, #skills from same page)
            // Let full URLs like /tasks/, /accounts/login/ navigate normally
            if (!href || href.startsWith('http') || href.startsWith('/') || !href.includes('#')) {
                return;
            }
            
            e.preventDefault();
            const targetElement = document.querySelector(href);
            
            if (targetElement) {
                const navHeight = document.querySelector('.navbar').offsetHeight;
                const elementPosition = targetElement.offsetTop - navHeight;
                
                window.scrollTo({
                    top: elementPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const hamburger = document.getElementById('hamburgerBtn');
                const navMenu = document.getElementById('navbarMenu');
                if (hamburger && hamburger.classList.contains('active')) {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                }
            }
        });
    });
}

// ===== UTILITY FUNCTIONS =====

/**
 * Smoothly scroll to a specific element on the page
 * @param {string} elementId - The ID of the element to scroll to
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Get the scroll position as a percentage of the total page height
 * Useful for progress indicators or animations based on scroll depth
 * @returns {number} - Scroll percentage (0-100)
 */
function getScrollPercentage() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    return (scrolled / documentHeight) * 100;
}
