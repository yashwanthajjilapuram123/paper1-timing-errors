# When the clock is wrong: event–tracking timing errors and event-level load

Code to reproduce all results in:

> Ajjilapuram, Y. (2026). *When the clock is wrong: event–tracking timing errors and their effect on event-level external load monitoring in elite football.* Preprint, SportRxiv. [DOI to be added]

## What this study does
Practitioners link coded match events (passes, tackles, shots) to positional data to measure the physical load of individual actions. Event timestamps are not perfectly aligned with tracking data. Using three elite German football matches with hand-annotated true event frames, this code measures how timing errors change event-level speed and acceleration flags under four conditions: raw provider timestamps, a best-case constant clock shift, ETSY and ELASTIC synchronisation.

**Key results (3,186 events):** with raw timestamps, 18.5% of true sprint flags and 27.9% of true sustained-acceleration flags were missed; a constant clock shift did not significantly help; ELASTIC synchronisation reduced misses to 1–2%. Each extra second of timing error increased the odds of a missed flag 2.6–4.9-fold.

## How to run
1. Open `paper1_reproduce.ipynb` in Google Colab (File → Upload notebook, or the "Open in Colab" button on GitHub).
2. Run all cells in order. First run ≈ 45–75 minutes; data are cached in your Google Drive (`MyDrive/paper1`).
3. Tables and figures are written to `paper1_results/`. Section 14 exports the per-event timing errors used for Figure 2.
4. Manuscript figures (written to `output/`):
   ```
   pip install numpy pandas matplotlib
   python make_fig2.py                 # Figure 2, computed from data/timing_errors_per_event.csv
   python make_figs.py                 # Figures 1, 3 and 4
   python make_figs2.py                # Figure 5 and Supplementary Figure S1
   python make_graphical_abstract.py   # graphical abstract (full size)
   python make_graphical_abstract_525.py output   # graphical abstract for the journal (525 px wide)
   ```
   `make_fig2.py` also prints the median and the percentage of events beyond 1 s and 2 s for each condition, which match the paper. The other scripts use the values reported by the notebook (Sections 12 and 13).

## Repository contents
| File | Purpose |
|---|---|
| `paper1_reproduce.ipynb` | Full analysis pipeline (download → sync → load flags → statistics → per-event export) |
| `data/timing_errors_per_event.csv` | Signed timing error (s) of every event under each condition (3,561 events; blank = event not placed by that method) |
| `make_fig2.py` | Figure 2 (timing-error distributions), built directly from the CSV |
| `make_figs.py`, `make_figs2.py`, `make_graphical_abstract.py`, `make_graphical_abstract_525.py`, `figstyle.py` | Other manuscript figures (colour-blind-safe style) |
| `requirements.txt` | Packages beyond the ELASTIC repository's own requirements |

### Figure files and paper numbering
| Paper | File |
|---|---|
| Figure 1 | `Fig1_schematic` |
| Figure 2 | `Fig2_timing_summary` |
| Figure 3 | `Fig3_flags_forest` |
| Figure 4 | `Fig5_event_type` |
| Figure 5 | `Fig4_dose_response` |
| Figure S1 | `FigS1_sensitivity` |

## Data and third-party code
The raw tracking and event data are not included here; they are downloaded automatically. The per-event timing-error file in `data/` is derived from the ELASTIC benchmark and the Sportec Open DFL Dataset and is shared under the same CC-BY 4.0 licence.

- **Sportec Open DFL Dataset** – Bassek, M., Rein, R., Weber, H., & Memmert, D. (2025). *Scientific Data*, 12, 195. https://doi.org/10.1038/s41597-025-04505-y (CC-BY 4.0; downloaded automatically from figshare).
- **ELASTIC benchmark and code** – Kim, H., et al. (2026). ELASTIC: Trajectory-based synchronization of event and tracking data in soccer. *CIKM 2026*. https://github.com/hyunsungkim-ds/elastic (data CC-BY 4.0, code MPL-2.0; cloned automatically).
- **ETSY** – Van Roy, M., Cascioli, L., & Davis, J. (2023). MLSA 2023 (implementation used via the ELASTIC repository).

## Notes
- Speeds and accelerations come from positional (camera) tracking at 25 Hz, not GPS.
- Section 6 contains a pilot instantaneous peak-acceleration flag that was not used in the paper (it fired on 82% of events); final flags are defined in Section 12.

## Citation
See `CITATION.cff`.

## Licence
Code in this repository: MIT. Data and third-party code keep their original licences.
