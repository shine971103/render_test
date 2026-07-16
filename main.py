import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# 讀取資料庫連線環境變數
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # 本地測試時如果沒有環境變數，預設使用 SQLite 資料庫
    DATABASE_URL = "sqlite:///./test.db"

# Render 提供之 PostgreSQL 網址開頭可能為 postgres://，但 SQLAlchemy 要求 postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 初始化 SQLAlchemy 連線
# 若為 SQLite，需額外加上 connect_args={'check_same_thread': False}
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定義資料庫 Book 模型
class BookDB(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=False)

# 自動建立資料表
Base.metadata.create_all(bind=engine)

# 定義 Pydantic 資料驗證格式
class BookBase(BaseModel):
    title: str
    author: str
    published_year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    
    class Config:
        from_attributes = True

# 初始化 FastAPI 應用程式
app = FastAPI(title="Book CRUD API")

# 取得資料庫連接的 Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 路由 1：首頁問候語
@app.get("/")
def read_root():
    return {"message": "Hello"}

# 路由 2：Hello 端點 (簡報中的 GET /Hello)
@app.get("/Hello")
def say_hello():
    return {"message": "Hello"}

# 路由 3：新增書籍 (POST /books)
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookDB(title=book.title, author=book.author, published_year=book.published_year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# 路由 4：取得所有書籍列表 (GET /books)
@app.get("/books", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(BookDB).all()

# 路由 5：取得單一書籍資訊 (GET /books/{book_id})
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# 路由 6：修改書籍資訊 (PUT /books/{book_id})
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = updated_book.title
    db_book.author = updated_book.author
    db_book.published_year = updated_book.published_year
    db.commit()
    db.refresh(db_book)
    return db_book

# 路由 7：刪除書籍 (DELETE /books/{book_id})
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
