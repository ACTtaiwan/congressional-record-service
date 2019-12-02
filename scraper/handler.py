import boto3
import json
import requests
from bs4 import BeautifulSoup
import datetime

top_selector = '.basic-search-results-lists.expanded-view'
heading_selector = '.result-heading'
title_selector = '.result-title'
item_selector = '.result-item'

def scrape(event, context):
  data = bills_scrape()
  file_name = f"cr-{data['date']}"
  save_file_to_s3('congressional-record', file_name, data)

def bills_scrape():
  page = requests.get("https://www.congress.gov/advanced-search/legislation?congresses%5B0%5D=116&congresses%5B1%5D=115&congresses%5B2%5D=114&congresses%5B3%5D=113&congresses%5B4%5D=112&congresses%5B5%5D=111&congresses%5B6%5D=110&congresses%5B7%5D=109&congresses%5B8%5D=108&congresses%5B9%5D=107&congresses%5B10%5D=106&congresses%5B11%5D=105&congresses%5B12%5D=104&congresses%5B13%5D=103&congresses%5B14%5D=102&congresses%5B15%5D=101&congresses%5B16%5D=100&congresses%5B17%5D=99&congresses%5B18%5D=98&congresses%5B19%5D=97&congresses%5B20%5D=96&congresses%5B21%5D=95&congresses%5B22%5D=94&congresses%5B23%5D=93&legislationNumbers=&restrictionType=includeBillText&restrictionFields%5B0%5D=allBillTitles&restrictionFields%5B1%5D=summary&summaryField=billSummary&enterTerms=Taiwan&wordVariants=true&legislationTypes%5B0%5D=hr&legislationTypes%5B1%5D=hres&legislationTypes%5B2%5D=hjres&legislationTypes%5B3%5D=hconres&legislationTypes%5B4%5D=hamdt&legislationTypes%5B5%5D=s&legislationTypes%5B6%5D=sres&legislationTypes%5B7%5D=sjres&legislationTypes%5B8%5D=sconres&legislationTypes%5B9%5D=samdt&legislationTypes%5B10%5D=suamdt&public=true&private=true&chamber=all&actionTerms=&legislativeActionWordVariants=true&dateOfActionOperator=equal&dateOfActionStartDate=&dateOfActionEndDate=&dateOfActionIsOptions=yesterday&dateOfActionToggle=multi&legislativeAction=Any&sponsorState=One&member=&sponsorTypes%5B0%5D=sponsor&sponsorTypes%5B1%5D=sponsor&sponsorTypeBool=OR&committeeActivity%5B0%5D=0&committeeActivity%5B1%5D=3&committeeActivity%5B2%5D=11&committeeActivity%5B3%5D=12&committeeActivity%5B4%5D=4&committeeActivity%5B5%5D=2&committeeActivity%5B6%5D=5&committeeActivity%5B7%5D=9&satellite=%5B%5D&search=&submitted=Submitted&searchResultViewType=expanded&pageSize=250&pageSort=latestAction%3Adesc&q=%7B%22type%22%3A%22bills%22%2C%22congress%22%3A116%7D")
  content = BeautifulSoup(page.content, 'html.parser')
  bills = content.select(top_selector)[0]
  heading = bills.select(heading_selector)[0].get_text()
  title = bills.select(title_selector)[0].get_text()
  item = bills.select(item_selector)[2].get_text()
  return {
    'Bill Number': heading,
    'Bill Name': title,
    'Latest Action:': item.split(':')[1].split('(')[0].strip()
  }

def save_file_to_s3(bucket, file_name, data):
  s3 = boto3.resource('s3')
  obj = s3.Object(bucket, file_name)
  obj.put(Body=json.dumps(data))

def main():
  print(bills_scrape())

if __name__ == "__main__":
  main()