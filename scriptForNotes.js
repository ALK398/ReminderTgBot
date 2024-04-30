let login = ''

fetch(`${login}_notes.csv`)
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n').slice(1);

        const notesList = document.getElementById('notes-ul');

        rows.forEach(row => {
        const [name, text] = row.split(',');

        const noteItem = document.createElement('li');
        noteItem.innerHTML = `
                <span class="noteText">${name}</span>
                <p class="noteText">${text}</p>
        `;

        notesList.appendChild(noteItem);

        });
    });

const notesSearchInput = document.getElementById('notes-search-input');

notesSearchInput.addEventListener('input', (event) => {
    const searchText = event.target.value.toLowerCase();

    const notes = document.querySelectorAll('.notes-list li');

    notes.forEach((note) => {
        const noteText = note.textContent.toLowerCase();

        if (noteText.includes(searchText)) {
            note.style.display = 'block';
        } else {
            note.style.display = 'none';
        }
    });
});

const notesUl = document.getElementById('notes-ul')

notesUl.addEventListener('click', (e) => {
    if (e.target.id === "mySpan") {
        e.target.parentElement.remove();
    }
})