from pydantic import ValidationError, BaseModel
from fastapi import FastAPI, HTTPException

# --- Phase 1: Pydantic on its own -------------------------------------------
#
# Book is a Pydantic model: subclassing BaseModel makes Pydantic check and
# convert the data whenever a Book is created, e.g. Book(title="Dune", ...).
#
# Fields:
#   title        - the book's title (str)
#   author       - the author's name (str)
#   publish_year - the year it was published (int)
#
# NOTE: fields must be declared as `name: type` (a type annotation).
# The fields below use `=` instead of `:`, which stores the type object
# itself as a value. Pydantic v2 raises a PydanticUserError
# ("A non-annotated attribute was detected") when the class is defined.
# Change `=` to `:` on each line to make them real fields.



class Book(BaseModel):
    title: str
    author: str
    publish_year: int


# --- Phase 2: First FastAPI endpoints ---------------------------------------
#
# Tasks:
#   1. Create the app.                                   -> FastAPI()
#   2. Store a few books in an in-memory "database".
#   3. GET /                - return a health message.   -> @app.get()
#   4. GET /books           - return all books.
#   5. GET /books/{book_id} - return one book by its id.
#   6. Return a 404 error when the book doesn't exist.   -> HTTPException
#   7. Run the app and test every endpoint at /docs.


app = FastAPI(
    title= "My First app",
    description=("This handles all the book information"),
    version= "1.0.0"
)


books_db = {
        1: Book(title="Hooville", author="Doctor.Suess", publish_year=1987),
        2: Book(title="Cat In The Hat", author="Doctor Suess", publish_year=1990),
        3: Book(title="Bridge To Terrabitha", author="Kathy Johnson", publish_year=2001)
    }
# Instantiated the db as a global dict
# to have every @app have access to it and recite specific books



@app.get("/") # this goes to root directory
def read_base():
    return{"message": "Hello"}


@app.get("/books")
def read_books():
    # read_book = Book(title="Bridge to Terabithia", author="Samuel Jannet", publish_year=2002)
    # books_db = {
    #     1: Book(title="Hooville", author="Doctor.Suess", publish_year=1987),
    #     2: Book(title="Cat In The Hat", author="Doctor Suess", publish_year=1990),
    #     3: Book(title="Bridge To Terrabitha", author="Kathy Johnson", publish_year=2001)
    # }
    return (list(books_db.values()))

# rather than creating n numbered apps, I managed to make apps up to the keys in the dictionary.


@app.get("/books/{b_id}")
def read_book(b_id: int):
    try:
        return(books_db[b_id])
    except KeyError:
        raise HTTPException(status_code=404, detail="Not the right ID for book.")

    









