import mysql.connector

# Функция для подключения к БД
def connect_to_database():
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ur password",
        database="library_db"
    )

    my_cursor = my_db.cursor()
    
    # Таблицу для книг
    my_cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            genre VARCHAR(50),
            # 1 - есть
            # 0 - нет
            is_available INT  
        )
    """)
    
    # Таблица для выдачи 
    my_cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT,
            reader_name VARCHAR(255),
            loan_date VARCHAR(50),
            return_date VARCHAR(50)
        )
    """)
    
    my_db.commit()
    
    return my_db, my_cursor

# Функция для добавления книг
def add_book_to_db(title, author, genre, my_cursor, my_db):
    my_cursor.execute("INSERT INTO books (title, author, genre, is_available) VALUES (%s, %s, %s, %s)", (title, author, genre, 1))
    my_db.commit()
    return {"message": "Книга добавлена!"}

# Функция для выдачи книг
def loan_book_to_reader(book_id, reader_name, loan_date, my_cursor, my_db):
    # Проверка: книга есть?
    my_cursor.execute("SELECT is_available FROM books WHERE book_id = %s", (book_id,))
    result = my_cursor.fetchone()

    if result is None:
        return {"message": "Книга не найдена!"}
    if result[0] == 0:
        return {"message": "Книга уже выдана!"}
    
    # Выдаём книгу
    my_cursor.execute("UPDATE books SET is_available = 0 WHERE book_id = %s", (book_id,))
    my_cursor.execute("INSERT INTO loans (book_id, reader_name, loan_date, return_date) VALUES (%s, %s, %s, %s)", (book_id, reader_name, loan_date, ""))
    my_db.commit()
    
    return {"message": "Книга выдана!"}

# Функция для возврата книг
def return_book_to_library(loan_id, return_date, my_cursor, my_db):
    # Проверка: книга вадавалась?
    my_cursor.execute("SELECT book_id FROM loans WHERE loan_id = %s", (loan_id,))
    result = my_cursor.fetchone()

    if result is None:
        return {"message": "Выдача не найдена!"}
    
    book_id = result[0]

    # Обновляем статус
    my_cursor.execute("UPDATE books SET is_available = 1 WHERE book_id = %s", (book_id,))
    my_cursor.execute("UPDATE loans SET return_date = %s WHERE loan_id = %s", (return_date, loan_id))
    my_db.commit()

    return {"message": "Книга возвращена!"}

# Функция для получения всех книг
def get_all_books(my_cursor):
    my_cursor.execute("SELECT book_id, title, author, genre, is_available FROM books")
    books = my_cursor.fetchall()
    book_list = []

    for book in books:
        book_list.append({
            "book_id": book[0],
            "title": book[1],
            "author": book[2],
            "genre": book[3],
            "is_available": book[4]
        })

    return book_list

# Функция для получения всех выдач
def get_all_loans(my_cursor):
    my_cursor.execute("SELECT loan_id, book_id, reader_name, loan_date, return_date FROM loans")
    loans = my_cursor.fetchall()
    loan_list = []

    for loan in loans:
        loan_list.append({
            "loan_id": loan[0],
            "book_id": loan[1],
            "reader_name": loan[2],
            "loan_date": loan[3],
            "return_date": loan[4]
        })

    return loan_list