# Aggregated data

This directory contains **aggregated statistics only**. It contains no case-level records, no party names, no store names, no addresses, and no sealed materials.

## Files

| File | What it contains | Key caveat |
|---|---|---|
| `bulk_annual.csv` | Annual SAD counts from the CourtListener quarterly bulk snapshot, 2013–2025.4 | RECAP coverage is incomplete; this is a lower bound. 2025 covers January–April only. |
| `bulk_rights_share.csv` | Nature-of-suit shares by year, 2020–2024 | Shares are calculated among non-missing NOS fields; 51.9%–60.0% of cases have missing NOS. Treat the trend as directional, not exact. |
| `sellerdefense_firm_structure.csv` | Law-firm structure in the sellerdefense sample, 2020–2022 vs. 2023–2026 | Industry index, not an official census; about 19% of its rows are non-SAD. |
| `calibration.csv` | Actual vs. simulated SAD counts, 2020–2025 | In-sample calibration. The model is not a forecasting tool. |
| `scenarios.csv` | Four baseline simulation scenarios | Five independent runs per scenario. The platform scenario is a **freeze-scope** scenario, not a refusal-to-freeze scenario. |
| `behavior_calibration.csv` | Four scenarios after calibrating the baseline default rate to Goldman's 70% | Robustness check; not a full validation. |
| `china_outcomes.csv` | Outcome structure of Chinese cohorts used in the paper | Cohort-based; not a population rate. |
| `china_platform_rates.csv` | Conditional platform-defendant rates in two sales-related cohorts | Conditional rates, not the overall e-commerce IP platform rate. |
| `chinese_plaintiffs.csv` | Chinese-plaintiff SAD cases by year, 2021–2026 | Probe sample; approximate. 2026 is partial (through September 2). |
| `chinese_plaintiff_categories.csv` | Chinese-plaintiff case categories | Identifiable sample only. |
| `data_sources.csv` | Data-source coverage and limitations | No raw data are included. |

## What is deliberately absent

- Raw sellerdefense CSV files.
- Raw 知产宝/知产查 case texts or docket reports.
- Sealed court documents.
- Party names, individual names, addresses, emails, phone numbers, or store account identifiers.

Researchers who need the raw data should obtain it from the original sources under their terms.
