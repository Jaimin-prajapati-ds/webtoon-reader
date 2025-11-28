# Webtoon Reader - Manhwa Clan Style Comic Website

A full-stack webtoon/manhwa reader website inspired by Manhwa Clan, built with FastAPI (Python) backend and React frontend.

## Features

- **Vertical Scroll Reader**: Mobile-friendly webtoon-style vertical reader
- **Comic Management**: Browse comics with cover images, descriptions, genres
- **Chapter System**: Organized chapter listing with navigation
- **Responsive Design**: Works on desktop and mobile devices
- **REST API**: Clean FastAPI backend with automatic documentation
- **SQLite Database**: Simple file-based database for easy deployment

## Project Structure

```
webtoon-reader/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   ├── database.py       # Database connection
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── comics.py     # Comic endpoints
│   │       └── chapters.py   # Chapter endpoints
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ComicCard.jsx
│   │   │   ├── ChapterList.jsx
│   │   │   └── Reader.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ComicPage.jsx
│   │   │   └── ReaderPage.jsx
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
└── README.md
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on http://localhost:3000

## Database Schema

### Comics Table
- id (Primary Key)
- title
- slug (URL-friendly)
- description
- cover_url (image URL)
- author_name
- status (ongoing/completed)
- created_at
- updated_at

### Chapters Table
- id (Primary Key)
- comic_id (Foreign Key)
- chapter_number
- title
- release_date
- is_published

### Chapter Images Table
- id (Primary Key)
- chapter_id (Foreign Key)
- image_url
- sort_order (for image sequence)

## API Endpoints

### Comics
- `GET /api/comics` - List all comics
- `GET /api/comics/{slug}` - Get single comic
- `POST /api/comics` - Create comic (admin)

### Chapters
- `GET /api/comics/{slug}/chapters` - List chapters for a comic
- `GET /api/comics/{slug}/chapters/{number}` - Get chapter with images
- `POST /api/chapters` - Create chapter (admin)

## Adding Your Comic

1. Upload comic images to a cloud service (Cloudinary, ImgBB, or S3)
2. Use API or database to add:
   - Comic entry with cover, title, description
   - Chapter entries
   - Image URLs for each chapter

### Example: Adding via Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Add comic
comic_data = {
    "title": "My Awesome Comic",
    "slug": "my-awesome-comic",
    "description": "An epic story...",
    "cover_url": "https://your-image-host.com/cover.jpg",
    "author_name": "Your Name",
    "status": "ongoing"
}
response = requests.post(f"{BASE_URL}/comics", json=comic_data)
comic = response.json()

# Add chapter
chapter_data = {
    "comic_id": comic["id"],
    "chapter_number": 1,
    "title": "Chapter 1: Beginning",
    "is_published": True
}
response = requests.post(f"{BASE_URL}/chapters", json=chapter_data)
chapter = response.json()

# Add images
for i, img_url in enumerate([
    "https://your-host.com/ch1-img1.jpg",
    "https://your-host.com/ch1-img2.jpg",
]):
    image_data = {
        "chapter_id": chapter["id"],
        "image_url": img_url,
        "sort_order": i
    }
    requests.post(f"{BASE_URL}/chapters/{chapter['id']}/images", json=image_data)
```

## Deployment

### Backend (Render/Railway)
1. Push code to GitHub
2. Connect Render to your repo
3. Add environment variables if needed
4. Deploy with command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy `build/` folder
3. Set environment variable: `REACT_APP_API_URL=https://your-backend.com`

## Image Hosting Options

1. **Cloudinary** (Free tier: 25GB)
2. **ImgBB** (Free)
3. **AWS S3** (Pay as you go)
4. **GitHub** (Not recommended for large files)

## Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM
- SQLite - Database
- Uvicorn - ASGI server

**Frontend:**
- React - UI framework
- React Router - Navigation
- Axios - HTTP client

## Contributing

Feel free to fork and customize for your own comics!

## License

MIT License
