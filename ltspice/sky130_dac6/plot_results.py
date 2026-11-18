#!/usr/bin/env python3
"""Render standalone scientific figures from the committed measurement CSV files."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent;R=B/'results';D=B/'docs'
def data(name):
 with (R/name).open() as f:return {k:np.array([float(q[k]) for q in rows]) for rows in [list(csv.DictReader(f))] for k in rows[0]}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.22,'figure.facecolor':'white','axes.titlesize':12,'savefig.facecolor':'white'})
fig,axes=plt.subplots(2,2,figsize=(12,8.2),layout='constrained')
ax=axes[0,0]
for name,label in [('Top','TT nominal'),('Min_Supply','SS / hot / low supply'),('Hot_Fast','FF / hot'),('Cold_Skew','SF / cold')]:
 q=data('reference_'+name+'_codes.csv');ax.plot(q['code'],q['error_LSB']*42.1875,label=label,lw=1.8)
ax.set(xlabel='DAC code',ylabel='Output error (mV)',title='Complete DAC: settled transfer error',xlim=(0,63),ylim=(-1,1));ax.legend(fontsize=8);ax.text(.02,.04,'0.5 LSB = 21.09 mV',transform=ax.transAxes,fontsize=9)
q=data('reference_step.csv');ax=axes[0,1]
ax.plot(q['time_us'],q['nominal_V'],label='TT nominal',lw=2);ax.plot(q['time_us'],q['low_supply_V'],label='SS / hot / low supply',lw=2)
ax.axhspan(2.9578125-.5*2.7/64,2.9578125+.5*2.7/64,color='gray',alpha=.25);ax.axvline(20,color='black',ls=':',lw=1)
ax.set(xlabel='Time after data update (µs)',ylabel='Output (V)',title='Large step into 100 kΩ / 20 pF',xlim=(0,25),ylim=(.2,3.1));ax.legend(loc='lower right',fontsize=9)
q=data('reference_range_envelope.csv')
for ax,pre,title in [(axes[1,0],'lower','Lower-rail tracking envelope'),(axes[1,1],'upper','Upper-rail tracking envelope')]:
 x=q['headroom_V']*1000;ax.fill_between(x,q[pre+'_min_mV'],q[pre+'_max_mV'],alpha=.28,color='#16689f',label='85 range runs')
 ax.plot(x,q[pre+'_min_mV'],lw=1,color='#16689f');ax.plot(x,q[pre+'_max_mV'],lw=1,color='#16689f')
 ax.axhline(5,color='gray',ls='--',lw=1);ax.axhline(-5,color='gray',ls='--',lw=1);ax.axvline(100,color='black',ls=':',lw=1.4,label='100 mV allowance')
 ax.set(xlabel='Clearance from rail (mV)',ylabel='Output − input (mV)',title=title,xlim=(0,200),ylim=(-20,20));ax.legend(loc='upper right',fontsize=8)
for ext in ['png','svg']:fig.savefig(D/('Results_Overview.'+ext),dpi=180)
plt.close(fig)
q=data('reference_bode.csv');fig,(a,b)=plt.subplots(2,1,figsize=(10,7),sharex=True,layout='constrained')
for prefix,label,color in [('nominal','TT nominal','#16689f'),('corner','FS / RC-LL / 110 °C / low supply-bias','#d56a21')]:
 a.semilogx(q['frequency_Hz'],q[prefix+'_dB'],label=label,color=color,lw=1.8);b.semilogx(q['frequency_Hz'],q[prefix+'_phase_deg'],color=color,lw=1.8)
a.axhline(0,color='gray',ls='--',lw=1);b.axhline(-180,color='gray',ls='--',lw=1)
a.set(ylabel='Loop gain (dB)',title='Sky130 physical buffer: loop gain at 1.65 V input',ylim=(-55,100));a.legend(fontsize=9)
b.set(xlabel='Frequency (Hz)',ylabel='Phase (degrees)',xlim=(1,1e8),ylim=(-270,0))
for ext in ['png','svg']:fig.savefig(D/('Loop_Gain.'+ext),dpi=180)
plt.close(fig)
print('Wrote Results_Overview and Loop_Gain PNG/SVG figures')
