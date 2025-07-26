let interestedCount = parseInt(localStorage.getItem('interestedCount') || '0');
const countEl = document.getElementById('count');
const messageEl = document.getElementById('message');
const emailSet = new Set();
countEl.textContent = interestedCount;

function animateCount(from, to) {
    const duration = 500;
    const start = performance.now();

    function step(timestamp) {
        const progress = Math.min((timestamp - start) / duration, 1);
        const value = Math.floor(progress * (to - from) + from);
        countEl.textContent = value;
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}

document.getElementById('subscribe').addEventListener('click', () => {
    const email = document.getElementById('email').value.trim();
    const select = document.getElementById('categories');
    const selected = Array.from(select.options)
        .filter(o => o.selected)
        .map(o => o.value);

    if (!email) {
        messageEl.textContent = 'Ingresa un email válido.';
        return;
    }

    if (emailSet.has(email)) {
        messageEl.textContent = '¡Ya te tenemos en cuenta!';
        return;
    }

    emailSet.add(email);
    interestedCount += 1;
    localStorage.setItem('interestedCount', interestedCount);
    const stored = JSON.parse(localStorage.getItem('categories') || '[]');
    stored.push(selected);
    localStorage.setItem('categories', JSON.stringify(stored));
    animateCount(interestedCount - 1, interestedCount);
    messageEl.textContent = '¡Gracias por tu interés! Te avisaremos cuando el producto esté listo.';
});
