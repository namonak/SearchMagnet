'''
pip install requests beautifulsoup4 lxml
'''
import requests
from bs4 import BeautifulSoup

# Chrome 에서 얻어온 user-agent 값을 header(dic) 변수에 저장한다. (F12 -> Network -> F5(Refresh) -> search?.... -> Headers)
# user-agent는 http 요청시 서버에 현재 브라우저를 알려주는 역학을 하며, requests를 통해 요청하여 받는 데이터가 Chrome의 검색결과와 동일하게 하기 위헤 세팅할 것이다.
header = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
# Chrome 에서 '윈도우10 torrent' 키워드로 검색 후 출력되는 url에 불필요한 부분은 삭제한다. 
# VS Code로 값을 복사하면 한글이 깨지기 때문에 keyword 변수에 '윈도우10' 스트링을 저장하여 넘겨준다.
keyword = "윈도우10"
url = "https://www.google.co.kr/search?hl=ko&source=hp&q={}+torrent&oq={}+torrent".format(keyword, keyword)
r = requests.get(url, headers=header)
bs = BeautifulSoup(r.content, "lxml")
# BeautifulSoup의 Select는 리스트 자료형으로 리턴을 한다. (데이터가 복수개가 될 수 있음을 의미함)
divs = bs.select("div.g")

for d in divs:
    print(d)
    print("\n")