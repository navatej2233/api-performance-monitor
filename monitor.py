import requests
import time
import sqlite3

URL = "https://httpbin.org/get"

while True:
    start = time.time()
    response = requests.get(URL)
    end = time.time()

    rt = end - start
    code = response.status_code

    conn = sqlite3.connect("API_DATA.db")
    c = conn.cursor()
    c.execute("INSERT INTO api_data(url, response_time, status_code) VALUES (?, ?, ?)",
              (URL, rt, code))
    conn.commit()
    conn.close()

    print("Inserted", rt, code)
    time.sleep(30)  # 30 seconds gap
