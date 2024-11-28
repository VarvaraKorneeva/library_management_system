import unittest
import os
import json

from library_management_system.system.library_management_system import LibraryManager


class TestLibraryManager(unittest.TestCase):
    def setUp(self) -> None:
        self.test_library_file: str = 'test_library.json'
        self.test_library: list = [{'id': 0,
                                    'title': 'Преступление и наказание',
                                    'author': 'Фёдор Михайлович Достоевский',
                                    'year': 1866,
                                    'status': 'в наличии'},
                                   {'id': 1,
                                    'title': 'Пир во время чумы',
                                    'author': 'Александр Сергеевич Пушкин',
                                    'year': 1830,
                                    'status': 'в наличии'},
                                   {'id': 2,
                                    'title': 'Капитанская дочка',
                                    'author': 'Александр Сергеевич Пушкин',
                                    'year': 1836,
                                    'status': 'в наличии'}]
        with open(self.test_library_file, 'a', encoding='utf-8') as file:
            json.dump({"library": self.test_library}, file, ensure_ascii=False)
        self.library_manager: LibraryManager = LibraryManager(self.test_library_file)

    def tearDown(self) -> None:
        os.remove(self.test_library_file)

    def read_test_library_file(self):
        with open(self.test_library_file, 'r', encoding='utf-8') as file:
            try:
                content: list = json.load(file)['library']
            except json.decoder.JSONDecodeError:
                content: list = []

        return content

    def test_add_book(self) -> None:
        self.assertDictEqual(self.library_manager.add_book('Пиковая дама', 'Александр Сергеевич Пушкин', 2834),
                             {'error': 'Год указан не корректно'})
        not_changed_content = self.read_test_library_file()
        self.assertListEqual(not_changed_content, self.test_library)

        self.assertDictEqual(self.library_manager.add_book('Пиковая дама', '', 1834),
                             {'error': 'Необходимо ввести название и автора книги'})
        not_changed_content = self.read_test_library_file()
        self.assertListEqual(not_changed_content, self.test_library)

        self.assertDictEqual(self.library_manager.add_book('Пиковая дама', 'Александр Сергеевич Пушкин', 1834),
                             {'massage': 'Книга успешно добавлена'})
        changed_content: list = self.read_test_library_file()
        expected_content: list = self.test_library + [{'id': 3,
                                                       'title': 'Пиковая дама',
                                                       'author': 'Александр Сергеевич Пушкин',
                                                       'year': 1834,
                                                       'status': 'в наличии'}]
        self.assertListEqual(changed_content, expected_content)

    def test_delete_book(self) -> None:
        self.assertDictEqual(self.library_manager.delete_book(100),
                             {'error': 'Книги с данным id не существует'})
        not_changed_content = self.read_test_library_file()
        self.assertListEqual(not_changed_content, self.test_library)

        self.assertDictEqual(self.library_manager.delete_book(0),
                             {'massage': 'Книга удалена из библиотеки'})
        changed_content = self.read_test_library_file()
        self.assertListEqual(changed_content, self.test_library[1:])

    def test_change_book_status(self) -> None:
        self.assertDictEqual(self.library_manager.change_book_status(0, 'нет в наличии'),
                             {'error': 'Не корректный статус книги'})
        not_changed_content = self.read_test_library_file()
        self.assertEqual(not_changed_content[0]['status'], 'в наличии')

        self.assertDictEqual(self.library_manager.change_book_status(100, 'выдана'),
                             {'error': 'Книги с данным id не существует'})

        self.assertDictEqual(self.library_manager.change_book_status(0, 'выдана'),
                             {'massage': 'Статус успешно изменен'})
        changed_content = self.read_test_library_file()
        self.assertEqual(changed_content[0]['status'], 'выдана')

    def test_display_all_books(self) -> None:
        result_display_all_books: list = [book.__dict__ for book in self.library_manager.display_all_books()]
        self.assertListEqual(result_display_all_books, self.test_library)

    def test_find_book(self) -> None:
        result_find_book: list = [
            book.__dict__ for book in self.library_manager.find_book('Александр Сергеевич Пушкин')
        ]
        self.assertListEqual(result_find_book, self.test_library[1:])

        result_find_book_by_year: list = [
            book.__dict__ for book in self.library_manager.find_book('1830')
        ]
        self.assertListEqual(result_find_book_by_year, self.test_library[1:2])

        result_find_book_by_non_exist_year: list = self.library_manager.find_book('3000')
        self.assertListEqual(result_find_book_by_non_exist_year, [])


if __name__ == '__main__':
    unittest.main()
