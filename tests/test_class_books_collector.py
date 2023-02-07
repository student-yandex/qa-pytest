import pytest
from classes.books_collector import BooksCollector


# класс TestBooksCollector содержит набор тестов, которыми мы покрываем BooksCollector
class TestBooksCollector:
    @pytest.mark.parametrize(
        "default_collection", ["Пять строк кода :: Кристиан Клаусен"], indirect=True
    )
    def test_add_new_book_add_two_books(self, default_collection):
        # через параметризованную фикстуру мы создаем объект BooksCollector и добавляем в него книгу
        # с именем из параметра

        # добавляем вторую книгу
        default_collection.add_new_book("Принципы юнит-тестирования :: Хориков Владимир")

        # проверяем, что добавилось именно две книги
        assert len(default_collection.get_books_rating()) == 2

    # Проверка на добавление книги с одинаковым названием
    @pytest.mark.parametrize(
        "default_collection", ["Паттерны объектно-ориентированного проектирования"], indirect=True
    )
    def test_add_new_book_same_name_twice_result_one_name(self, request, default_collection):
        # добавляем вторую книгу с таким же названием, название берем из уже созданной коллекции
        default_collection.add_new_book(next(iter(default_collection.books_rating)))

        assert len(default_collection.get_books_rating()) == 1

    # Проверяем выставление рейтинга книге за пределами допустимых значений (1-10)
    @pytest.mark.parametrize("default_collection", ["Чистый код :: Роберт Мартин"], indirect=True)
    @pytest.mark.parametrize("rating", [-15, 0, 11])
    def test_set_book_rating_set_outside_margins_has_no_effect(self, default_collection, rating):
        # выставляем рейтинг меньше 1
        book_name = next(iter(default_collection.books_rating))
        default_collection.set_book_rating(book_name, rating)

        assert default_collection.get_book_rating(book_name) == 1

    # Проверяем выставление рейтинга книге в допустимых пределах (1-10)
    @pytest.mark.parametrize(
        "default_collection",
        ["Эффективное тестирование программного обеспечения :: Аниче Маурисио"],
        indirect=True,
    )
    @pytest.mark.parametrize("rating", [1, 7, 10])
    def test_set_book_rating_set_inside_margins_has_effect(self, default_collection, rating):
        book_name = next(iter(default_collection.books_rating))
        default_collection.set_book_rating(book_name, rating)

        assert default_collection.get_book_rating(book_name) == rating

    # Проверка на получение рейтинга несуществующей книги
    @pytest.mark.parametrize(
        "default_collection",
        ["Предметно-ориентированное проектирование :: Эрик Эванс"],
        indirect=True,
    )
    def test_get_book_rating_book_non_existent_book_returns_none_rating(self, default_collection):

        assert (
            default_collection.get_book_rating(
                "Python. Разработка на основе тестирования :: Персиваль Гарри"
            )
            is None
        )

    # Тест на добавление книги в избранное
    @pytest.mark.parametrize(
        "default_collection", ["Программируй & типизируй :: Влад Ришкуция"], indirect=True
    )
    def test_add_book_in_favorites_adding_book_name_into_list_of_favorites(
        self, default_collection
    ):
        book_name = next(iter(default_collection.books_rating))
        default_collection.add_book_in_favorites(book_name)

        assert default_collection.get_list_of_favorites_books() == [book_name]

    # Нельзя добавить книгу в избранное, если её нет в словаре books_rating коллекции.
    @pytest.mark.parametrize(
        "default_collection",
        ["Эффективная работа с унаследованным кодом :: Майкл Физерс"],
        indirect=True,
    )
    def test_add_book_in_favorites_adding_unknown_book_has_no_effect(self, default_collection):
        default_collection.add_book_in_favorites("Библия Linux. 10-е издание :: Негус Кристофер")

        assert default_collection.get_list_of_favorites_books() == []

    # Проверка на удаления книги из списка избранных
    @pytest.mark.parametrize(
        "default_collection", ["Шаблоны корпоративных приложений :: Мартин Фаулер"], indirect=True
    )
    def test_delete_book_from_favorites_remove_and_book_from_favorites_returns_empty_list(
        self, default_collection
    ):
        book_name = next(iter(default_collection.books_rating))
        default_collection.add_book_in_favorites(book_name)
        default_collection.delete_book_from_favorites(book_name)

        assert default_collection.get_list_of_favorites_books() == []

    # Тестирования фильтрации книг по рейтингу
    @pytest.mark.parametrize(
        "default_collection",
        ["A Philosophy of Software Design, 2nd edition :: John Ousterhout"],
        indirect=True,
    )
    @pytest.mark.parametrize(
        "books_with_rating",
        [
            [
                ("PostgreSQL 14 изнутри :: Егор Рогов", 7),
                ("Безопасность web-приложений :: Эндрю Хоффман", 3),
                ("Язык программирования Go :: Алан Донован, Брайан Керниган", 5),
                ("Внутри CPYTHON: гид по интерпретатору Python :: Энтони Шоу", 9),
            ]
        ],
    )
    @pytest.mark.parametrize("threshold", [3, 7, 9])
    def test_get_books_with_specific_rating_shows_books_with_rating_above_threshold(
        self, default_collection, books_with_rating, threshold
    ):
        book_name = next(iter(default_collection.books_rating))
        default_collection.set_book_rating(book_name, 3)
        for book_name, book_rating in books_with_rating:
            default_collection.add_new_book(book_name)
            default_collection.set_book_rating(book_name, book_rating)

        assert default_collection.get_books_with_specific_rating(threshold) == [
            book
            for book in default_collection.books_rating
            if default_collection.get_book_rating(book) == threshold
        ]