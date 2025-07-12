import random
import time
import asyncio
from typing import List, Dict

class AntiDetectionUtils:
    """
    Utility class untuk menghindari deteksi bot dan rate limiting
    """
    
    # Daftar User-Agent yang akan dirotasi
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    ]
    
    # Daftar Accept-Language headers
    ACCEPT_LANGUAGES = [
        'en-US,en;q=0.9',
        'en-GB,en;q=0.9',
        'en-US,en;q=0.8,id;q=0.6',
        'id-ID,id;q=0.9,en;q=0.8',
        'en-US,en;q=0.9,es;q=0.8',
    ]
    
    @staticmethod
    def get_random_user_agent() -> str:
        """
        Mengembalikan User-Agent secara acak
        """
        return random.choice(AntiDetectionUtils.USER_AGENTS)
    
    @staticmethod
    def get_random_accept_language() -> str:
        """
        Mengembalikan Accept-Language secara acak
        """
        return random.choice(AntiDetectionUtils.ACCEPT_LANGUAGES)
    
    @staticmethod
    def get_random_headers() -> Dict[str, str]:
        """
        Mengembalikan headers HTTP yang dirandomisasi
        """
        return {
            'User-Agent': AntiDetectionUtils.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': AntiDetectionUtils.get_random_accept_language(),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
    
    @staticmethod
    async def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
        """
        Menambahkan delay acak untuk menghindari rate limiting
        """
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    @staticmethod
    def random_delay_sync(min_seconds: float = 1.0, max_seconds: float = 3.0):
        """
        Versi sinkron dari random_delay
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @staticmethod
    def get_request_config() -> Dict:
        """
        Mengembalikan konfigurasi request yang optimal untuk menghindari deteksi
        """
        return {
            'headers': AntiDetectionUtils.get_random_headers(),
            'timeout': random.uniform(10, 20),  # Timeout acak antara 10-20 detik
        }

class RateLimiter:
    """
    Class untuk mengatur rate limiting
    """
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Args:
            max_requests: Maksimal request dalam time_window
            time_window: Window waktu dalam detik
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def can_make_request(self) -> bool:
        """
        Mengecek apakah bisa membuat request baru
        """
        now = time.time()
        
        # Hapus request yang sudah lewat dari time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        # Cek apakah masih bisa membuat request
        return len(self.requests) < self.max_requests
    
    def add_request(self):
        """
        Menambahkan timestamp request baru
        """
        self.requests.append(time.time())
    
    def wait_time(self) -> float:
        """
        Mengembalikan waktu tunggu sebelum bisa membuat request lagi
        """
        if self.can_make_request():
            return 0
        
        now = time.time()
        oldest_request = min(self.requests)
        return self.time_window - (now - oldest_request)

# Instance global rate limiter
global_rate_limiter = RateLimiter(max_requests=20, time_window=300)  # 20 request per 5 menit

