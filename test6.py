import requests
from bs4 import BeautifulSoup

# IT/과학 뉴스 URL
url = "https://news.naver.com/main/list.naver?mode=LSD&mid=shm&sid1=105"

# 웹페이지 데이터 가져오기
response = requests.get(url)
html = response.text

# BeautifulSoup을 사용해 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 뉴스 기사 제목과 링크 추출
news_list = soup.select('.list_body.newsflash_body .type06_headline a')

# AI 관련 기사만 추출
ai_news = []
for news in news_list:
    title = news.get_text().strip()
    link = news['href']
    
    # "AI" 키워드가 제목에 포함된 기사만 추출
    if "AI" in title or "인공지능" in title:
        ai_news.append((title, link))
    
    # 최대 10개까지만 수집
    if len(ai_news) >= 10:
        break

# AI 관련 기사 출력
for title, link in ai_news:
    print(f"제목: {title}")
    print(f"링크: {link}")
    print("-" * 50)
