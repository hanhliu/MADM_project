import json
from typing import List

from PySide6.QtSql import QSqlQuery
from src.core.database_local.abstract_db_manager import AbstractDatabaseManager
from src.core.models.reviewer_model import Reviewer


class ReviewersDatabaseManager(AbstractDatabaseManager):

    def __init__(self, db_manager=None):
        super().__init__()
        self.db_manager = db_manager

    def createDatabase(self):
        self.db_manager.open()
        query = QSqlQuery()
        success = query.exec(
            """
            CREATE TABLE IF NOT EXISTS reviewers (
                id VARCHAR(255) PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                field TEXT NOT NULL,
                degree TEXT NOT NULL,
                conference_topic TEXT,
                average_rating FLOAT,
                years_of_experience INTEGER,
                published_papers INTEGER,
                availability TEXT
            )
            """
        )
        if success:
            print("✅ Created reviewers table")
        else:
            print("❌ Error creating reviewers table:", query.lastError().text())
        self.db_manager.close()

    def addToDatabase(self, reviewer: Reviewer):
        if not self.db_manager.open():
            print("❌ Không mở được database trong addToDatabase")
            return

        self.db_manager.open()
        query = QSqlQuery(self.db_manager.db)

        # Kiểm tra xem reviewer đã tồn tại chưa
        query.prepare("SELECT COUNT(*) FROM reviewers WHERE id = ?")
        query.addBindValue(reviewer.id)
        if not query.exec():
            print("❌ Query failed (check existence):", query.lastError().text())
            self.db_manager.close()
            return

        query.next()
        if query.value(0) > 0:
            print(f"⚠️ Reviewer '{reviewer.name}' already exists")
            self.db_manager.close()
            return

        # Thêm reviewer mới
        query.prepare(
            """
            INSERT INTO reviewers (
                id, name, field, degree, conference_topic,
                average_rating, years_of_experience,
                published_papers, availability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )
        query.addBindValue(reviewer.id)
        query.addBindValue(reviewer.name)
        query.addBindValue(json.dumps(reviewer.field))
        query.addBindValue(reviewer.degree)
        query.addBindValue(reviewer.conference_topic)
        query.addBindValue(reviewer.average_rating)
        query.addBindValue(reviewer.years_of_experience)
        query.addBindValue(reviewer.published_papers)

        query.addBindValue(json.dumps(reviewer.availability))

        if query.exec():
            print(f"✅ Added Reviewer: {reviewer.name}")
        else:
            print("❌ Failed to add Reviewer:", query.lastError().text())

        self.db_manager.close()

    def getAllFromDatabase(self) -> List[Reviewer]:
        self.db_manager.open()
        query = QSqlQuery()
        query.prepare("SELECT * FROM reviewers")

        reviewers = []
        if not query.exec():
            print("❌ Failed to get reviewers:", query.lastError().text())
            self.db_manager.close()
            return reviewers

        while query.next():
            reviewers.append(Reviewer(
                id=query.value(0),
                name=query.value(1),
                field=json.loads(query.value(2)),  # Nếu lưu json, cần json.loads
                degree=query.value(3),
                conference_topic=query.value(4),
                average_rating=query.value(5),
                years_of_experience=query.value(6),
                published_papers=query.value(7),
                availability=json.loads(query.value(8))
            ))

        self.db_manager.close()
        return reviewers

    def removeFromDatabase(self, reviewer_id: str) -> bool:
        self.db_manager.open()
        query = QSqlQuery()
        query.prepare("DELETE FROM reviewers WHERE id = ?")
        query.addBindValue(reviewer_id)

        success = query.exec()
        if success:
            print(f"🗑️ Reviewer with ID {reviewer_id} has been removed")
        else:
            print("❌ Failed to remove reviewer:", query.lastError().text())

        self.db_manager.close()
        return success