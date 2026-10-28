#!/usr/bin/env python3
"""Compute blinded interrater agreement only after two completed genuine scoring sheets exist."""
import argparse,csv
AXES=['correctness','completeness','context','uncertainty_safety','evidence']
def kappa(a,b):
 if len(a)!=len(b) or not a:raise ValueError('Paired nonempty data required')
 from collections import Counter
 n=len(a);A=Counter(a);B=Counter(b)
 observed=sum(((x-y)/2)**2 for x,y in zip(a,b))/n
 expected=sum(((i-j)/2)**2*A[i]*B[j] for i in range(3) for j in range(3))/(n*n)
 return None if expected==0 else 1-observed/expected
def load(path):
 with open(path,encoding='utf8',newline='') as f:r=list(csv.DictReader(f))
 d={}
 for x in r:
  key=x['card_id']
  if not key or key in d:raise ValueError('Duplicate or absent card id')
  d[key]={a:int(x[a+'_0_2']) for a in AXES}
  if any(v not in (0,1,2) for v in d[key].values()):raise ValueError('Score outside 0-2')
 return d
def main():
 p=argparse.ArgumentParser();p.add_argument('scorer1');p.add_argument('scorer2');a=p.parse_args();x=load(a.scorer1);y=load(a.scorer2)
 if not x or x.keys()!=y.keys():raise ValueError('Scorer card sets differ or empty')
 for axis in AXES:
  z=kappa([x[k][axis] for k in x],[y[k][axis] for k in x]);print(axis,'n',len(x),'quadratic kappa','UNDEFINED' if z is None else round(z,4))
 print('Needs adjudication (>2 point total difference):',sum(abs(sum(x[k].values())-sum(y[k].values()))>2 for k in x))
if __name__=='__main__':main()
