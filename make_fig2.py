"""Figure 2: distribution of timing errors, built directly from the per-event data.

Input : timing_errors_per_event.csv (exported by Cell 14 of paper1_reproduce.ipynb)
Output: figs/Fig2_timing_summary.pdf / .png
"""
import os, sys
import numpy as np, pandas as pd, matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from figstyle import *

style()
CSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data', 'timing_errors_per_event.csv')
OUT = os.path.join(HERE, 'output') + '/'
os.makedirs(OUT, exist_ok=True)
M = ['Raw feed', 'Constant shift', 'ETSY', 'ELASTIC']
LIM = 4.0

d = pd.read_csv(CSV)
rng = np.random.default_rng(1)
fig, (axA, axB) = plt.subplots(1, 2, figsize=(6.85, 2.7), gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.28))

# A: every event (jittered strip) + box plot (median, IQR, 5th-95th percentiles)
for k, m in enumerate(M):
    x = d[m].dropna().to_numpy()
    y = 3 - k
    out = np.abs(x) > LIM
    xs = x[~out]
    axA.scatter(xs, y + 0.13 + rng.uniform(-0.17, 0.17, xs.size), s=1.2, color=OKABE[m], alpha=0.35, lw=0, rasterized=True)
    axA.boxplot([x], positions=[y - 0.22], orientation='horizontal', widths=0.16, whis=(5, 95), showfliers=False,
                medianprops=dict(color=INK, lw=1.3), boxprops=dict(color=INK, lw=0.7),
                whiskerprops=dict(color=INK, lw=0.7), capprops=dict(color=INK, lw=0.7))
    axA.text(-LIM + 0.05, y + 0.42, f'n = {x.size:,}; {out.sum()} events beyond ±{LIM:g} s not shown',
             fontsize=5.6, color=MUTED, va='bottom',
             bbox=dict(facecolor='white', edgecolor='none', pad=0.6))
axA.axvline(0, color=MUTED, lw=0.6, ls=(0, (2, 2)))
axA.set_yticks(range(4)); axA.set_yticklabels(M[::-1]); axA.set_ylim(-0.55, 3.75)
axA.set_xlim(-LIM, LIM); axA.grid(axis='y', visible=False)
axA.set_xlabel('Timing error: timestamp minus true frame (s)')
panel(axA, 'A')

# B: cumulative percentage of events within each absolute error
grid = np.linspace(0, 3, 601)
for m in M:
    a = np.sort(np.abs(d[m].dropna().to_numpy()))
    axB.plot(grid, np.searchsorted(a, grid, side='right') / a.size * 100, color=OKABE[m], lw=1.5,
             ls={'Raw feed': '-', 'Constant shift': (0, (4, 1.5)), 'ETSY': (0, (6, 1.5, 1.5, 1.5)), 'ELASTIC': '-'}[m], label=m)
for v in (1, 2):
    axB.axvline(v, color=MUTED, lw=0.6, ls=(0, (1, 2)))
axB.set_xlim(0, 3); axB.set_ylim(0, 100)
axB.set_xlabel('Absolute timing error (s)'); axB.set_ylabel('Events within error (%)')
axB.legend(loc='lower right', fontsize=6.4)
panel(axB, 'B')

fig.savefig(OUT + 'Fig2_timing_summary.pdf', dpi=400)
fig.savefig(OUT + 'Fig2_timing_summary.png', dpi=400)
plt.close()

# Printed check values (should match the manuscript)
for m in M:
    a = d[m].dropna().abs()
    print(f'{m:15s} n={a.size:5d} median={a.median():.2f} s  >1 s={(a > 1).mean()*100:.1f}%  >2 s={(a > 2).mean()*100:.1f}%')
