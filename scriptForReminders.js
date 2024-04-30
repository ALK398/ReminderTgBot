let login = ''

fetch(`${login}_reminders.csv`)
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n').slice(1);

        const remsList = document.getElementById('rems-ul');

        rows.forEach(row => {
        const [name, time, text] = row.split(',');

        const remItem = document.createElement('li');
        remItem.innerHTML = `
                <span class="remText">${name}</span>
                <span class="rem-date">${time}</span><br>
                <p class="remText">${text}</p>
        `;

        remsList.appendChild(remItem);

        });
    });

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