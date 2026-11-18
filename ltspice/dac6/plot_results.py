import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_results import analyse,mean_window,LSB
from reportlab.graphics.shapes import Drawing,String,Rect
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderSVG
from reportlab.lib import colors
summary,runs,rows=analyse();r=runs['DAC6_Top'];O=Path(__file__).resolve().parent / 'docs'
d=Drawing(1400,1100);d.add(Rect(0,0,1400,1100,fillColor=colors.HexColor('#f6f8fc'),strokeColor=None))
def txt(x,y,s,size=15,col='#24334b'):
 d.add(String(x,y,s,fontName='Helvetica',fontSize=size,fillColor=colors.HexColor(col)))
txt(48,1050,'Buffered 6-bit resistor-string DAC',30);txt(48,1018,'LTspice 26.1.1 | 3.3 V analogue / 1.8 V logic | 100 kohm + 20 pF nominal load',17)
cols=['#176bb5','#d35920','#418749','#9156ae']
def panel(x,y,title,subtitle,data,labels,xrange,yrange,xlabel):
 d.add(Rect(x,y,636,430,rx=14,ry=14,fillColor=colors.white,strokeColor=colors.HexColor('#dbe3ef')))
 txt(x+24,y+395,title,20);txt(x+24,y+367,subtitle,13)
 lp=LinePlot();lp.x=x+64;lp.y=y+70;lp.width=540;lp.height=264
 lp.data=data;lp.joinedLines=1
 lp.xValueAxis.valueMin,lp.xValueAxis.valueMax=xrange;lp.yValueAxis.valueMin,lp.yValueAxis.valueMax=yrange
 lp.xValueAxis.labels.fontSize=11;lp.yValueAxis.labels.fontSize=11
 lp.xValueAxis.visibleGrid=1;lp.yValueAxis.visibleGrid=1
 lp.xValueAxis.gridStrokeColor=colors.HexColor('#e7edf5');lp.yValueAxis.gridStrokeColor=colors.HexColor('#e7edf5')
 for i in range(len(data)):lp.lines[i].strokeColor=colors.HexColor(cols[i]);lp.lines[i].strokeWidth=1.6
 d.add(lp);txt(x+270,y+43,xlabel,12);txt(x+20,y+335,'V',12)
 for i,label in enumerate(labels):txt(x+24+i*200,y+18,label,12,cols[i])
def wave(run,s,a,b,maxpoints=3500):
 pts=[(t*1000,v) for t,v in zip(run['time'],run[s]) if a<=t<=b]
 if len(pts)>maxpoints:
  # Preserve extrema of each time bin so brief disturbances stay visible.
  z=[];step=max(1,len(pts)//(maxpoints//4))
  for i in range(0,len(pts),step):
   p=pts[i:i+step];z+=sorted(set([p[0],p[-1],min(p,key=lambda q:q[1]),max(p,key=lambda q:q[1])]))
  pts=z
 return pts
panel(40,540,'All 64 codes and stress sequence','EN is low at startup and from 7.2 to 7.4 ms.',[wave(r,'v(tap)',0,.008),wave(r,'v(out)',0,.008)],['Selected tap','Buffered output'],(0,8),(0,3.15),'Time (ms)')
loaded=runs['DAC6_Tap_Load'];heavy=runs['DAC6_Heavy_Load']
series=[[(z['code'],z['output_V']) for z in rows]]
for rr in [loaded,heavy]:series.append([(i,mean_window(rr,'v(out)',i*1e-4+60e-6,i*1e-4+90e-6)) for i in range(64)])
panel(724,540,'Buffer and loading comparison','Failure tests: 100 kohm on tap; 1 kohm at output.',series,['Nominal','Direct tap load','Heavy output load'],(0,63),(0,3.15),'Input code')
panel(40,60,'Large jump: code 0 to 63','Output settles within +/-0.5 LSB in about 4.8 us.',[wave(r,'v(tap)',.006497,.006515),wave(r,'v(out)',.006497,.006515)],['Selected tap','Buffered output'],(6.497,6.515),(0,3.2),'Time (ms)')
panel(724,60,'Major carry: code 31 to 32','All six bits change; allow settling before sampling.',[wave(r,'v(tap)',.006797,.006815),wave(r,'v(out)',.006797,.006815)],['Selected tap','Buffered output'],(6.797,6.815),(0,3.2),'Time (ms)')
txt(48,28,'Functional model: equal resistors, generic CMOS and the supplied MCP6001 teaching model. These plots do not predict Sky130 silicon.',13)
renderSVG.drawToFile(d,str(O/'DAC6_Simulation.svg'))
print('PLOT written')
