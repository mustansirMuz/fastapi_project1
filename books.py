from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/books")
async def read_all_books():
    """
    Returns all the books
    """
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    """
    Returns a specific book matching the provided book title as path parameter
    """
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    """
    Returns all books for a given category in query parameter
    """
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    """
    Returns all books of the given author in path parameter, and category in query parameter
    """
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


@app.post("/books")
async def create_book(new_book=Body()):
    """
    Creates a new book
    """
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    """
    Updates an existing book
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book")
async def delete_book(book_title: str):
    """
    Deletes a book
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# Assignment - Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters.


@app.get("/books/by_author/{author}")
async def read_books_by_author(author: str):
    """
    Returns books of the given author in path parameter
    """
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return
