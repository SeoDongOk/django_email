import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


def getData():
  url = "https://www.jobkorea.co.kr/Search/?stext=%EC%82%B0%EC%97%85%EA%B8%B0%EB%8A%A5%EC%9A%94%EC%9B%90&local=I000&duty=1000229%2C1000230%2C1000231%2C1000232&tabType=recruit&Page_No=1"

  res=requests.get(url)
  res.encoding = 'utf-8'
  soup=BeautifulSoup(res.text,"html.parser")
  target = []
  base_url = "https://www.jobkorea.co.kr/"

  # Assuming soup is already defined and contains parsed HTML
  for i in soup.find_all("article", class_="list-item"):
      company = i.find("a", class_="corp-name-link dev-view")
      text = i.find("div", class_="information-title")
      
      if company is None:  # Check if the company element is None
          continue

      company_name = re.sub("\n", "", company.text.strip())
      job_title = re.sub("\n", "", text.text.strip())
      
      target.append({
          "업로드위치": base_url,
          "공고명": job_title,
          "공고회사": company_name,
          "공고주소": base_url + company.attrs["href"]
      })

  df = pd.DataFrame(target)
  return df