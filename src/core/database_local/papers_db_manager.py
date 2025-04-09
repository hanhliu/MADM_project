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
        if query.exec("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            """):
            print(f"HanhLT: Created Paper")
        self.db_manager.close()

    def addToDatabase(self, paper_data: Paper):
        self.db_manager.open()
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM papers WHERE id = ? AND topic = ?")
        query.addBindValue(paper_data.id)
        query.addBindValue(paper_data.topic)

        if not query.exec():
            print("Không thể thực hiện truy vấn kiểm tra:", query.lastError().text())
            return

        query.next()
        count = query.value(0)
        if count > 0:
            print(f"Paper {paper_data.topic} đã có trong dữ liệu")
            return

        query.prepare(
            """
            INSERT INTO papers (id,
                topic, field, date, reviewer_degree_requirement, required_reviewer_rating,
                min_reviewers, authors, numbers_of_published_papers_requirement,
                years_of_experience_requirement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        )

        query.addBindValue(paper_data.id)
        query.addBindValue(paper_data.topic)
        query.addBindValue(paper_data.field)
        query.addBindValue(paper_data.date)
        query.addBindValue(paper_data.reviewer_degree_requirement)
        query.addBindValue(paper_data.required_reviewer_rating)
        query.addBindValue(paper_data.min_reviewers)
        query.addBindValue(paper_data.authors)
        query.addBindValue(paper_data.numbers_of_published_papers_requirement)
        query.addBindValue(paper_data.years_of_experience_requirement)
        if query.exec():
            print(f"Thêm Paper: '{paper_data.topic}' thanh cong")
        else:
            print("Không thể thêm Paper:", query.lastError().text())
