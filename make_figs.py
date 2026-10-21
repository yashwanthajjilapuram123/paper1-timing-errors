import numpy as np, pandas as pd, matplotlib.pyplot as plt, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from figstyle import *
style(); OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output') + '/'; os.makedirs(OUT, exist_ok=True)
M = ['Raw feed', 'Constant shift', 'ETSY', 'ELASTIC']
T2 = pd.DataFrame([
 ('Sprint (≥7.0 m·s⁻¹)', 7.470, [(18.487,13.9,23.8,12.217,None),(15.966,11.5,20.7,11.504,.281),(6.723,3.7,10.0,6.329,0),(2.101,0.4,4.1,1.271,0)]),
 ('High-speed running (≥5.5 m·s⁻¹)', 25.361, [(14.604,12.2,17.1,8.488,None),(12.129,9.8,14.4,8.031,.015),(4.455,3.0,5.8,6.763,0),(0.990,0.4,1.7,0.498,0)]),
 ('Sustained acceleration (≥2.5 m·s⁻², ≥0.5 s)', 29.881, [(24.790,22.2,27.4,11.496,None),(22.059,19.2,24.8,11.772,.140),(7.458,5.8,9.0,7.361,0),(1.155,0.5,1.9,1.155,0)]),
 ('Sustained acceleration (≥3.0 m·s⁻², ≥0.5 s)', 18.927, [(27.861,24.4,31.4,12.651,None),(24.212,20.9,27.9,13.774,.271),(9.619,7.4,12.1,7.155,0),(1.658,0.7,2.8,1.002,0)])],
 columns=['flag','base','vals'])

# ---------- Fig 1: schematic ----------
fig, ax = plt.subplots(figsize=(6.85, 2.3))
t = np.linspace(-6, 7.6, 700)
sp = 2.2 + 5.3*np.exp(-((t+0.6)**2)/0.9) + 0.4*np.sin(t*1.7)
ax.plot(t, sp, color=INK, lw=1.4)
ax.axhline(7.0, color=MUTED, lw=0.8, ls=(0,(4,3))); ax.text(7.55, 7.15, 'Sprint threshold 7.0 m·s⁻¹', ha='right', va='bottom', fontsize=6.8, color=MUTED)
for c, lab, col, ls in [(0, 'True event time\n(annotated)', OKABE['ELASTIC'], '-'), (2.8, 'Raw logged time\n(provider feed)', OKABE['Raw feed'], (0,(3,2)))]:
    ax.axvspan(c-2, c+2, color=col, alpha=0.10, lw=0)
    ax.axvline(c, color=col, lw=1.6, ls=ls)
    ax.text(c+0.12, 0.35, lab, color=col, fontsize=6.8, va='bottom', fontweight='bold')
ax.annotate('', xy=(2.8, 8.4), xytext=(0, 8.4), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
ax.text(1.4, 8.55, 'timing error = 2.8 s', ha='center', va='bottom', fontsize=7)
ax.text(-2.15, 5.2, 'Peak inside true window:\nsprint flagged', fontsize=6.6, color=OKABE['ELASTIC'], ha='right')
ax.text(4.9, 4.1, 'No peak inside raw window:\nsprint missed', fontsize=6.6, color=OKABE['Raw feed'], ha='left')
ax.set_xlim(-6, 7.6); ax.set_ylim(0, 9.4)
ax.set_xlabel('Time relative to true event (s)'); ax.set_ylabel('Player speed (m·s⁻¹)')
ax.grid(False)
fig.savefig(OUT+'Fig1_schematic.pdf'); fig.savefig(OUT+'Fig1_schematic.png', dpi=400); plt.close()

# ---------- Fig 3: forest plot misses + false alerts ----------
fig, axes = plt.subplots(4, 3, figsize=(6.85, 5.6), gridspec_kw=dict(width_ratios=[1.2, 1.05, 0.9], hspace=0.62, wspace=0.05))
for r, row in T2.iterrows():
    axm, axt, axf = axes[r]
    for k, (m, (mi, lo, hi, fa, p)) in enumerate(zip(M, row.vals)):
        y = 3 - k
        axm.plot([lo, hi], [y, y], color=OKABE[m], lw=1.6, solid_capstyle='round')
        axm.plot(mi, y, MARK[m], color=OKABE[m], ms=5.2, mec='white', mew=0.7, zorder=3)
        axt.text(0.02, y, f'{mi:.1f}% [{lo:.1f}–{hi:.1f}]', va='center', ha='left', fontsize=6.6)
        ptxt = 'ref.' if p is None else ('p<0.001' if p == 0 else f'p={p:.3f}')
        if p is not None and p >= 0.0042: ptxt += ' n.s.'
        axt.text(0.98, y, ptxt, va='center', ha='right', fontsize=6.3, color=MUTED)
        axf.barh(y, fa, color=OKABE[m], height=0.62, edgecolor='white', lw=0.6)
        axf.text(fa + 0.3, y, f'{fa:.1f}%', va='center', fontsize=6.6)
    for a in (axm, axt, axf):
        a.set_ylim(-0.6, 3.6)
    axt.set_xlim(0, 1); axt.axis('off')
    axm.set_yticks(range(4)); axm.set_yticklabels(M[::-1]); axm.grid(axis='y', visible=False)
    axf.set_yticks(range(4)); axf.set_yticklabels([]); axf.grid(axis='y', visible=False); axf.tick_params(axis='y', length=0)
    axm.set_xlim(0, 33); axf.set_xlim(0, 16.5)
    if r < 3: axm.set_xticklabels([]); axf.set_xticklabels([])
    axm.set_title(f'{row.flag}  ·  true flag rate {row.base:.1f}% of events', loc='left', fontsize=7.6, fontweight='bold', x=-0.33)
axes[-1,0].set_xlabel('True flags missed (%, 95% CI)'); axes[-1,2].set_xlabel('False alerts among raised flags (%)')
fig.text(0.99, 0.0, 'p: paired exact (McNemar) test vs raw feed; n.s. = not significant after Bonferroni correction (α = 0.0042). n = 3,186 events.', ha='right', fontsize=6, color=MUTED)
fig.savefig(OUT+'Fig3_flags_forest.pdf'); fig.savefig(OUT+'Fig3_flags_forest.png', dpi=400); plt.close()

# ---------- Fig 5: event-type heatmap ----------
T3 = pd.DataFrame({'n':[2126,198,125,119,108,107,100,60],
    'Raw feed':[0.72,0.94,0.60,0.08,0.86,1.48,0.78,0.84],'Constant shift':[0.72,0.80,0.52,0.52,0.78,1.60,0.66,0.54],
    'ETSY':[0.08,0.08,0.04,0.00,0.12,0.44,0.12,0.04],'ELASTIC':[0.0]*8},
    index=['Pass','Interception','Clearance','Throw-in','Tackle','Dispossessed','Bad touch','Shot'])
T3 = T3.sort_values('Raw feed', ascending=False)
V = T3[M].values
fig, ax = plt.subplots(figsize=(4.2, 3.0))
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('b', ['#F4F8FB', '#9CC3E0', '#2F6FA6', '#0B3A63'])
im = ax.imshow(V, cmap=cmap, vmin=0, vmax=1.6, aspect='auto')
for (i, j), v in np.ndenumerate(V):
    ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=6.8, color='white' if v > 0.9 else INK)
