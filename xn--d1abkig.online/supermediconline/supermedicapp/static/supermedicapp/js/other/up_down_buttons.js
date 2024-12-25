$(document).ready(function() {
    const upButton = document.getElementById('up-button');
    const downButton = document.getElementById('down-button');
    const scrollAmount = 150;

    function scrollTop() {
        const currentPosition = window.scrollY;
        if (currentPosition > 0) {
            const newPosition = currentPosition - scrollAmount > 0 ? currentPosition - scrollAmount : 0;
            window.scrollBy({ top: -scrollAmount, behavior: 'smooth' });
        }
    }

    function scrollBottom() {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        let currentPosition = window.scrollY;

        if (currentPosition < documentHeight - windowHeight) {
            currentPosition += scrollAmount;
            if (currentPosition > documentHeight - windowHeight) {
                currentPosition = documentHeight - windowHeight;
            }

            window.scrollBy({ top: scrollAmount, behavior: 'smooth' });
        }
    }

    upButton.addEventListener('click', scrollTop);
    downButton.addEventListener('click', scrollBottom);
});
