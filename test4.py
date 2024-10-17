import requests
from bs4 import BeautifulSoup
import time

# 뉴스 검색 및 스크래핑 함수
def search_naver_news(keyword, max_results=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=&de=&docid=&nso=so:r,p:from20200101to20241231,a:all&mynews=0&refresh_start=0&related=0"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.select('ul.list_news li.bx')
    
    results = []
    titles_seen = set()  # 중복 제거용
    
    for i, article in enumerate(articles[:max_results]):
        title_tag = article.select_one('a.news_tit')
        title = title_tag.text.strip()
        
        # 중복된 제목 필터링
        if title in titles_seen:
            continue
        
        link = title_tag['href']
        summary = article.select_one('a.api_txt_lines').text.strip()
        date = article.select_one('span.info').text.strip()
        
        titles_seen.add(title)
        
        # 요약된 본문 스크래핑
        summary_content = get_summary_content(link)
        
        results.append({
            'title': title,
            'summary': summary_content,
            'date': date,
            'link': link
        })
        
        if len(results) == max_results:
            break
    
    return results

# 네이버 뉴스 본문 요약 스크래핑
def get_summary_content(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 요약된 본문 추출 (본문 요약봇에 해당하는 영역이 있을 경우)
    summary_section = soup.find('div', {'id': '_SUMMARY_BUTTON'})
    
    if summary_section:
        summary = summary_section.text.strip()
    else:
        summary = "요약된 내용을 찾을 수 없습니다."
    
    return summary

# 결과를 텍스트 파일로 저장
def save_to_txt(filename, articles):
    with open(filename, 'w', encoding='utf-8') as f:
        for article in articles:
            f.write(f"제목: {article['title']}\n")
            f.write(f"내용: {article['summary']}\n")
            f.write(f"발행 일자: {article['date']}\n")
            f.write(f"링크: {article['link']}\n")
            f.write('\n' + '-'*80 + '\n')

# 검색 및 저장 실행
if __name__ == "__main__":
    keyword = input("검색할 키워드를 입력하세요: ")
    articles = search_naver_news(keyword)
    
    if articles:
        filename = f"{keyword}_news.txt"
        save_to_txt(filename, articles)
        print(f"{filename} 파일로 저장되었습니다.")
    else:
        print("기사를 찾을 수 없습니다.")
