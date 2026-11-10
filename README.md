# Book Library API

A small REST API for browsing a collection of books, built to practice **FastAPI** and **Pydantic**.

Books are stored in memory, so there's no database to set up. Each book is a Pydantic model, which validates its data, and FastAPI serves the books as JSON.

## Features

- List all books
- Get a single book by its id
- Returns `404 Not Found` for a book id that doesn't exist
- Returns `422 Unprocessable Entity` when the id isn't a number (FastAPI does this automatically)
- Interactive API docs at `/docs`, generated automatically

## Endpoints

| Method | Path              | Description                  | Example response                                                          |
|--------|-------------------|------------------------------|---------------------------------------------------------------------------|
| GET    | `/`               | Health check                 | `{"message": "Hello"}`                                                    |
| GET    | `/books`          | List all books               | `[{"title": "Hooville", "author": "Doctor.Suess", "publish_year": 1987}, ...]` |
| GET    | `/books/{b_id}`   | Get one book by its id       | `{"title": "Cat In The Hat", "author": "Doctor Suess", "publish_year": 1990}`  |

A request for an id that doesn't exist (e.g. `/books/99`) returns:

```json
{"detail": "Not the right ID for book."}
```

## Requirements

- [uv](https://docs.astral.sh/uv/), the Python package and project manager
- Python 3.15 or newer (uv can install it for you, see step 2)

## Installation

### 1. Install uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal and check that it worked:
```bash
uv --version
```

### 2. Get the project

Clone the repository (or download and unzip it), then open a terminal in the project folder:

```bash
git clone <repository-url>
cd pydantic_folder
```

### 3. Install Python and the dependencies

```bash
uv sync
```

This reads `pyproject.toml` and `uv.lock`, downloads Python 3.15 if you don't have it, creates a virtual environment in `.venv`, and installs:

- `fastapi[standard]`: the web framework, plus the uvicorn server and the `fastapi` command
- `pydantic`: data validation
- `python-dotenv`: loads settings from a `.env` file

## Running the API

```bash
uv run fastapi dev practice.py
```

The server starts at **http://127.0.0.1:8000** and restarts automatically whenever you save a file. Press `Ctrl+C` to stop it.

To try it out:

- **Interactive docs:** http://127.0.0.1:8000/docs. Expand an endpoint, click **Try it out**, then **Execute**.
- **Alternative docs:** http://127.0.0.1:8000/redoc
- **Directly in the browser:** http://127.0.0.1:8000/books or http://127.0.0.1:8000/books/2

## Project structure

```
pydantic_folder/
├── practice.py          # The API: Book model, in-memory data, and endpoints
├── src/pydantic_folder/ # Package folder (placeholder for now)
├── pyproject.toml       # Project metadata and dependencies
├── uv.lock              # Exact dependency versions (managed by uv)
└── .python-version      # Python version used by uv
```

## How it works

- **`Book` model:** a Pydantic `BaseModel` with `title`, `author` and `publish_year` fields. Pydantic checks the types whenever a `Book` is created.
- **`books_db`:** a dictionary at module level whose keys are the book ids. All endpoints share it. Because it lives in memory, the data resets whenever the server restarts.
- **Path parameters:** in `/books/{b_id}`, FastAPI takes the id from the URL, converts it to an `int`, and passes it to the function.
- **Error handling:** a missing id raises a `KeyError`, which is caught and turned into an `HTTPException` with status 404.

## Roadmap

This project is being built in phases as a learning exercise:

- [x] **Phase 1:** Pydantic model basics
- [x] **Phase 2:** First FastAPI endpoints (`GET`, path parameters, 404 handling)
- [ ] **Phase 3:** Separate input and output models; `POST`, `PATCH` and `DELETE`
- [ ] **Phase 4:** Query parameters (filtering, pagination) and nested models (reviews)
- [ ] **Phase 5:** Configuration with `pydantic-settings` and dependency injection (API key)
- [ ] **Phase 6:** Tests, custom error handlers, and a SQLite database
