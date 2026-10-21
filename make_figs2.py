import numpy as np, pandas as pd, matplotlib.pyplot as plt, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from figstyle import *
style(); OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output') + '/'; os.makedirs(OUT, exist_ok=True)
labels = ['<0.2', '0.2–0.5', '0.5–1', '1–2', '2–4', '≥4']
nev = [573, 630, 711, 794, 385, 93]
S = dict(m=[0.0, 2.6, 7.8, 22.2, 55.6, 62.5], lo=[0.0, 0.5, 3.1, 13.7, 37.3, 38.6], hi=[8.4, 13.2, 18.5, 33.9, 72.4, 81.5], n=[42, 39, 51, 63, 27, 16])
A = dict(m=[1.1, 8.0, 13.1, 40.1, 67.5, 100.0], lo=[0.2, 4.2, 8.3, 33.0, 56.6, 83.9], hi=[5.8, 14.4, 19.9, 47.7, 76.8, 100.0], n=[93, 113, 130, 167, 80, 20])
fig, ax = plt.subplots(figsize=(4.6, 3.0))
x = np.arange(6)
for d, col, mk, lab, off in [(S, OKABE['Raw feed'], 'o', 'Sprint (≥7.0 m·s⁻¹)', -0.09),
                             (A, OKABE['Constant shift'], 's', 'Sustained acceleration (≥3.0 m·s⁻², ≥0.5 s)', 0.09)]:
    xx = x + off
    ax.vlines(xx, d['lo'], d['hi'], color=col, lw=1.1, alpha=0.9)
    ax.plot(xx, d['m'], marker=mk, color=col, lw=1.6, ms=5, mec='white', mew=0.7, label=lab, zorder=3)
ax.annotate('GEE odds ratio per 1 s of error:\nsprint 2.59 (1.98–3.38)\nsustained acceleration 4.89 (3.77–6.35)',
            xy=(0.02, 0.97), xycoords='axes fraction', va='top', fontsize=6.5, color=MUTED)
ax.set_xticks(x); ax.set_xticklabels([f'{l}\nn={n}' for l, n in zip(labels, nev)], fontsize=6.6)
ax.set_xlabel('Absolute timing error of raw timestamp (s); n = events per bin')
ax.set_ylabel('True flags missed (%, Wilson 95% CI)'); ax.set_ylim(0, 105); ax.set_xlim(-0.4, 5.4)
ax.legend(loc='upper left', bbox_to_anchor=(0.0, 0.72), fontsize=6.6)
ax.grid(axis='x', visible=False)
fig.savefig(OUT+'Fig4_dose_response.pdf'); fig.savefig(OUT+'Fig4_dose_response.png', dpi=400); plt.close()

# Fig S1 sensitivity
thr = [6.0, 6.5, 7.0, 7.5, 8.0]; win = ['±1 s', '±2 s', '±3 s']
RAW = np.array([[27.2, 29.9, 32.0, 39.8, 45.6], [15.9, 18.5, 18.5, 21.9, 24.0], [10.5, 10.7, 12.9, 17.0, 20.6]])
EL = np.array([[1.7, 2.6, 2.9, 5.6, 10.5], [1.4, 2.1, 2.1, 2.7, 4.0], [0.8, 1.1, 1.0, 1.6, 3.1]])
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('b', ['#F4F8FB', '#9CC3E0', '#2F6FA6', '#0B3A63'])
fig, axes = plt.subplots(1, 2, figsize=(6.85, 1.9), gridspec_kw=dict(wspace=0.12))
for ax, M_, t, L in [(axes[0], RAW, 'Raw feed', 'A'), (axes[1], EL, 'ELASTIC', 'B')]:
    im = ax.imshow(M_, cmap=cmap, vmin=0, vmax=46, aspect='auto')
    for (i, j), v in np.ndenumerate(M_):
        ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=6.8, color='white' if v > 26 else INK)
    ax.set_xticks(range(5)); ax.set_xticklabels([f'{c:g}' for c in thr]); ax.set_yticks(range(3))
    ax.set_yticklabels(win if L == 'A' else []); ax.tick_params(length=0); ax.grid(False)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlabel('Sprint threshold (m·s⁻¹)'); ax.set_title(t, loc='left', fontsize=8, fontweight='bold'); panel(ax, L)
axes[0].set_ylabel('Analysis window')
cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02); cb.set_label('True sprint flags missed (%)', fontsize=6.6); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=6.3)
fig.savefig(OUT+'FigS1_sensitivity.pdf'); fig.savefig(OUT+'FigS1_sensitivity.png', dpi=400); plt.close()
print('ok')
