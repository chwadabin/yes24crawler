import requests
from bs4 import BeautifulSoup
import pandas as pd

result = []

for page in range(1, 43):
    print(f"{page}페이지 수집 중...")

    url = f"https://www.yes24.com/product/category/bestseller?categoryNumber=001&pageNumber={page}&pageSize=24"
    res = requests.get(url)
    
    if res.status_code != 200:
        print("접속 실패", res.status_code)
        continue

    soup = BeautifulSoup(res.text, "html.parser")
    books = soup.find_all("li", attrs={"data-goods-no": True})

    if not books:
        print("책 정보 없음")
        continue

    for book in books:
        try:
            rank = book.find("em", class_="ico rank").text.strip()
        except:
            rank = ""

        try:
            title = book.find("a", class_="gd_name").text.strip()
        except:
            title = ""

        try:
            author_tag = book.find("span", class_="authPub info_auth")
            author = author_tag.find("a").text.strip() if author_tag else ""
        except:
            author = ""

        try:
            pub_tag = book.find("span", class_="authPub info_pub")
            publisher = pub_tag.find("a").text.strip() if pub_tag else ""
        except:
            publisher = ""

        result.append([rank, title, author, publisher])

df = pd.DataFrame(result, columns=["순위", "제목", "저자", "출판사"])
df.to_csv("yes24_베스트셀러_전체.csv", index=False, encoding="utf-8-sig")
print("✅ 저장 완료. 총", len(df), "권")
