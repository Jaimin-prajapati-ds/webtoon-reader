# Complete Code Files for Webtoon Reader

Yeh file me har ek backend aur frontend file ka complete code diya gaya hai. Tum directly copy-paste karke use kar sakte ho.

---

## Backend Files

### 1. `backend/app/__init__.py`
```python
# Empty file to make app a Python package
```

### 2. `backend/app/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./webtoon.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3. `backend/app/models.py`
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    cover_url = Column(String(500))
    author_name = Column(String(255))
    status = Column(String(50), default="ongoing")  # ongoing, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    chapters = relationship("Chapter", back_populates="comic")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    comic_id = Column(Integer, ForeignKey("comics.id"))
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(255))
    release_date = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=True)

    comic = relationship("Comic", back_populates="chapters")
    images = relationship("ChapterImage", back_populates="chapter")

class ChapterImage(Base):
    __tablename__ = "chapter_images"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    image_url = Column(String(500), nullable=False)
    sort_order = Column(Integer, nullable=False)

    chapter = relationship("Chapter", back_populates="images")
```

### 4. `backend/app/schemas.py`
```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Chapter Image Schemas
class ChapterImageBase(BaseModel):
    image_url: str
    sort_order: int

class ChapterImageCreate(ChapterImageBase):
    chapter_id: int

class ChapterImage(ChapterImageBase):
    id: int
    chapter_id: int

    class Config:
        from_attributes = True

# Chapter Schemas
class ChapterBase(BaseModel):
    chapter_number: int
    title: Optional[str] = None
    is_published: bool = True

class ChapterCreate(ChapterBase):
    comic_id: int

class Chapter(ChapterBase):
    id: int
    comic_id: int
    release_date: datetime
    images: List[ChapterImage] = []

    class Config:
        from_attributes = True

# Comic Schemas
class ComicBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    author_name: Optional[str] = None
    status: str = "ongoing"

class ComicCreate(ComicBase):
    pass

class Comic(ComicBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    chapters: List[Chapter] = []

    class Config:
        from_attributes = True

class ComicList(ComicBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

### 5. `backend/app/routers/__init__.py`
```python
# Empty file
```

### 6. `backend/app/routers/comics.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.ComicList])
def get_all_comics(db: Session = Depends(get_db)):
    comics = db.query(models.Comic).all()
    return comics

@router.get("/{slug}", response_model=schemas.Comic)
def get_comic(slug: str, db: Session = Depends(get_db)):
    comic = db.query(models.Comic).filter(models.Comic.slug == slug).first()
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return comic

@router.post("/", response_model=schemas.Comic)
def create_comic(comic: schemas.ComicCreate, db: Session = Depends(get_db)):
    db_comic = models.Comic(**comic.dict())
    db.add(db_comic)
    db.commit()
    db.refresh(db_comic)
    return db_comic

@router.get("/{slug}/chapters", response_model=List[schemas.Chapter])
def get_comic_chapters(slug: str, db: Session = Depends(get_db)):
    comic = db.query(models.Comic).filter(models.Comic.slug == slug).first()
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return comic.chapters
```

### 7. `backend/app/routers/chapters.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Chapter)
def create_chapter(chapter: schemas.ChapterCreate, db: Session = Depends(get_db)):
    db_chapter = models.Chapter(**chapter.dict())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

@router.get("/{chapter_id}", response_model=schemas.Chapter)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.post("/{chapter_id}/images", response_model=schemas.ChapterImage)
def add_chapter_image(chapter_id: int, image: schemas.ChapterImageCreate, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    db_image = models.ChapterImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
```

---

## Usage Instructions

### 1. Setup Backend
```bash
cd backend
mkdir -p app/routers
touch app/__init__.py
touch app/routers/__init__.py
# Copy each file content from above
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Test APIs
Backend: http://localhost:8000
Docs: http://localhost:8000/docs

### 3. Add Sample Comic (Python Script)
```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# 1. Create Comic
comic_data = {
    "title": "My First Comic",
    "slug": "my-first-comic",
    "description": "This is an amazing story about...",
    "cover_url": "https://via.placeholder.com/300x450",
    "author_name": "Your Name",
    "status": "ongoing"
}
res = requests.post(f"{BASE_URL}/comics/", json=comic_data)
comic = res.json()
print(f"Comic created: {comic['id']}")

# 2. Create Chapter
chapter_data = {
    "comic_id": comic["id"],
    "chapter_number": 1,
    "title": "Chapter 1: The Beginning",
    "is_published": True
}
res = requests.post(f"{BASE_URL}/chapters/", json=chapter_data)
chapter = res.json()
print(f"Chapter created: {chapter['id']}")

# 3. Add Images
for i in range(5):
    img_data = {
        "chapter_id": chapter["id"],
        "image_url": f"https://via.placeholder.com/800x{1200+i*100}",
        "sort_order": i
    }
    requests.post(f"{BASE_URL}/chapters/{chapter['id']}/images", json=img_data)
    print(f"Image {i+1} added")

print("Done! Check http://localhost:8000/docs to test APIs")
```

---

## Next Steps

1. **Images upload karo**: Cloudinary ya ImgBB pe
2. **Frontend banao**: React me (coming soon)
3. **Deploy karo**: Render (backend) + Vercel (frontend)

## Frontend Code (React) - Coming Soon

Frontend ke liye Vite + React setup karna hoga:

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios react-router-dom
```

Main components:
- HomePage: Comic list
- ComicPage: Comic details + chapters
- ReaderPage: Vertical scroll image reader

Complete frontend code agle update me!
