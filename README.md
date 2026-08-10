# POV - AI Fashion Intelligence Platform (MVP)

This is the backend prototype for POV, an AI fashion intelligence platform that translates clothing sizes between different fashion brands.

## Tech Stack
*   **FastAPI**: Web framework for building APIs.
*   **Supabase PostgreSQL**: Database for storing brands, categories, mappings, and feedback.
*   **SQLAlchemy**: ORM for database interactions.

## Setup Instructions

### 1. Supabase Setup
1.  Go to [Supabase](https://supabase.com/) and create a new project.
2.  Go to **Project Settings** -> **Database**.
3.  Under **Connection string**, select **URI**.
4.  It will look like `postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres`.

### 2. Local Environment Setup
1.  Clone this repository or navigate to the project directory.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Copy `.env.example` to `.env` and paste your Supabase connection string.
    ```bash
    cp .env.example .env
    ```

### 3. Running the App and Seeding Data
1.  Start the FastAPI server. On startup, it will automatically create the necessary database tables in Supabase.
    ```bash
    uvicorn app.main:app --reload
    ```
2.  Open another terminal window (with the virtual environment activated).
3.  Run the initialization script to populate the database with manual demo data:
    ```bash
    python -m app.utils.init_db
    ```

## API Documentation
Once the server is running, you can access the interactive API documentation (Swagger UI) at:
*   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can use the `/recommend-size` endpoint to test the size mapping intelligence.
