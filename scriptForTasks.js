const tasksSearchInput = document.getElementById('tasks-search-input');

tasksSearchInput.addEventListener('input', (event) => {
    const searchText = event.target.value.toLowerCase();

    const tasks = document.querySelectorAll('.tasks-list li');

    tasks.forEach((task) => {
        const taskText = task.textContent.toLowerCase();

        if (taskText.includes(searchText)) {
            task.style.display = 'block';
        } else {
            task.style.display = 'none';
        }
    });
});


const checkbox = document.querySelectorAll('.taskCheckbox');
const taskText = document.querySelectorAll('.taskText');

checkbox.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            checkbox.nextElementSibling.classList.add('crossed');
            checkbox.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.add('crossed');
        } else {
            checkbox.nextElementSibling.classList.remove('crossed');
            checkbox.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.classList.remove('crossed');
        }
    });
});


const tasksUl = document.getElementById('tasks-ul')

tasksUl.addEventListener('click', (e) => {
    if (e.target.id === "mySpan") {
        e.target.parentElement.remove();
    }
})