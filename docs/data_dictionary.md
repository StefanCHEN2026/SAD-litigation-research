# Data dictionary

All files are in `data/aggregates/` unless noted. They contain **aggregates only**; no case-level identifiers.

## `bulk_annual.csv`

| Column | Meaning |
|---|---|
| `year` | Filing year (2013–2025). |
| `total` | SAD cases whose case name contains “Schedule A”, “Unincorporated Associations”, or “Doe/Does” and whose NOS is trademark, copyright, or patent. |
| `ilnd` | Cases filed in the Northern District of Illinois. |
| `non_ilnd` | Cases filed elsewhere. |
| `ilnd_share` | `ilnd / total`, as a decimal. |

2025 covers January–April only. RECAP coverage is incomplete; counts are a lower bound.

## `bulk_rights_share.csv`

| Column | Meaning |
|---|---|
| `year` | Filing year. |
| `n` | Total SAD cases in that year. |
| `missing` | Cases with an empty nature-of-suit field. |
| `missing_share` | `missing / n`, in percent. |
| `trademark`, `copyright`, `patent` | Counts among non-missing NOS. |
| `trademark_share`, `copyright_share`, `patent_share` | Shares among non-missing NOS, in percent. |

Because 52%–60% of cases have missing NOS, treat the trend as directional.

## `sellerdefense_firm_structure.csv`

| Column | Meaning |
|---|---|
| `period` | 2020–2022 or 2023–2026. |
| `cases` | Cases in the period. |
| `firms` | Number of law firms (normalized variants). |
| `gbc_share`, `keith_share`, `hsp_share` | Share of cases handled by the named firm, in percent. |

One 2019 case is excluded from the period split.

## `calibration.csv`

Actual vs. simulated SAD counts, 2020–2025. `error_pct` is `(model - actual) / actual × 100`. This is an in-sample calibration, not a forecast.

## `scenarios.csv`

Four simulation scenarios: baseline, unsealing, platform freeze-scope limits, and both. `mutual_awareness` is the share of targeted sellers who know at least one other targeted seller; it is a condition for coordination, not actual coordination.

## `behavior_calibration.csv`

The same four scenarios after calibrating `post_freeze_response` so the baseline default rate matches Goldman’s 70%.

## `china_outcomes.csv`

Cohort-level outcome structure for the Chinese comparison. Cohorts are defined by party name (“网店”), cause of action (“侵害作品发行权纠纷”), or platform defendant (Pinduoduo/Shanghai Xunmeng). These are **cohort rates**, not population rates.

## `china_platform_rates.csv`

Conditional platform-defendant rates:

- `被告名称含网店`: 184/869 = 21.2%.
- `侵害作品发行权-拼多多`: 5,048/26,153 = 19.3%.
- Taobao: 161/26,153 = 0.6%; JD: 269/26,153 = 1.0%.
- Three-platform sum: 5,478/26,153 = 20.9% (undeduplicated).

These are conditional rates for sales-related cohorts, not the overall e-commerce IP platform-defendant rate.

## `chinese_plaintiffs.csv` and `chinese_plaintiff_categories.csv`

Chinese-plaintiff SAD cases by year (probe sample; approximate) and the three categories used in the paper (anonymous mass defendants, named foreign defendants, named Chinese defendants).

## `data_sources.csv`

Source coverage, role, and limitations. No raw data are included.
