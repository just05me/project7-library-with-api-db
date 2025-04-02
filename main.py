from fastapi import FastAPI
from datetime import datetime
from database import connect_to_database, add_book_to_db, loan_book_to_reader, return_book_to_library, get_all_books, get_all_loans
from stats import analyze_genres

# API
app = FastAPI()

# Подключаем к БД
my_db, my_cursor = connect_to_database()

# Главная страница
@app.get("/")
def home_page():
    return {"message": "Привет! Это система управления библиотекой!"}

# Добавление
@app.post("/add_book")
def add_book(title: str, author: str, genre: str):
    result = add_book_to_db(title, author, genre, my_cursor, my_db)
    return result

# Выдача
@app.post("/loan_book")
def loan_book(book_id: int, reader_name: str):
    loan_date = datetime.now().strftime("%Y-%m-%d")
    result = loan_book_to_reader(book_id, reader_name, loan_date, my_cursor, my_db)
    return result

# Возврат
@app.post("/return_book")
def return_book(loan_id: int):
    return_date = datetime.now().strftime("%Y-%m-%d")
    result = return_book_to_library(loan_id, return_date, my_cursor, my_db)
    return result

# Все книги
@app.get("/books")
def show_books():
    books = get_all_books(my_cursor)
    return books

# Все выдачи
@app.get("/loans")
def show_loans():
    loans = get_all_loans(my_cursor)
    return loans

# Статистику по жанрам
@app.get("/genre_stats")
def show_genre_stats():
    books = get_all_books(my_cursor)
    stats = analyze_genres(books)
    return stats

