import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from datetime import datetime, timedelta

# Huggingface summarization 모델 로드 (적용할 요약 모델 선택)
summarizer = pipeline("summarization")

# 특정 날짜 범위의 기사 URL을 가져오는 함수
def get_news_urls(keyword, start_date, end_date):
    base_url = "https://search.naver.com/search.naver"
    urls = []
    current_date = start_date

    while current_date <= end_date:
        params = {
            "where": "news",
            "query": keyword,
            "sort": "0",  # 날짜 순 정렬
            "start": "1",
            "ds": current_date.strftime("%Y.%m.%d"),
            "de": current_date.strftime("%Y.%m.%d"),
        }
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', {'class': 'news_tit'})
        
        for article in articles:
            title = article['title']
            link = article['href']
            date = current_date.strftime("%Y-%m-%d")
            urls.append((title, link, date))
        
        current_date += timedelta(days=1)

    return urls

# 기사 내용을 요약하는 함수
# def get_article_summary(article_url):
#     response = requests.get(article_url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # 기사 본문 추출 (페이지 구조에 따라 수정 필요)
#     paragraphs = soup.find_all('p')
#     content = ' '.join([para.text for para in paragraphs])

#     # 내용이 충분히 긴 경우만 요약 진행
#     if len(content) > 200:
#         summary = summarizer(content, max_length=60, min_length=30, do_sample=False)
#         return summary[0]['summary_text']
#     else:
#         return "요약 불가 (본문이 짧음)"

def get_article_summary(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    content = ' '.join([para.text for para in paragraphs])

    if len(content) > 200:
        try:
            summary = summarizer(content, max_length=60, min_length=30, do_sample=False)
            if len(summary) > 0:
                return summary[0]['summary_text']
            else:
                return "요약이 생성되지 않았습니다."
        except Exception as e:
            return f"요약 오류: {str(e)}"
    else:
        return "본문이 너무 짧아 요약 불가"


# 출력 함수
def fetch_news_summaries(keywords, start_date, end_date):
    for keyword in keywords:
        print(f"=== {keyword}에 대한 뉴스 ===")
        urls = get_news_urls(keyword, start_date, end_date)

        for title, link, date in urls:
            print(f"\n기사 제목: {title}")
            print(f"기사 날짜: {date}")
            print(f"원문 링크: {link}")
            summary = get_article_summary(link)
            print(f"기사 요약: {summary}")

# 날짜 설정
start_date = datetime.strptime("2024-10-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-10-03", "%Y-%m-%d")

# 키워드 설정
keywords = ["AI", "AGI"]

# 기사 요약 출력
fetch_news_summaries(keywords, start_date, end_date)