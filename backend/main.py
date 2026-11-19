from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from scraper import LK21Scraper

app = FastAPI(
    title="Netflix LK21 TV Backend API",
    description="Backend API pengumpan data film untuk Android TV Leanback app",
    version="1.0.0"
)

# Aktifkan CORS agar Android TV dalam jaringan lokal (Wi-Fi) bisa mengakses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = LK21Scraper()

class MovieCard(BaseModel):
    id: str
    title: str
    poster_url: str
    rating: str
    quality: Optional[str] = "HD"
    description: Optional[str] = ""

class CategoryFeed(BaseModel):
    id: int
    name: str
    movies: List[MovieCard]

class MovieDetail(BaseModel):
    id: str
    title: str
    overview: str
    rating: str
    year: str
    stream_url: str
    poster_url: str

@app.get("/")
def index():
    return {
        "status": "online",
        "service": "Netflix LK21 TV Backend",
        "endpoints": {
            "feed": "/api/feed",
            "detail": "/api/movie/{id}",
            "search": "/api/search?q=..."
        }
    }

@app.get("/api/feed", response_model=List[CategoryFeed])
async def get_home_feed():
    """Mengembalikan feed berbaris layaknya Netflix (Trending, Populer, Genre)"""
    mock_all = scraper.get_mock_movies()

    # Siapkan baris kategori khas Netflix
    feed = [
        CategoryFeed(
            id=1,
            name="🔥 Sedang Tren Minggu Ini",
            movies=[MovieCard(**m) for m in mock_all[0:4]]
        ),
        CategoryFeed(
            id=2,
            name="⭐ Film Terpopuler & Rating Tertinggi",
            movies=[MovieCard(**m) for m in mock_all[2:6]]
        ),
        CategoryFeed(
            id=3,
            name="💥 Aksi & Petualangan Pilihan",
            movies=[MovieCard(**m) for m in mock_all[1:5]]
        ),
        CategoryFeed(
            id=4,
            name="👻 Horor & Thriller Menegangkan",
            movies=[MovieCard(**m) for m in mock_all[6:8] + mock_all[0:2]]
        ),
        CategoryFeed(
            id=5,
            name="🚀 Fiksi Ilmiah & Multiverse",
            movies=[MovieCard(**m) for m in mock_all[4:7]]
        )
    ]
    return feed

@app.get("/api/movie/{movie_id}", response_model=MovieDetail)
async def get_movie(movie_id: str):
    """Mengambil detail film dan link stream video yang siap diputar di ExoPlayer"""
    detail = await scraper.get_movie_detail(movie_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Film tidak ditemukan")
    return MovieDetail(**detail)

@app.get("/api/search", response_model=List[MovieCard])
async def search_movies(q: str = Query(..., min_length=1)):
    """Pencarian film berdasarkan kata kunci"""
    all_movies = scraper.get_mock_movies()
    results = [
        MovieCard(**m) for m in all_movies 
        if q.lower() in m["title"].lower() or q.lower() in m.get("description", "").lower()
    ]
    return results

if __name__ == "__main__":
    import uvicorn
    # Menjalankan di port 8000 dan mendengarkan semua IP (0.0.0.0) agar Android TV bisa konek
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
