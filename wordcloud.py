#coding:utf-8

import sys
import MeCab
import amazon
from sklearn.feature_extraction.text import TfidfVectorizer

def tokenize(text):
  tagger = MeCab.Tagger("-Ochasen")
  nouns = []

  node = tagger.parseToNode(text)
  while node:
    noun = node.feature.split(",")[0]
    if noun == r'名詞' and not node.surface.isdigit():
      nouns.append(node.surface)
    node = node.next

  return ' '.join(nouns)

def getNoun(reviews):
  nouns = {}

  tokenized_reviews = [tokenize(rev.encode('utf-8')) for rev in reviews]

  tfidf = TfidfVectorizer()
  tfs = tfidf.fit_transform(tokenized_reviews)

  feature_names = tfidf.get_feature_names()

  dic = {}
  for i, v in enumerate(tokenized_reviews):
    d = dict(zip(feature_names, tfs[i].toarray()[0]))
    score = [(x, d[x]) for x in sorted(d, key=lambda x:-d[x])]
    dic[i] = score

  res = {}
  for d in dic.items():
    for n in d[1]:
      res.setdefault(n[0], 0.0)
      res[n[0]] += n[1]

  return res

# for unit module
if __name__ == '__main__':
  if(len(sys.argv) != 2):
    print 'Usage: python %s [item_id]' % sys.argv[0]
    quit()

  item_id = sys.argv[1]

  res = amazon.get_reviews(item_id, 1)
  nouns = getNoun(res["reviews"])

  for n in nouns.items():
    print n[0], n[1]
