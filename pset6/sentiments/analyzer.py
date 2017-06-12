from nltk import TweetTokenizer
d=dict()
class Analyzer():
    def __init__(self, positives, negatives):
         fp=open(positives,"r")
         for line in fp:
             if not line.startswith(";"):
                   d[line.strip()]=1
         fp.close()
         fp=open(negatives,"r")
         for line in fp:
             if not line.startswith(";"):
                   d[line.strip()]=-1
         fp.close()           
                  
    def analyze(self, text):
        s=0
        li=TweetTokenizer().tokenize(text)
        for w in li:
            w.lower
            if(w in d):
               s=s+d[w]
        return s     

