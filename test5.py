import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# 뉴스 데이터 크롤링 함수
def get_news_data(keyword, start_date="2024-10-02", end_date="2024-10-03", top_n=5):
    news_list = []
    
    # 검색 URL 및 파라미터 설정
    url = "https://search.naver.com/search.naver"
    params = {
        "where": "news",
        "query": keyword,
        "sort": "0",  # 관련성순으로 정렬
        "nso": f"so:r,p:from{start_date.replace('-', '')}to{end_date.replace('-', '')},a:all",
        "start": "1"
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 뉴스 기사 추출
    articles = soup.find_all("a", {"class": "news_tit"}, limit=top_n)
    
    for article in articles:
        title = article.get_text()
        link = article["href"]
        
        # 기사 발행일 추출 (대신 기사 링크 페이지에 들어가서 요약 가져오기)
        news_data = {
            "title": title,
            "link": link,
            "date": start_date  # (실제로는 날짜를 더 정확히 추출할 수도 있음)
        }
        
        # 기사 본문 요약 가져오기
        summary = get_summary_from_article(link)
        news_data["summary"] = summary
        news_list.append(news_data)
    
    return news_list

# 요약된 기사 내용 크롤링 함수
def get_summary_from_article(link):
    # Selenium 옵션 설정
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(link)
    time.sleep(2)  # 페이지 로딩을 기다림

    try:
        summary_element = driver.find_element(By.CLASS_NAME, "media_end_head_autosummary _auto_summary_wrapper")
        summary_text = summary_element.text.strip()
    except Exception as e:
        print(f"요약을 가져오지 못했습니다: {e}")
        summary_text = "요약 없음"
    
    driver.quit()
    return summary_text

# 메인 실행 코드
if __name__ == "__main__":
    keywords = ["AI", "LLMOps", "AGI"]
    start_date = "2024-10-02"
    end_date = "2024-10-03"

    all_news = []
    
    # 각 키워드별로 뉴스 가져오기
    for keyword in keywords:
        print(f"'{keyword}' 키워드에 대한 뉴스를 가져오는 중...")
        news_data = get_news_data(keyword, start_date, end_date)
        all_news.extend(news_data)  # 뉴스 데이터를 리스트에 추가
    
    # 중복된 기사 제거
    unique_news = {news['title']: news for news in all_news}.values()
    
    # 결과 txt 파일로 저장
    with open('news_summary.txt', 'w', encoding='utf-8') as f:
        for news in unique_news:
            f.write(f"기사 제목: {news['title']}\n")
            f.write(f"기사 요약: {news['summary']}\n")
            f.write(f"기사 링크: {news['link']}\n")
            f.write(f"기사 발행일: {news['date']}\n")
            f.write("\n" + "="*50 + "\n\n")
    
    print("크롤링 완료 및 결과가 'news_summary.txt'에 저장되었습니다.")
