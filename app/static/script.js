// Animation scripts for counter effects
document.addEventListener("DOMContentLoaded", () => {
    // We observe mutations because Streamlit rerenders components
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                animateCounters();
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Initial run
    animateCounters();
});

function animateCounters() {
    const counters = document.querySelectorAll('.counter:not(.animated)');
    const speed = 200; // The lower the slower

    counters.forEach(counter => {
        counter.classList.add('animated');
        const updateCount = () => {
            // Check if string contains formatting like Commas or is a float
            const targetStr = counter.getAttribute('data-target');
            if (!targetStr) return;

            const isFloat = targetStr.includes('.');
            const isFormatted = targetStr.includes(',');

            const target = parseFloat(targetStr.replace(/,/g, ''));
            const count = parseFloat(counter.innerText.replace(/,/g, ''));

            if (isNaN(target)) {
                counter.innerText = targetStr;
                return;
            }

            const inc = target / speed;

            if (count < target) {
                let current = count + inc;
                if (isFloat) {
                    current = current.toFixed(2);
                } else {
                    current = Math.ceil(current);
                }

                // Keep intermediate non-formatted to do math right, then format display
                counter.innerText = isFormatted ? Number(current).toLocaleString() : current;
                setTimeout(updateCount, 10);
            } else {
                counter.innerText = targetStr; // Set to exact final string
            }
        };

        // Initialize display to zero if we are targeting a number
        if (!isNaN(parseFloat(counter.getAttribute('data-target')))) {
            counter.innerText = '0';
        }
        updateCount();
    });
}
