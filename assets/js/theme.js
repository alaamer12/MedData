document.addEventListener('DOMContentLoaded', () => {
    const themeSwitcher = document.querySelector('.theme-switcher-button');
    const html = document.documentElement;

    const setTheme = (theme) => {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    };

    const toggleTheme = () => {
        const currentTheme = html.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    };

    themeSwitcher.addEventListener('click', toggleTheme);

    // Apply saved theme on load
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
});
