import pytest

from classes.books_collector import BooksCollector


@pytest.fixture(scope="function")
def default_collection(request):
    _collection = BooksCollector()
    _collection.add_new_book(request.param)
    return _collection