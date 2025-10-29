document.addEventListener('DOMContentLoaded', () => {
    // Elementos de la UI
    const userList = document.getElementById('userList');
    const bookList = document.getElementById('bookList');
    const loanList = document.getElementById('loanList');

    // Formularios
    const userForm = document.getElementById('userForm');
    const bookForm = document.getElementById('bookForm');
    const createLoanForm = document.getElementById('createLoanForm');

    // Botones
    const loadUsersBtn = document.getElementById('loadUsers');
    const loadBooksBtn = document.getElementById('loadBooks');
    const loadLoansBtn = document.getElementById('loadLoans');

    const API_URLS = {
        users: 'http://localhost:8001/users/',
        books: 'http://localhost:8002/books/',
        loans: 'http://localhost:8000/loans/'
    };

    // --- Funciones CRUD Genéricas ---

    async function fetchData(url, listElement, renderItem) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
            const data = await response.json();
            listElement.innerHTML = '';
            data.forEach(item => listElement.appendChild(renderItem(item)));
        } catch (error) {
            listElement.innerHTML = `<li>Error al cargar los datos: ${error.message}</li>`;
        }
    }

    async function saveData(url, data, method = 'POST') {
        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(JSON.stringify(errorData));
            }
            return await response.json();
        } catch (error) {
            alert(`Error al guardar: ${error.message}`);
            return null;
        }
    }

    async function deleteData(url) {
        try {
            const response = await fetch(url, { method: 'DELETE' });
            if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
            return true;
        } catch (error) {
            alert(`Error al eliminar: ${error.message}`);
            return false;
        }
    }

    // --- Renderizado de Items ---

    function renderUser(user) {
        const li = document.createElement('li');
        li.textContent = `ID: ${user.id}, Nombre: ${user.name}, Email: ${user.email}`;
        
        const editBtn = document.createElement('button');
        editBtn.textContent = 'Editar';
        editBtn.onclick = () => {
            document.getElementById('userId').value = user.id;
            document.getElementById('userName').value = user.name;
            document.getElementById('userEmail').value = user.email;
        };

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Eliminar';
        deleteBtn.onclick = async () => {
            if (confirm(`¿Seguro que quieres eliminar a ${user.name}?`)) {
                if (await deleteData(`${API_URLS.users}${user.id}/`)) {
                    loadUsersBtn.click();
                }
            }
        };

        li.appendChild(editBtn);
        li.appendChild(deleteBtn);
        return li;
    }

    function renderBook(book) {
        const li = document.createElement('li');
        li.textContent = `ID: ${book.id}, Título: ${book.title}, Autor: ${book.author}`;

        const editBtn = document.createElement('button');
        editBtn.textContent = 'Editar';
        editBtn.onclick = () => {
            document.getElementById('bookId').value = book.id;
            document.getElementById('bookTitle').value = book.title;
            document.getElementById('bookAuthor').value = book.author;
        };

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Eliminar';
        deleteBtn.onclick = async () => {
            if (confirm(`¿Seguro que quieres eliminar "${book.title}"?`)) {
                if (await deleteData(`${API_URLS.books}${book.id}/`)) {
                    loadBooksBtn.click();
                }
            }
        };

        li.appendChild(editBtn);
        li.appendChild(deleteBtn);
        return li;
    }

    function renderLoan(loan) {
        const li = document.createElement('li');
        li.textContent = `ID: ${loan.id}, ID Usuario: ${loan.user_id}, ID Libro: ${loan.book_id}, Fecha Préstamo: ${loan.loan_date}, Fecha Devolución: ${loan.return_date || 'No devuelto'}`;
        return li;
    }

    // --- Event Listeners ---

    loadUsersBtn.addEventListener('click', () => fetchData(API_URLS.users, userList, renderUser));
    loadBooksBtn.addEventListener('click', () => fetchData(API_URLS.books, bookList, renderBook));
    loadLoansBtn.addEventListener('click', () => fetchData(API_URLS.loans, loanList, renderLoan));

    userForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('userId').value;
        const data = {
            name: document.getElementById('userName').value,
            email: document.getElementById('userEmail').value
        };
        const url = id ? `${API_URLS.users}${id}/` : API_URLS.users;
        const method = id ? 'PUT' : 'POST';
        
        if (await saveData(url, data, method)) {
            userForm.reset();
            loadUsersBtn.click();
        }
    });

    bookForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('bookId').value;
        const data = {
            title: document.getElementById('bookTitle').value,
            author: document.getElementById('bookAuthor').value
        };
        const url = id ? `${API_URLS.books}${id}/` : API_URLS.books;
        const method = id ? 'PUT' : 'POST';

        if (await saveData(url, data, method)) {
            bookForm.reset();
            loadBooksBtn.click();
        }
    });

    createLoanForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            user_id: parseInt(document.getElementById('loanUserId').value, 10),
            book_id: parseInt(document.getElementById('loanBookId').value, 10)
        };
        if (await saveData(API_URLS.loans, data)) {
            createLoanForm.reset();
            loadLoansBtn.click();
        }
    });
});