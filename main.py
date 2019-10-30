'''
pip install requests beautifulsoup4 lxml flask
'''
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template_string

app = Flask(__name__)

def search_magnet():
    # Chrome 에서 얻어온 user-agent 값을 header(dic) 변수에 저장한다. (F12 -> Network -> F5(Refresh) -> search?.... -> Headers)
    # user-agent는 http 요청시 서버에 현재 브라우저를 알려주는 역학을 하며, requests를 통해 요청하여 받는 데이터가 Chrome의 검색결과와 동일하게 하기 위헤 세팅할 것이다.
    header = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    # Chrome 에서 '윈도우10 torrent' 키워드로 검색 후 출력되는 url에 불필요한 부분은 삭제한다. 
    # VS Code로 값을 복사하면 한글이 깨지기 때문에 keyword 변수에 '윈도우10' 스트링을 저장하여 넘겨준다.
    keyword = "윈도우10"
    url = "https://www.google.co.kr/search?hl=ko&source=hp&q={}+torrent&oq={}+torrent".format(keyword, keyword)
    r = requests.get(url, headers=header)
    bs = BeautifulSoup(r.content, "lxml")
    # BeautifulSoup의 select는 리스트 자료형으로 리턴을 한다. (데이터가 복수개가 될 수 있음을 의미함)
    # Google의 검색 결과는 <div class="g"> 에 저장되기 때문에 select로 div.g에 해당하는 값만 parsing 한다.
    divs = bs.select("div.g")

    magnets = []

    for d in divs:
        alink = d.select("div.r > a")[0]
        title = alink.select("h3")[0].text
        href = alink.get("href")

        r = requests.get(href)
        bs = BeautifulSoup(r.content, "lxml")
        all_links = bs.select("a")

        for a in all_links:
            g_link = a.get("href")
            # a 태그에 href 가 항상 있는건은 아니기 때문에 예외처리한다.
            if g_link is None:
                continue
            if g_link.find("magnet:?") >= 0:
                magnets.append({
                    "title": title,
                    "href": href,
                    "magnet": g_link,
                })
    return magnets

@app.route("/")
def index():
    magnets = search_magnet()
    HTML = '''
    {% for m in magnets %}
    <li><a href="{{m.magnet}}" target="_blank">{{m.title}}</a></li>
    {% endfor %}
    '''

    return render_template_string(HTML, **{"magnets": magnets})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=True)