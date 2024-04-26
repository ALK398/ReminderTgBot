const remSearchInput = document.getElementById('rem-search-input');

remSearchInput.addEventListener('input', (event) => {
    const searchText = event.target.value.toLowerCase();

    const rem = document.querySelectorAll('.rem-list li');

    rem.forEach((rem) => {
        const remText = rem.textContent.toLowerCase();

        if (remText.includes(searchText)) {
            rem.style.display = 'block';
        } else {
            rem.style.display = 'none';
        }
    });
});

const remUl = document.getElementById('rems-ul')

remUl.addEventListener('click', (e) => {
    if (e.target.id === "mySpan") {
        e.target.parentElement.remove();
    }
})