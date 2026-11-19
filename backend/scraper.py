import httpx
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any, Optional

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
}

class LK21Scraper:
    def __init__(self, base_url: str = "https://tv10.lk21official.my"):
        self.base_url = base_url.rstrip("/")

    async def _fetch_html(self, url: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=DEFAULT_HEADERS) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.text
        except Exception as e:
            print(f"[Scraper Error] Fetching {url} failed: {e}")
        return None

    def _parse_movie_card(self, article) -> Optional[Dict[str, Any]]:
        try:
            link_tag = article.find("a")
            if not link_tag:
                return None
            
            href = link_tag.get("href", "")
            slug = href.strip("/").split("/")[-1]
            
            # Title
            title_tag = article.find(["h2", "h3", "span", "strong"], class_=re.compile(r"title|film-title", re.I))
            title = title_tag.get_text(strip=True) if title_tag else link_tag.get("title", slug)

            # Poster
            img_tag = article.find("img")
            poster = ""
            if img_tag:
                poster = img_tag.get("data-src") or img_tag.get("src") or ""
                if poster.startswith("//"):
                    poster = "https:" + poster

            # Rating
            rating_tag = article.find(class_=re.compile(r"rating|imdb", re.I))
            rating = rating_tag.get_text(strip=True) if rating_tag else "7.5"

            # Year / Duration / Quality
            quality_tag = article.find(class_=re.compile(r"quality|label", re.I))
            quality = quality_tag.get_text(strip=True) if quality_tag else "HD"

            return {
                "id": slug,
                "title": title,
                "poster_url": poster,
                "rating": rating,
                "quality": quality,
                "detail_url": href if href.startswith("http") else f"{self.base_url}/{slug}",
                "description": f"Kualitas: {quality} • Rating: {rating} ★"
            }
        except Exception as e:
            print(f"[Parser Error] Failed to parse item: {e}")
            return None

    async def get_movies(self, path: str = "") -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        html = await self._fetch_html(url)
        movies = []

        if html:
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all(["article", "div"], class_=re.compile(r"movie|item|poster", re.I))
            for item in items:
                movie = self._parse_movie_card(item)
                if movie and movie["poster_url"]:
                    movies.append(movie)

        # Fallback if scraping returns empty (e.g., domain down or cloudflare)
        if not movies:
            movies = self.get_mock_movies(category=path)

        return movies

    async def get_movie_detail(self, slug: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{slug}"
        html = await self._fetch_html(url)
        
        if html:
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("h1")
            title_text = title.get_text(strip=True) if title else slug.replace("-", " ").title()

            overview_tag = soup.find("blockquote") or soup.find("div", class_=re.compile(r"synopsis|desc", re.I))
            overview = overview_tag.get_text(strip=True) if overview_tag else "Nonton film gratis dengan subtitle Indonesia."

            # Find stream iframe or player
            iframe = soup.find("iframe", src=re.compile(r"player|embed|stream", re.I))
            stream_url = iframe.get("src") if iframe else "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

            return {
                "id": slug,
                "title": title_text,
                "overview": overview,
                "rating": "8.1",
                "year": "2024",
                "stream_url": stream_url,
                "poster_url": f"https://picsum.photos/seed/{slug}/500/750"
            }

        # Mock fallback for instant test play
        mock_map = {m["id"]: m for m in self.get_mock_movies("all")}
        if slug in mock_map:
            m = mock_map[slug]
            return {
                "id": m["id"],
                "title": m["title"],
                "overview": m.get("description", "Film pilihan populer dengan streaming kualitas HD subtitle Indonesia."),
                "rating": m.get("rating", "8.5"),
                "year": "2024",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                "poster_url": m["poster_url"]
            }

        return {
            "id": slug,
            "title": slug.replace("-", " ").title(),
            "overview": "Film streaming kualitas HD dengan navigasi mudah ala Netflix.",
            "rating": "8.0",
            "year": "2024",
            "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
            "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&auto=format&fit=crop"
        }

    def get_mock_movies(self, category: str = "") -> List[Dict[str, Any]]:
        """Fallback mock data yang siap diputar di Android TV tanpa takut link mati/iklan"""
        sample_database = [
            {
                "id": "avatar-the-way-of-water",
                "title": "Avatar: The Way of Water",
                "poster_url": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
                "rating": "8.2",
                "quality": "4K UltraHD",
                "description": "Jake Sully dan Neytiri harus melindungi keluarga mereka dari ancaman bangsa manusia.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
            },
            {
                "id": "spider-man-no-way-home",
                "title": "Spider-Man: No Way Home",
                "poster_url": "https://image.tmdb.org/t/p/w500/uJYYizSuA9Y3DCs0qS4qWvlyZz4.jpg",
                "rating": "8.7",
                "quality": "1080p HD",
                "description": "Identitas Spider-Man terbongkar, memicu terbukanya multiverse dari dimensi lain.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
            },
            {
                "id": "oppenheimer-2023",
                "title": "Oppenheimer",
                "poster_url": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
                "rating": "8.9",
                "quality": "IMAX HD",
                "description": "Kisah ilmuwan J. Robert Oppenheimer memimpin Proyek Manhattan untuk menciptakan bom atom.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
            },
            {
                "id": "top-gun-maverick",
                "title": "Top Gun: Maverick",
                "poster_url": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg",
                "rating": "8.4",
                "quality": "1080p HD",
                "description": "Pete 'Maverick' Mitchell kembali melatih pilot muda untuk misi berbahaya yang hampir mustahil.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
            },
            {
                "id": "interstellar",
                "title": "Interstellar",
                "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
                "rating": "9.0",
                "quality": "4K UHD",
                "description": "Perjalanan melintasi lubang cacing di luar angkasa demi mencari rumah baru bagi umat manusia.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackSeeTheWorld.mp4"
            },
            {
                "id": "the-batman-2022",
                "title": "The Batman",
                "poster_url": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg",
                "rating": "8.1",
                "quality": "1080p HD",
                "description": "Batman menginvestigasi korupsi tersembunyi di kota Gotham dan menghadapi pembunuh berantai Riddler.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
            },
            {
                "id": "dune-part-two",
                "title": "Dune: Part Two",
                "poster_url": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
                "rating": "8.8",
                "quality": "4K UHD",
                "description": "Paul Atreides bersatu dengan Chani dan suku Fremen untuk membalaskan dendam keluarganya.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
            },
            {
                "id": "pengabdi-setan-2",
                "title": "Pengabdi Setan 2: Communion",
                "poster_url": "https://image.tmdb.org/t/p/w500/9k97rQ2T4PZgUo0u3k4F2aZ7R1.jpg",
                "rating": "7.8",
                "quality": "HD 1080p",
                "description": "Rini dan adik-adiknya pindah ke rumah susun, namun teror masa lalu kembali menghantui mereka.",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
            }
        ]
        return sample_database
