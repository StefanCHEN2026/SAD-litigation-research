# SAD Litigation Research Replication Package

**A replication package for an empirical and agent-based study of U.S. “Schedule A Defendants” (SAD) intellectual-property litigation.**

This repository accompanies a research paper on the **generation and persistence of SAD litigation** against cross-border e-commerce sellers. It contains the simulation code, the aggregated empirical statistics, synthetic model outputs, and an interactive visualization frontend. It does **not** contain raw case-level data from commercial databases, sealed court materials, or personal identifiers.

> **Research use only.** This repository is provided for research, teaching, and replication. It is **not legal advice**, and it does **not** determine whether any particular seller or company infringed any right. Allegations in court records are allegations, not findings of liability.

---

## 1. What is included

| Path | Content |
|---|---|
| `code/sad_abm_v2.py` | Persistent-agent agent-based model (ABM) of plaintiffs, sellers, platforms, and courts. |
| `code/oos_validate.py` | Out-of-sample calibration: fit 2020–2023, predict 2024–2025. |
| `code/behavior_validate.py` | Behavioral calibration: align the baseline default rate to the external benchmark and rerun the scenarios. |
| `data/synthetic/` | Simulation outputs produced by the code (no real sellers). |
| `data/aggregates/` | Aggregated empirical statistics (annual counts, court/cause/firm structure, China cohorts). |
| `viz/sad-abm-lab.html` | Interactive four-scenario visualization using synthetic data only. |
| `docs/data_dictionary.md` | Column definitions for the aggregate files. |
| `docs/codebook.md` | Coding protocol for SAD classification and e-commerce/platform coding. |
| `docs/data_sources.md` | Source coverage, access, and limitations. |

## 2. What is deliberately not included

- Raw **sellerdefense** CSV files.
- Raw **知产宝 / 知产查** case texts or docket reports.
- Sealed court documents or confidential materials.
- Party names, individual names, addresses, emails, phone numbers, or store-account identifiers.
- API keys, tokens, or `.env` files.

The raw data remain subject to the terms of their sources. Researchers who need them should obtain access from the original providers. See `docs/data_sources.md`.

## 3. Data coverage

| Source | Period | N | Role | Main limitation |
|---|---|---:|---|---|
| CourtListener quarterly bulk dockets | 2013–2025.4 | 7,696 | SAD universe, trend, court/cause/duration | RECAP coverage incomplete; lower bound |
| sellerdefense industry index | 2020–2026 | 11,555 | China-seller identification, law firm/brand structure | Industry index, not official; about 19% non-SAD |
| CourtListener REST API sample | 2013–2026 | 4,304 | Defendant count, duration, attorney scale | Partial sample |
| 知产查 U.S. document database | 2020–2026 | 2,169 | Latest cases, procedural detail | Commercial database; title-based filter |
| 知产查 full docket reports | 2020–2026 | 170 | Sealing/TRO/default timeline | Stratified sample, not representative |

The union of the three main case-level sources, deduplicated by year + docket number, is approximately **13,300** cases. This is a research estimate, not a census.

## 4. Quick start

The core ABM uses only the Python standard library.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

bash reproduce.sh
```

`reproduce.sh` runs:

```bash
python code/sad_abm_v2.py      > data/synthetic/sad_abm_v2_results.csv
python code/oos_validate.py    > data/synthetic/oos_results.csv
python code/behavior_validate.py > data/synthetic/behavior_results.csv
```

The full ABM runs 400,000 persistent sellers over 11 periods and may take several minutes. To shorten a test run, reduce `n_sellers` or `years` in `code/sad_abm_v2.py`.

## 5. Key results (summary)

- **Sealing changes the outcome structure more than the case volume.** Removing sealing lowers cumulative cases by about 20%, but lowers the default rate from 61% to 26% and raises mutual awareness from 25% to 81%.
- **Platform freeze-scope limits alone are slow and limited.** Narrowing the freeze scope reduces cumulative cases by about 12%, with little effect on the default rate.
- **The two reforms interact.** Doing both produces a roughly 40% reduction, larger than the sum of the separate effects.
- **Damages caps are not the main lever.** Lowering expected damages from USD 150,000 to USD 20,000 reduces cases by only about 4%; recovery is constrained by frozen account balances.
- **The model is a mechanism illustration, not a forecast.** An out-of-sample test calibrated on 2020–2023 under-predicts 2024–2025 by 21.9% and 39.5%.

## 6. Citation

If you use this repository, please cite the paper and the repository. See `CITATION.cff`.

```text
SAD Research Project. SAD Litigation Research Replication Package, version 1.0.0 (2026).
```

## 7. License

- **Code:** MIT License. See `LICENSE`.
- **Aggregated and synthetic data:** CC BY-NC 4.0 **plus** the additional restrictions in `DATA_USE.md`. They are for non-commercial research and teaching only.

“Research use only” is a use restriction, not an OSI-approved open-source license. The code and the data are therefore licensed separately.

## 8. Disclaimer

This repository is a research artifact. It does not constitute legal advice, does not verify the merits of any allegation, and must not be used to identify, contact, blacklist, or take legal or commercial action against any seller, platform, or rights holder. See `DATA_USE.md` before using the data.

## 9. Contact

For questions about the paper or the replication package, please open an issue or contact the authors.
