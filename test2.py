import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def search_naver_news(keyword, start_date, end_date):
    articles = []
    base_url = "https://search.naver.com/search.naver"
    
    for date in date_range(start_date, end_date):
        params = {
            'where': 'news',
            'query': keyword,
            'sort': '0',  # 관련도순
            'ds': date,
            'de': date,
            'nso': f"so:r,p:from{date.replace('.', '')}to{date.replace('.', '')}",
        }
        
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_items = soup.find_all('div', {'class': 'news_area'})
        
        for item in news_items:
            title = item.find('a', {'class': 'news_tit'}).text
            link = item.find('a', {'class': 'news_tit'})['href']
            pub_date = date

            # 본문 요약 가져오기 (3줄 요약된 것)
            summary = item.find('a', {'class': 'dsc_txt_wrap'})
            if summary:
                summary_text = summary.text.strip()
            else:
                summary_text = "요약 정보 없음"

            # 중복 기사 제거
            if not any(article['title'] == title for article in articles):
                articles.append({
                    'title': title,
                    'link': link,
                    'pub_date': pub_date,
                    'summary': summary_text
                })

    return articles

def date_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y.%m.%d')
    end = datetime.strptime(end_date, '%Y.%m.%d')
    step = timedelta(days=1)
    
    while start <= end:
        yield start.strftime('%Y.%m.%d')
        start += step

# 출력하는 함수
def print_articles(articles):
    for article in articles:
        print(f"제목: {article['title']}")
        print(f"링크: {article['link']}")
        print(f"발행일: {article['pub_date']}")
        print(f"요약: {article['summary']}\n")
        
# 테스트 실행
keyword = "인공지능"
start_date = "2024.10.01"
end_date = "2024.10.03"

articles = search_naver_news(keyword, start_date, end_date)
print_articles(articles)
