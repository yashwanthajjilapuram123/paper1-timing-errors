import numpy as np, matplotlib.pyplot as plt, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from figstyle import *
style(); OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output') + '/'; os.makedirs(OUT, exist_ok=True)
fig = plt.figure(figsize=(6.85, 2.75))
gs = fig.add_gridspec(1, 3, width_ratios=[0.95, 1.45, 1.0], wspace=0.55)

# A: the problem
ax = fig.add_subplot(gs[0])
t = np.linspace(-4, 4, 400); sp = 2 + 5.4*np.exp(-((t+0.4)**2)/0.5)
ax.plot(t, sp, color=INK, lw=1.3)
ax.axhline(7, color=MUTED, lw=0.7, ls=(0,(3,2)))
ax.axvline(0, color=OKABE['ELASTIC'], lw=1.6); ax.axvline(2.4, color=OKABE['Raw feed'], lw=1.6, ls=(0,(3,2)))
ax.annotate('', xy=(2.4, 8.3), xytext=(0, 8.3), arrowprops=dict(arrowstyle='->', lw=0.9, color=INK))
ax.text(2.3, 8.75, 'logged late', ha='right', fontsize=6.6)
ax.text(-0.15, 0.4, 'true', color=OKABE['ELASTIC'], ha='right', fontsize=6.6, fontweight='bold')
ax.text(2.55, 0.4, 'raw', color=OKABE['Raw feed'], ha='left', fontsize=6.6, fontweight='bold')
ax.text(-3.9, 7.25, 'sprint', fontsize=6.2, color=MUTED)
ax.set_xlim(-4, 4); ax.set_ylim(0, 9.6); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
for s in ['left', 'bottom']: ax.spines[s].set_color('#BBBBBB')
ax.set_xlabel('time around event', fontsize=6.6); ax.set_ylabel('player speed', fontsize=6.6)
ax.set_title('A  The problem', loc='left', fontsize=8, fontweight='bold')

# B: dumbbell of misses
ax = fig.add_subplot(gs[1])
flags = ['Sprint', 'High-speed run', 'Sust. accel 2.5', 'Sust. accel 3.0']
raw = [18.5, 14.6, 24.8, 27.9]; sh = [16.0, 12.1, 22.1, 24.2]; et = [6.7, 4.5, 7.5, 9.6]; el = [2.1, 1.0, 1.2, 1.7]
y = np.arange(4)[::-1]
for yi, a, d in zip(y, raw, el):
    ax.plot([d, a], [yi, yi], color='#D5D5D5', lw=3, solid_capstyle='round', zorder=1)
for vals, m in [(raw, 'Raw feed'), (sh, 'Constant shift'), (et, 'ETSY'), (el, 'ELASTIC')]:
    ax.scatter(vals, y, s=34, marker=MARK[m], color=OKABE[m], edgecolor='white', lw=0.6, zorder=3, label=m)
for yi, a in zip(y, raw): ax.text(a + 1.2, yi, f'{a:.1f}%', va='center', fontsize=6.5, color=OKABE['Raw feed'], fontweight='bold')
for yi, d in zip(y, el): ax.text(d + 0.6, yi - 0.33, f'{d:.1f}%', va='center', ha='left', fontsize=6.2, color=OKABE['ELASTIC'], fontweight='bold')
ax.set_yticks(y); ax.set_yticklabels(flags); ax.set_xlim(0, 34); ax.set_ylim(-0.6, 3.5)
ax.set_xlabel('True flags missed (%)'); ax.grid(axis='y', visible=False)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.24), ncol=4, fontsize=6, handletextpad=0.2, columnspacing=0.8)
ax.set_title('B  What it does to load flags', loc='left', fontsize=8, fontweight='bold')

# C: dose response + message
ax = fig.add_subplot(gs[2])
lab = ['<0.2', '0.2–0.5', '0.5–1', '1–2', '2–4', '≥4']
S = [0.0, 2.6, 7.8, 22.2, 55.6, 62.5]; A = [1.1, 8.0, 13.1, 40.1, 67.5, 100.0]
x = np.arange(6)
ax.plot(x, S, 'o-', color=OKABE['Raw feed'], ms=3.5, lw=1.3, mec='white', mew=0.5, label='Sprint')
ax.plot(x, A, 's-', color=OKABE['Constant shift'], ms=3.5, lw=1.3, mec='white', mew=0.5, label='Sust. accel 3.0')
ax.set_xticks(x); ax.set_xticklabels(lab, rotation=40, ha='right', fontsize=6)
ax.set_ylim(0, 105); ax.set_ylabel('Missed (%)'); ax.set_xlabel('Raw timing error (s)', fontsize=6.8)
ax.legend(loc='upper left', fontsize=6); ax.grid(axis='x', visible=False)
ax.set_title('C  Bigger error, more misses', loc='left', fontsize=8, fontweight='bold')
fig.savefig(OUT + 'Fig0_graphical_abstract.pdf'); fig.savefig(OUT + 'Fig0_graphical_abstract.png', dpi=400); plt.close()
print('ok')
