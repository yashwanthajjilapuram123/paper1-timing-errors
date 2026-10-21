# When the clock is wrong: event–tracking timing errors and event-level load

Code to reproduce all results in:

> Ajjilapuram, Y. (2026). *When the clock is wrong: event–tracking timing errors and their effect on event-level external load monitoring in elite football.* Preprint. [link to be added]

## What this study does
Practitioners link coded match events (passes, tackles, shots) to positional data to measure the physical load of individual actions. Event timestamps are not perfectly aligned with tracking data. Using three elite German football matches with hand-annotated true event frames, this code measures how timing errors change event-level speed and acceleration flags under four conditions: raw provider timestamps, a best-case constant clock shift, ETSY and ELASTIC synchronisation.

**Key results (3,186 events):** with raw timestamps, 18.5% of true sprint flags and 27.9% of true sustained-acceleration flags were missed; a constant clock shift did not significantly help; ELASTIC synchronisation reduced misses to 1–2%. Each extra second of timing error increased the odds of a missed flag 2.6–4.9-fold.

## How to run
1. Open `paper1_reproduce.ipynb` in Google Colab (File → Upload notebook, or the "Open in Colab" button on GitHub).
2. Run all cells in order. First run ≈ 45–75 minutes; data are cached in your Google Drive (`MyDrive/paper1`).
3. Tables and figures are written to `paper1_results/`.
4. Publication-style figures: `python figures/make_figs.py` and `python figures/make_figs2.py` (numbers taken from the notebook outputs).

## Repository contents
| File | Purpose |
|---|---|
| `paper1_reproduce.ipynb` | Full analysis pipeline (download → sync → load flags → statistics → figures) |
| `figures/` | Scripts for the final manuscript figures (colour-blind-safe style) |
| `requirements.txt` | Packages beyond the ELASTIC repository's own requirements |

## Data and third-party code (not included here)
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
