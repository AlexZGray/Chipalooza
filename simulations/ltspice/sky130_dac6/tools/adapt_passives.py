import re

def adapt_passives(t):
 # LTspice does not accept ngspice c= or tc1/tc2 spelling on these primitives.
 # Explicit temperature multiplication also works on voltage-dependent resistors.
 lines=[]
 for line in t.splitlines():
  if line.startswith('+') and lines and re.match(r'^r\S*\s',lines[-1],re.I):lines[-1]+=' '+line[1:].strip()
  else:lines.append(line)
 out=[]
 for ln in lines:
  if re.match(r'^r\S*\s',ln,re.I):
   a=re.search(r'\s+tc1\s*=\s*(\{[^}]+\}|\S+)\s+tc2\s*=\s*(\{[^}]+\}|\S+)',ln,re.I)
   if a:
    tc1,tc2=a.group(1).strip('{}'),a.group(2).strip('{}');ln=ln[:a.start()]+ln[a.end():]
    m=re.match(r'^(r\S+\s+\S+\s+\S+\s+)(?:r\s*=\s*)?(\{.*\}|\S+)\s*$',ln,re.I)
    if not m:raise ValueError(ln)
    val=m.group(2).strip('{}');ln=m.group(1)+'R={('+val+')*(1+('+tc1+')*(PDK_TEMP-27)+('+tc2+')*(PDK_TEMP-27)**2)}'
  if re.match(r'^c\S*\s',ln,re.I):
   ln=re.sub(r'^(c\S+\s+\S+\s+\S+\s+)c\s*=\s*',r'\1',ln,flags=re.I)
   ln=re.sub(r'\s+tc[12]\s*=\s*0(?:\.0)?\b','',ln,flags=re.I)
  out.append(ln)
 return '\n'.join(out)+'\n'
