from requests import get
from time import sleep

def get_wrapper(url):
    r = get(url)
    while True:
        if r.status_code == 200:
            return r
        elif r.status_code == 429:
            retry_time = int(r.headers["Retry-After"])
            print(f'Retrying after {retry_time} sec...')
            sleep(retry_time)
        else:
            return r
    
        