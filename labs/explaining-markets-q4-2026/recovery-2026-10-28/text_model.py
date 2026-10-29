"""Local statistical candidate — Oladapo Olaniyan, FIN-43900."""
import re,hashlib
from collections import Counter
import numpy as np
from scipy.sparse import csr_matrix,diags
from scipy.sparse.linalg import lsqr

class RidgeTextModel:
    def __init__(self,alpha=1.0,dimensions=32768):
        self.alpha=alpha;self.dimensions=dimensions
    def counts(self,documents):
        rows=[];cols=[];values=[]
        for i,doc in enumerate(documents):
            words=re.findall(r'[a-z]+|[+-]?\d+(?:\.\d+)?',doc.lower())
            terms=words+[' '.join(x) for x in zip(words,words[1:])]
            counts=Counter(int.from_bytes(hashlib.blake2b(t.encode(),digest_size=4).digest(),'little')%self.dimensions for t in terms)
            for j,count in counts.items():rows.append(i);cols.append(j);values.append(1+np.log(count))
        return csr_matrix((values,(rows,cols)),shape=(len(documents),self.dimensions))
    def transform(self,documents):
        x=self.counts(documents).multiply(self.idf)
        norm=np.sqrt(np.asarray(x.multiply(x).sum(axis=1)).ravel())
        return diags(1/np.maximum(norm,1e-12))@x
    def fit(self,documents,target):
        x=self.counts(documents);df=np.asarray((x!=0).sum(axis=0)).ravel()
        self.idf=np.log((1+len(documents))/(1+df))+1
        self.mean=float(np.mean(target));x=self.transform(documents)
        self.weights=lsqr(x,np.asarray(target)-self.mean,damp=np.sqrt(self.alpha),atol=1e-6,btol=1e-6,iter_lim=200)[0]
        return self
    def predict(self,documents):
        return np.clip(self.mean+self.transform(documents)@self.weights,0,1)
