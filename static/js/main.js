document.getElementById('search-bar').addEventListener('input', function() {
    const query = this.value;
    fetch(`/search_books?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('book-list');
            bookList.innerHTML = '';
            data.books.forEach(book => {
                const li = document.createElement('li');
                li.innerHTML = `<a href="#">${book.title} by ${book.author}</a>`;
                bookList.appendChild(li);
            });
        });
});
