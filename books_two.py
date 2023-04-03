from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: int,
        published_date: int,
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1980, lt=2024)

    class Config:
        schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codingwithmustansir",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2022,
            }
        }


BOOKS = [
    Book(
        1, "Computer Science Pro", "codingwithmustansir", "A very nice book!", 5, 2020
    ),
    Book(2, "Be Fast with FastAPI", "codingwithmustansir", "A great book!", 5, 2018),
    Book(3, "Master Endpoints", "codingwithmustansir", "An awesome book!", 5, 2018),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2022),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2023),
    Book(6, "HP3", "Author 3", "Book Description", 3, 2018),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """
    Returns all the books
    """
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    """
    Returns a specific book for the provided book id as path parameter
    """
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=-1, lt=6)):
    """
    Returns all books for a given rating in query parameter
    """
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


# Assignment - Create a new GET Request method to filter by published_date
@app.get("/books/filter_by_publish/{published_date}", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Path(gt=1980, lt=2024)):
    """
    Returns all books for a given published_date in path parameter
    """
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    """
    Creates a new book
    """
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book) -> Book:
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    """
    Updates an existing book
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    """
    Deletes a book
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")
