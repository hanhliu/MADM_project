import os
from enum import Enum
from typing import Dict

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from src.core.database_local.abstract_db_manager import AbstractDatabaseManager
from src.core.database_local.papers_db_manager import PapersDatabaseManager
from src.core.database_local.reviewers_db_manager import ReviewersDatabaseManager
from src.core.singleton_class import Singleton
from src.core.utils import ItemType


class DatabaseManager(metaclass=Singleton):
    def __init__(self):
        self.db = None
        reviewers_repo = ReviewersDatabaseManager(self)
        papers_repo = PapersDatabaseManager(self)
        self.repo_dict: dict[int, AbstractDatabaseManager] = {
            ItemType.REVIEWER.value: reviewers_repo,
            ItemType.PAPER.value: papers_repo
        }
        self.initDatabase()

    def initDatabase(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("madm.db")

        if not self.db.open():
            raise Exception("Cannot open database")

        if self.db.isOpen():
            self.createTables()

    # mở kết nối csdl
    def open(self) -> bool:
        try:
            if not self.db.isOpen():
                self.db.open()
            return True
        except Exception as e:
            print(e)
            return False

    # đóng kết nối csdl
    def close(self) -> bool:
        try:
            if self.db.isOpen():
                self.db.close()
            return True
        except Exception as e:
            print(e)
            return False

    # tạo bảng
    def createTables(self):
        for repo in self.repo_dict.values():
            repo.createDatabase()

    # thêm vào csdl
    def addToDatabase(self, itemType, *args, **kwargs) -> int:
        return self.repo_dict[itemType].addToDatabase(*args, **kwargs)

    # xóa ra khỏi csdl
    def removeFromDatabase(self, itemType, *args, **kwargs):
        return self.repo_dict[itemType].removeFromDatabase(*args, **kwargs)

    # lấy tất cả dữ liệu từ csdl
    def getAllFromDatabase(self, itemType):
        return self.repo_dict[itemType].getAllFromDatabase()
