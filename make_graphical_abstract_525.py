"""Graphical abstract sized for Taylor & Francis (maximum width 525 px)."""
import os, sys
import numpy as np, matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from figstyle import *
style()
plt.rcParams.update({'savefig.bbox': 'standard', 'font.size': 9, 'axes.labelsize': 9, 'xtick.labelsize': 8.5, 'ytick.labelsize': 8.5})
OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'figs')
os.makedirs(OUT, exist_ok=True)

fig = plt.figure(figsize=(5.25, 3.5), dpi=100)
fig.text(0.5, 0.975, 'Raw event timestamps miss short, intense efforts', ha='center', va='top', fontsize=11, fontweight='bold')
fig.text(0.5, 0.905, '3 elite football matches · 3,186 events · frame-level ground truth', ha='center', va='top', fontsize=8.5, color=MUTED)
gs = fig.add_gridspec(1, 2, left=0.25, right=0.97, top=0.78, bottom=0.30, wspace=0.55, width_ratios=[1.25, 1])

ax = fig.add_subplot(gs[0])
flags = ['Sprint', 'High-speed run', 'Sust. accel 2.5', 'Sust. accel 3.0']
raw = [18.5, 14.6, 24.8, 27.9]; el = [2.1, 1.0, 1.2, 1.7]
y = np.arange(4)[::-1]
for yi, a, d in zip(y, raw, el):
    ax.plot([d, a], [yi, yi], color='#D5D5D5', lw=3.5, solid_capstyle='round', zorder=1)
ax.scatter(raw, y, s=48, marker='o', color=OKABE['Raw feed'], edgecolor='white', lw=0.6, zorder=3, label='Raw feed')
ax.scatter(el, y, s=52, marker='^', color=OKABE['ELASTIC'], edgecolor='white', lw=0.6, zorder=3, label='Synchronised (ELASTIC)')
for yi, a in zip(y, raw):
    ax.text(a + 1.5, yi, f'{a:.1f}%', va='center', fontsize=8.5, color=OKABE['Raw feed'], fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(flags); ax.set_xlim(0, 37); ax.set_ylim(-0.6, 3.6)
ax.set_xlabel('True flags missed (%)'); ax.grid(axis='y', visible=False)
ax.legend(loc='upper center', bbox_to_anchor=(0.25, -0.24), ncol=2, fontsize=8, handletextpad=0.2, columnspacing=1.0)

ax = fig.add_subplot(gs[1])
lab = ['<0.2', '0.2–0.5', '0.5–1', '1–2', '2–4', '≥4']
S = [0.0, 2.6, 7.8, 22.2, 55.6, 62.5]; A = [1.1, 8.0, 13.1, 40.1, 67.5, 100.0]
x = np.arange(6)
ax.plot(x, S, 'o-', color=OKABE['Raw feed'], ms=4, lw=1.5, mec='white', mew=0.5, label='Sprint')
ax.plot(x, A, 's-', color=OKABE['Constant shift'], ms=4, lw=1.5, mec='white', mew=0.5, label='Sust. accel 3.0')
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=7.5, rotation=45, ha='right', rotation_mode='anchor')
ax.set_ylim(0, 105); ax.set_ylabel('Missed (%)'); ax.set_xlabel('Raw timing error (s)')
ax.legend(loc='upper left', fontsize=7.5); ax.grid(axis='x', visible=False)

fig.savefig(os.path.join(OUT, 'GraphicalAbstract1.png'), dpi=100, bbox_inches=None)
plt.close()
print('ok')
