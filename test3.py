import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 검색할 키워드
keywords = ["AI", "LLMOps", "AGI"]
# 검색 기간 설정
start_date = "2024-10-02"
end_date = "2024-10-03"
# 가져올 기사 수 상위 5개
top_n = 5

# 네이버 뉴스 URL 템플릿
base_url = "https://search.naver.com/search.naver"
params = {
    "where": "news",
    "sm": "tab_jum",
    "query": "",  # 검색어를 나중에 입력
    "ds": start_date,
    "de": end_date,
    "nso": f"so:r,p:from{start_date.replace('-', '')}to{end_date.replace('-', '')},a:all"
}

def get_news_data(query):
    params['query'] = query
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 뉴스 기사를 담을 리스트
    news_list = []
    
    # 뉴스 기사를 크롤링
    articles = soup.select("ul.list_news > li")[:top_n]  # 상위 top_n개의 기사만 추출
    
    for article in articles:
        title = article.select_one("a.news_tit").get_text()
        link = article.select_one("a.news_tit")["href"]
        summary = article.select_one(".dsc_txt_wrap").get_text()
        date = article.select_one(".info_group > span").get_text()

        # 데이터 정리
        news_item = {
            "title": title,
            "summary": summary,
            "link": link,
            "date": date
        }
        news_list.append(news_item)
    
    return news_list

def save_to_txt(news_data, filename="news_results.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for keyword, articles in news_data.items():
            f.write(f"--- Keyword: {keyword} ---\n\n")
            for idx, article in enumerate(articles, 1):
                f.write(f"{idx}. Title: {article['title']}\n")
                f.write(f"   Summary: {article['summary']}\n")
                f.write(f"   Link: {article['link']}\n")
                f.write(f"   Date: {article['date']}\n\n")

# 메인 실행 코드
if __name__ == "__main__":
    all_news_data = {}
    
    # 키워드별로 뉴스 검색
    for keyword in keywords:
        print(f"Searching for {keyword}...")
        news_data = get_news_data(keyword)
        all_news_data[keyword] = news_data

    # 결과를 텍스트 파일로 저장
    save_to_txt(all_news_data)
    print("Results saved to news_results.txt")