ax.set_xticks(range(4)); ax.set_xticklabels(M, rotation=0)
ax.set_yticks(range(len(T3))); ax.set_yticklabels([f'{n}  (n={c:,})' for n, c in zip(T3.index, T3.n)])
ax.tick_params(length=0); ax.grid(False)
for s in ax.spines.values(): s.set_visible(False)
ax.xaxis.tick_top()
cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03); cb.set_label('Median |timing error| (s)', fontsize=6.8); cb.ax.tick_params(labelsize=6.4); cb.outline.set_visible(False)
i = list(T3.index).index('Throw-in')
ax.add_patch(plt.Rectangle((-0.5, i-0.5), 2, 1, fill=False, ec=OKABE['Constant shift'], lw=1.4))
fig.savefig(OUT+'Fig5_event_type.pdf'); fig.savefig(OUT+'Fig5_event_type.png', dpi=400); plt.close()

# ---------- Fig 2 (summary, from known values): timing error thresholds by method ----------
TE = pd.DataFrame({'Median |error| (s)':[0.76,0.72,0.08,0.00],'>1 s':[39.2,35.4,11.4,2.1],'>2 s':[15.9,12.3,5.8,1.2]}, index=M)
fig, axes = plt.subplots(1, 2, figsize=(6.85, 1.9), gridspec_kw=dict(width_ratios=[1, 1.6], wspace=0.45))
ax = axes[0]
for k, m in enumerate(M):
    ax.barh(3-k, TE.loc[m,'Median |error| (s)'], color=OKABE[m], height=0.62)
    ax.text(TE.loc[m,'Median |error| (s)']+0.02, 3-k, f"{TE.loc[m,'Median |error| (s)']:.2f} s", va='center', fontsize=6.8)
ax.set_yticks(range(4)); ax.set_yticklabels(M[::-1]); ax.set_xlim(0, 1.0); ax.grid(axis='y', visible=False)
ax.set_xlabel('Median absolute timing error (s)'); panel(ax, 'A')
ax = axes[1]
w = 0.36
for k, m in enumerate(M):
    y = 3-k
    ax.barh(y+w/2, TE.loc[m,'>1 s'], height=w, color=OKABE[m], edgecolor='white', lw=0.5)
    ax.barh(y-w/2, TE.loc[m,'>2 s'], height=w, color=OKABE[m], alpha=0.45, edgecolor='white', lw=0.5, hatch='////')
    ax.text(TE.loc[m,'>1 s']+0.6, y+w/2, f"{TE.loc[m,'>1 s']:.1f}%  >1 s", va='center', fontsize=6.5)
    ax.text(TE.loc[m,'>2 s']+0.6, y-w/2, f"{TE.loc[m,'>2 s']:.1f}%  >2 s", va='center', fontsize=6.5, color=MUTED)
ax.set_yticks(range(4)); ax.set_yticklabels([]); ax.set_xlim(0, 52); ax.grid(axis='y', visible=False)
ax.set_xlabel('Events exceeding error threshold (%)'); panel(ax, 'B')
fig.savefig(OUT+'Fig2_timing_summary.pdf'); fig.savefig(OUT+'Fig2_timing_summary.png', dpi=400); plt.close()
print('ok')
