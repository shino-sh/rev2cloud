# -*- coding:utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag
import os
import re
import sys
import time
import urllib2

def get_reviews(item_id, page):

  res = {}
  res["reviews"] = []

  review_url = "http://www.amazon.co.jp/product-reviews/"+item_id+"/ref=cm_cr_pr_top_link_2?ie=UTF8&pageNumber="+str(page)+"&showViewpoints=0&sortBy=byRankDescending"
  print 'urlopen : page=' + str(page)
  print review_url
  response = urllib2.urlopen(review_url)
  soup = BeautifulSoup(response, fromEncoding='shift-jis')

  #print soup.prettify()
  for span_review in soup.findAll("span", {"class":"a-size-base review-text"}):
    rev = [item if str(item)!='<br />' else '\n' for item in span_review.contents]
    rev = [r.text if isinstance(r, Tag) else r for r in rev]
    res["reviews"].append(''.join(rev))

  time.sleep(3)

  return res

# for unit module
if __name__ == '__main__':

  if (len(sys.argv) != 2):
    print 'Usage: python %s [item_id]' % sys.argv[0]
    quit()

  item_id = sys.argv[1] # B00U2EXR4A

  res = get_reviews(item_id,1)  
  
  for i, review in enumerate(res["reviews"]):
    print 'Review ' + str(i+1) + ':\n\t' + review
    print

