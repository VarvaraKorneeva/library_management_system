import json
from datetime import datetime


class Book:
    """
    Класс Book используется для создания экземпляров книг, которые храняться в библиотеке.

    Attributes:
    id: int -- уникальный идентификатор книги
    title: str -- название книги
    author: str -- автор книги
    year: int -- год издания книги
    status: str -- статус книги: 'в наличии' или 'выдана' (default 'в наличии')
    """

    def __init__(self, id: int, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status


class LibraryManager:
    """
    Класс LibraryManager осуществляет взаимодейсвие со списком книг, хранящимся в файле library.json.

    Attributes:
    library_file: str -- название файла, в котором храниться список книг (default 'library.json')
    library: list[Book] -- список всех книг, представленных как экземпляры класса Book
    """

    def __init__(self, library_file: str = 'library.json') -> None:
        self.library_file: str = library_file
        self.library: list = self.read_library()

    def read_library(self) -> list[Book]:
        """
        Метод читает данные из файла библиотеки и формирует из них список экземпляров класса Book.
        В случае если файл пуст, возврощается пустой список.

        :return: list[Book] -- список всех книг
        """

        with open(self.library_file, 'r', encoding='utf-8') as file:
            try:
                data: dict = json.load(file)
                books: list = [Book(**data['library'][i]) for i in range(len(data['library']))]
            except json.decoder.JSONDecodeError:
                books: list = []

        return books

    def write_library(self) -> None:
        """
        Метод записывает данные о книгах в файл библиотеки.

        :return: None
        """

        with open(self.library_file, 'w', encoding='utf-8') as file:
            json.dump({"library": [book.__dict__ for book in self.library]}, file, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> dict:
        """
        Метод добавляет новую книгу с указанными названием, автором и годом издания.
        В случае если указанный год больше текущего возвращается сообщение с ошибкой.
        Если не указано название или автор также возвращается сообщение с ошибкой.

        :param title: str -- название книги
        :param author: str -- автор книги
        :param year: int -- год издания книги
        :return: dict -- сообщение с результатом выполнения
        """

        if year > datetime.now().year:
            return {'error': 'Год указан не корректно'}

        if not title or not author:
            return {'error': 'Необходимо ввести название и автора книги'}

        new_id: int = self.get_new_book_id()
        new_book: Book = Book(new_id, title, author, year)
        self.library.append(new_book)
        self.write_library()

        return {'massage': 'Книга успешно добавлена'}

    def get_new_book_id(self) -> int:
        """
        Метод определяет последний использованный id и увеличивает его на 1 для формирования нового.

        :return: int -- новый id
        """

        if self.library:
            last_id: int = self.library[-1].id
            return last_id + 1
        return 0

    def delete_book(self, id_: int) -> dict:
        """
        Метод удаляет книгу из библиотеки по указанному id.
        Если книга с указанным id не была найдена возврощает сообщение с ошибкой.

        :param id_: int -- id книги, которую нужно удалить
        :return: dict -- сообщение с результатом выполнения
        """

        for book in self.library:
            if book.id == id_:
                self.library.remove(book)
                self.write_library()
                return {'massage': 'Книга удалена из библиотеки'}

        return {'error': 'Книги с данным id не существует'}

    def find_book(self, attribute_to_find: str) -> list[Book]:
        """
        Метод возврощает список книг с соответствующим названием, автором или годом издания.

        :param attribute_to_find: str -- строка, по которой будет осуществляться поиск
        :return: list[Book] -- список книг отвечающих запросу
        """

        found_books: list = []
        for book in self.library:
            if attribute_to_find == book.title or attribute_to_find == book.author:
                found_books.append(book)
        try:
            year_to_find: int = int(attribute_to_find)
            for book in self.library:
                if year_to_find == book.year:
                    found_books.append(book)
        except ValueError:
            pass

        return found_books

    def display_all_books(self) -> list[Book]:
        """
        Метод возврощает список свех книг в библиотеке.

        :return: list[Book] -- список всех книг
        """

        return self.library

    def change_book_status(self, id_: int, new_status: str) -> dict:
        """
        Метод изменяет статус книги по указанному id на новый статус.
        В случае если новый статус не соответствует возможным вариантам статуса возврощается сообщение об ошибке.
        Если книга с указанным id не была найдена возврощается сообщение о том, что книги с данным id не существует.

        :param id_: int -- id книги, у которой нужно изменить статус
        :param new_status: str -- новый статус
        :return: dict -- сообщение с результатом выполнения
        """

        if new_status != 'в наличии' and new_status != 'выдана':
            return {'error': 'Не корректный статус книги'}

        for book in self.library:
            if book.id == id_:
                book.status = new_status
                self.write_library()
                return {'massage': 'Статус успешно изменен'}

        return {'error': 'Книги с данным id не существует'}


class LibraryManagementSystem:
    """
    Класс LibraryManagementSystem осуществляет взаимодейсвие пользователя и библиотеки.

    Attributes:
    library_manager: LibraryManager -- экземпляр класса LibraryManager
    """

    def __init__(self) -> None:
        self.library_manager: LibraryManager = LibraryManager()

    @staticmethod
    def output_command_result(command_result: dict) -> None:
        """
        Метод выводит в консоль полученный результат выполнения
        методов добавления, удаления книги или изменения статуса книги.

        :param command_result: dict -- сообщение с результатом выполнения
        :return: None
        """

        if 'error' in command_result.keys():
            print('!', command_result['error'], '!')
        else:
            print(command_result['massage'])

    @staticmethod
    def output_books_information(books: list[Book]) -> None:
        """
        Метод выводит в консоль информацию о каждой книге из списка книг.

        :param books: list[Book] -- список книг, представленных экземплярами класса Book
        :return: None
        """

        for book in books:
            print('--------------------')
            print('id:', book.id)
            print('Название:', book.title)
            print('Автор:', book.author)
            print('Год:', book.year)
            print('Статус:', book.status)

    def launch_system(self) -> None:
        """
        Метод запускает бесконечный цикл, в котором ожидает команды пользователя
        и в зависимости от полученной команды вызывает соответствующий метод для отоброжения последующих инструкций.

        :return: None
        """

        print('Для использоваиня системы введите одну из следующих команд:\n'
              '- добавить книгу\n'
              '- удалить книгу\n'
              '- найти книгу\n'
              '- вывести список всех книг\n'
              '- изменить статус книги')
        while True:
            command: str = str(input('>')).lower()
            if command == 'добавить книгу':
                self.add_book_command()
            elif command == 'удалить книгу':
                self.delete_book_command()
            elif command == 'найти книгу':
                self.find_book_command()
            elif command == 'вывести список всех книг':
                self.display_all_books_command()
            elif command == 'изменить статус книги':
                self.change_book_status_command()
            elif command:
                print('Такой команды не существует')

    def add_book_command(self) -> None:
        """
        Метод получает из консоли название, автора и год издания книги,
        вызывает метод добавления книги из класса LibraryManager и выводит результат его выполнения.

        :return: None
        """

        title: str = str(input('Введите название книги: '))
        author: str = str(input('Введите автора книги: '))
        try:
            year: int = int(input('Введите год издания книги: '))
        except ValueError:
            print('! Год должен быть представлен в числовом формате !')
        else:
            result_add_book: dict = self.library_manager.add_book(title, author, year)
            self.output_command_result(result_add_book)

    def delete_book_command(self) -> None:
        """
        Метод получает из консоли id книги, которую нужно удалить, вызывает метод удаления книги из библиотеки
        и выводит результат его выполнения в консоль пользователю.
        Если пользователь ввел id, которое не является числом, выводится сообщение об ошибке.

        :return: None
        """

        try:
            delete_id: int = int(input('Введите id книги, которую хотите удалить: '))
        except ValueError:
            print('! Не корректный id !')
        else:
            result_delete_book: dict = self.library_manager.delete_book(delete_id)
            self.output_command_result(result_delete_book)

    def display_all_books_command(self) -> None:
        """
        Метод получает список книг и выводит их в консоль.

        :return: None
        """

        library: list = self.library_manager.display_all_books()
        self.output_books_information(library)

    def change_book_status_command(self) -> None:
        """
        Метод получает из консоли id книги и новый статус, вызывает метод изменения статуса книги
        и выводит результат ее выполнения в консоль пользователю.
        Если пользователь ввел id, которое не является числом, выводится сообщение об ошибке.

        :return: None
        """

        try:
            change_id: int = int(input('Введите id книги: '))
        except ValueError:
            print('! Не корректный id !')
        else:
            new_status: str = str(input('Введите новый статус книги (возможные варианты: "в наличии", "выдана"): '))
            result_change_status: dict = self.library_manager.change_book_status(change_id, new_status)
            self.output_command_result(result_change_status)

    def find_book_command(self) -> None:
        """
        Метод получает из консоли строку, по которой будет происходить поиск, вызывает метод поиска книг
        и если книги были найдены выводит их в консоль, иначе выводит сообщение о том, что ничего не было найдено.

        :return: None
        """

        attribute_to_find: str = str(input('Введите название, автора или год издания книги: '))
        found_books: list = self.library_manager.find_book(attribute_to_find)
        if not found_books:
            print('К сожалению, ничего не было найдено')
        else:
            self.output_books_information(found_books)


if __name__ == '__main__':
    LibraryManagementSystem().launch_system()
