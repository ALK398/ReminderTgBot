const notesSearchInput = document.getElementById('notes-search-input');
const remindersSearchInput = document.getElementById('reminders-search-input');

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