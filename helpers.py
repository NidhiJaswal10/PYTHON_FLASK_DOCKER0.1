import time


def getNetflixMovies(name):
    """
    Yeh function Netflix API ko simulate karta hai.
    Asli duniya mein ye network call karega aur time lega.
    """
    print(f"Fetching movies for {name} from Netflix API...")
    time.sleep(5)  # 5 second ka artificial delay
    return ["Stranger Things", "Dark", "Inception", "The Crown"]
