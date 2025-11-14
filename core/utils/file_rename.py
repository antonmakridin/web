import os
from uuid import uuid4
from datetime import datetime
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day

class BookFileRenamer:
    """Класс для переименования файлов книг"""
    
    @staticmethod
    def rename_cover(instance, filename):
        """Переименовывает файл обложки книги"""
        ext = filename.split('.')[-1]  # расширение файла
        # новое имя
        new_filename = f"cover_{uuid4().hex[:8]}.{ext}"
        return os.path.join(f'books/covers/{year}/{month}/{day}/', new_filename)
    
    @staticmethod
    def rename_file(instance, filename):
        """Переименовываем файл книги"""
        ext = filename.split('.')[-1]
        # новое имя
        new_filename = f"book_{uuid4().hex[:8]}.{ext}"
        return os.path.join(f'books/pdfs/{year}/{month}/{day}', new_filename)