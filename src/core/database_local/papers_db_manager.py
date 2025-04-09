import json
from typing import List

from PySide6.QtSql import QSqlQuery
from src.core.database_local.abstract_db_manager import AbstractDatabaseManager
from src.core.models.paper_model import Paper


class PapersDatabaseManager(AbstractDatabaseManager):

    def __init__(self, db_manager=None):
        super().__init__()
        self.db_manager = db_manager

    def createDatabase(self):
        self.db_manager.open()
        query = QSqlQuery()
        if query.exec(
            """
            CREATE TABLE IF NOT EXISTS papers (
                id VARCHAR(255) PRIMARY KEY NOT NULL,
                topic TEXT NOT NULL,
                field TEXT NOT NULL,
                date TEXT NOT NULL,
                reviewer_degree_requirement TEXT,
                required_reviewer_rating REAL,
                min_reviewers INTEGER,
                authors TEXT NOT NULL,
                numbers_of_published_papers_requirement INTEGER,
                years_of_experience_requirement INTEGER
            )
            """
        ):
            print("✅ Created papers table")
        else:
            print("❌ Error creating papers table:", query.lastError().text())
        self.db_manager.close()

    def addToDatabase(self, paper_data: Paper):
        if not self.db_manager.open():
            print("❌ Không mở được database trong addToDatabase")
            return

        self.db_manager.open()
        query = QSqlQuery(self.db_manager.db)

        # Kiểm tra paper đã tồn tại chưa
        query.prepare("SELECT COUNT(*) FROM papers WHERE id = ?")
        query.addBindValue(paper_data.id)
        if not query.exec():
            print("❌ Failed to check paper:", query.lastError().text())
            self.db_manager.close()
            return

        query.next()
        count = query.value(0)
        if count > 0:
            print(f"⚠️ Paper '{paper_data.topic}' đã có trong dữ liệu")
            self.db_manager.close()
            return

        # Thêm paper mới
        query.prepare(
            """
            INSERT INTO papers (
                id, topic, field, date, reviewer_degree_requirement,
                required_reviewer_rating, min_reviewers, authors,
                numbers_of_published_papers_requirement, years_of_experience_requirement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )

        query.addBindValue(paper_data.id)
        query.addBindValue(paper_data.topic)
        query.addBindValue(json.dumps(paper_data.field))  # Có thể serialize JSON nếu là list
        query.addBindValue(paper_data.date)
        query.addBindValue(paper_data.reviewer_degree_requirement)
        query.addBindValue(paper_data.required_reviewer_rating)
        query.addBindValue(paper_data.min_reviewers)
        query.addBindValue(json.dumps(paper_data.authors))  # Có thể là JSON list
        query.addBindValue(paper_data.numbers_of_published_papers_requirement)
        query.addBindValue(paper_data.years_of_experience_requirement)

        if query.exec():
            print(f"✅ Thêm Paper: '{paper_data.topic}' thành công")
        else:
            print("❌ Không thể thêm Paper:", query.lastError().text())

        self.db_manager.close()

    def getAllFromDatabase(self) -> List[Paper]:
        self.db_manager.open()
        query = QSqlQuery()
        query.prepare("SELECT * FROM papers")  # ✅ sửa tên bảng

        papers = []
        if not query.exec():
            print("❌ Lỗi khi truy vấn papers:", query.lastError().text())
            self.db_manager.close()
            return papers

        while query.next():
            papers.append(Paper(
                id=query.value(0),
                topic=query.value(1),
                field=json.loads(query.value(2)),  # field dạng List[str]
                date=query.value(3),
                reviewer_degree_requirement=query.value(4),
                required_reviewer_rating=query.value(5),
                min_reviewers=query.value(6),
                authors=json.loads(query.value(7)),  # authors dạng List[str]
                numbers_of_published_papers_requirement=query.value(8),
                years_of_experience_requirement=query.value(9)
            ))

        self.db_manager.close()
        return papers

    def removeFromDatabase(self, paper_id: str) -> bool:
        self.db_manager.open()
        query = QSqlQuery()
        query.prepare("DELETE FROM papers WHERE id = ?")
        query.addBindValue(paper_id)

        success = query.exec()
        if success:
            print(f"🗑️ Đã xoá paper với ID: {paper_id}")
        else:
            print("❌ Không thể xoá paper:", query.lastError().text())

        self.db_manager.close()
        return success
