import os
from typing import Dict

from PySide6.QtSql import QSqlDatabase, QSqlQuery
from src.core.singleton_class import Singleton


class DatabaseManager(metaclass=Singleton):
    def __init__(self):
        self.db = None
        self.repo_dict: Dict[str, object] = {}
        self.initDatabase()

    def initDatabase(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("madm.db")

        if not self.db.open():
            raise Exception("Cannot open database")

        # Kiểm tra nếu file chưa tồn tại, thì tạo bảng
        if not os.path.exists("madm.db"):
            self.createTables()

    def addRepository(self, name: str, repo):
        """
        Thêm repository (đối tượng có phương thức createDatabase()) vào repo_dict
        """
        self.repo_dict[name] = repo

    def createTables(self):
        """
        Gọi createDatabase() từ từng repository để tạo bảng
        """
        for name, repo in self.repo_dict.items():
            if hasattr(repo, "createDatabase") and callable(repo.createDatabase):
                repo.createDatabase()
            else:
                print(f"Repository {name} is missing a callable createDatabase() method.")

    def closeDatabase(self):
        """
        Đóng kết nối khi không còn dùng
        """
        if self.db and self.db.isOpen():
            self.db.close()
