from pathlib import Path
import re,struct
import numpy as np

def read_raw(path):
 b=Path(path).read_bytes();enc='utf-16-le' if b[:2] in [b'T\0',b'\xff\xfe'] else 'utf-8-sig';ee='utf-16-le' if enc=='utf-16-le' else 'utf-8'
 marker='Binary:\n'.encode(ee)
 if marker not in b:marker='Binary:\r\n'.encode(ee)
 pos=b.index(marker);h=b[:pos].decode(enc);body=b[pos+len(marker):]
 names=re.findall(r'^\s*\d+\s+(\S+)\s+\S+',h,re.M);n=int(re.search(r'No\. Variables:\s*(\d+)',h).group(1));p=int(re.search(r'No\. Points:\s*(\d+)',h).group(1));flags=re.search(r'Flags:\s*(.*)',h).group(1)
 if 'complex' in flags:
  z=np.frombuffer(body,dtype='<c16').reshape(p,n);return {name.lower():z[:,i] for i,name in enumerate(names)}
 size=8 if len(body)==p*n*8 else 4
 if 'FastAccess' in flags:
  ans={names[0].lower():np.frombuffer(body,dtype='<f8',count=p)}
  for i in range(1,n):ans[names[i].lower()]=np.frombuffer(body,dtype='<f'+str(size),count=p,offset=p*(8+(i-1)*size))
  return ans
 dtype=np.dtype([('axis','<f8'),('values','<f'+str(size),(n-1,))]);z=np.frombuffer(body,dtype=dtype,count=p)
 return {name.lower():(z['axis'] if i==0 else z['values'][:,i-1]) for i,name in enumerate(names)}
