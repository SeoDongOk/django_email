import pandas as pd
import requests
import re
import json
import numpy as np
from bs4 import BeautifulSoup


def getWanted():
  url = "https://www.wanted.co.kr/api/chaos/navigation/v1/results?1726455232533=&job_group_id=518&job_ids=10110&country=kr&job_sort=job.recommend_order&years=0&years=1&locations=seoul.all&attraction_tags=10445&limit=20"
  res=requests.get(url)
  res.encoding = 'utf-8'
  target = []
  base_url = "https://www.jobkorea.co.kr/"
  target = []
  base_url = "https://www.wanted.co.kr/"
  job_list=json.loads(res.text)

  for i in job_list['data']:
    company = i['company']['name']
    job_title=i["position"]
    target.append({
        "업로드위치": base_url,
        "공고명": job_title,
        "공고회사": company,
        "공고주소": base_url+ "wd/" + str(i["id"])
    })
  df = pd.DataFrame(target)
  return df


def getJobKorea(page):
  custom_header={
    "User-Agent":"PostmanRuntime/7.42.0",
    "Cookie":"GTMVars=b86daa8f8a80f8bb68260b0930f45617; GTMVarsFrom=NET:00:39:02; jobkorea=Site_Oem_Code=C1; sm=keyword=%ec%82%b0%ec%97%85%ea%b8%b0%eb%8a%a5%ec%9a%94%ec%9b%90; ASP.NET_SessionId=ly3vfa5nemwumsm4dzerotbj"
    }
  url = f"https://www.jobkorea.co.kr/Search/?stext=%EC%82%B0%EC%97%85%EA%B8%B0%EB%8A%A5%EC%9A%94%EC%9B%90&local=I000&duty=1000229%2C1000230%2C1000231%2C1000232&tabType=recruit&Page_No={page}"

  res=requests.get(url, headers=custom_header)
  res.encoding = 'utf-8'
  soup=BeautifulSoup(res.text,"html.parser")
  target = []
  base_url = "https://www.jobkorea.co.kr/"
  for i in soup.find_all("article", class_="list-item"):
    company = i.find("a", class_="corp-name-link dev-view")
    text = i.find("div", class_="information-title")
    if company is None:  
        continue
    if company is np.nan:
        continue
    if company.text.strip() is "Nan":
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
  print(target)
  return df

def getData():
  total_df=pd.DataFrame(index=["업로드위치","공고명","공고회사","공고주소"])
  for i in range(1,3):
    df = getJobKorea(i)
    total_df=pd.concat([total_df,df])
  wanted_df = getWanted()
  total_df = pd.concat([total_df,wanted_df])
  total_df.dropna(axis=0,inplace=True)
  return total_df