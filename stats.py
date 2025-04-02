import pandas as pd

# Анализ жанров
def analyze_genres(books):
    # Делаем табличку из книг
    defo = pd.DataFrame(books)

    # Считает сколько книг с каждого жанра
    genre_counts = defo["genre"].value_counts().to_dict()
    return {"genre_stats": genre_counts}