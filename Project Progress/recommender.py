"""Phase I: basic TF-IDF document search, no external API required."""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT=Path(__file__).resolve().parent
STOPWORDS='a an and are as at be been before by can do does for from has have how i if in into is it its may must of on or our should that the their them then there these they this to use was we were what when which who why will with you your'.split()

def clean(text):
    """Normalize case, accents, and special characters before tokenization."""
    text=unicodedata.normalize('NFKD',str(text)).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9\s]',' ',text)

def load_corpus(path=ROOT/'corpus.csv'):
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(f'Corpus not found: {path}')
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if not {'id','title','text'}<=set(reader.fieldnames or []):
            raise ValueError('Corpus requires id, title and text columns')
        docs=list(reader)
    if len(docs)<6:raise ValueError('At least six documents are required for Top-5 by ID')
    if any(not all(d.get(k,'').strip() for k in ('id','title','text')) for d in docs):
        raise ValueError('Empty document fields are not allowed')
    if len({d['id'] for d in docs})!=len(docs):raise ValueError('Duplicate document identifiers')
    return docs

def make_vectorizer():
    return TfidfVectorizer(preprocessor=clean,stop_words=STOPWORDS,
        token_pattern=r'(?u)\b[a-z0-9]{2,}\b',ngram_range=(1,2),sublinear_tf=True)

class Recommender:
    def __init__(self,path=ROOT/'corpus.csv'):
        self.docs=load_corpus(path)
        self.by_id={d['id']:i for i,d in enumerate(self.docs)}
        self.vectorizer=make_vectorizer()
        self.matrix=self.vectorizer.fit_transform([d['text'] for d in self.docs])

    def recommend(self,doc_id=None,query=None,k=5):
        if (doc_id is None)==(query is None):raise ValueError('Supply exactly one ID or query')
        if not isinstance(k,int) or k<1:raise ValueError('k must be a positive integer')
        seed=None
        if doc_id is not None:
            if doc_id not in self.by_id:raise ValueError(f'Unknown document ID: {doc_id}')
            seed=self.by_id[doc_id];vector=self.matrix[seed]
        else:
            if not query or not query.strip():raise ValueError('The query cannot be empty')
            vector=self.vectorizer.transform([query])
        scores=cosine_similarity(vector,self.matrix).ravel()
        # Deterministic identifier tie-breaks make browser/Python results comparable.
        order=sorted((i for i in range(len(self.docs)) if i!=seed),
                     key=lambda i:(-float(scores[i]),self.docs[i]['id']))[:k]
        return [dict(self.docs[i],score=float(scores[i])) for i in order]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--id',dest='doc_id');g.add_argument('--query')
    p.add_argument('--corpus',type=Path,default=ROOT/'corpus.csv')
    p.add_argument('--json',action='store_true');a=p.parse_args()
    try:results=Recommender(a.corpus).recommend(a.doc_id,a.query)
    except (ValueError,FileNotFoundError) as exc:p.exit(2,f'Error: {exc}\n')
    if a.json:print(json.dumps(results,indent=2))
    else:
        print(f'Input: {a.doc_id or a.query}')
        for n,d in enumerate(results,1):print(f"{n}. {d['id']}  {d['score']:.6f}  {d['title']}")

if __name__=='__main__':main()
