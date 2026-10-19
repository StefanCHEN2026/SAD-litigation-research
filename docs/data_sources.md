# Data sources and access

This repository does **not** redistribute raw case-level data. The notes below describe what each source is, what it was used for, and the main limitations. Researchers should obtain access from the original providers and comply with their terms.

## 1. CourtListener quarterly bulk dockets

- Provider: Free Law Project / CourtListener.
- Period used: 2013–2025.4 (snapshot dated 2025-04-30).
- N: 7,696 modern SAD cases after filtering.
- Role: SAD universe, annual trend, court concentration, nature of suit, duration.
- Access: CourtListener bulk data (public).
- Limitation: RECAP coverage is incomplete; counts are a lower bound. Bulk dockets do not contain party or attorney fields.

## 2. sellerdefense industry index

- Provider: sellerdefense (industry index of Chinese sellers sued in the U.S.).
- Period used: 2020–2026.
- N: 11,555 case-level rows.
- Role: China-seller identification; law firm and brand structure.
- Access: the provider’s public index; not redistributed here.
- Limitation: industry index, not an official census; about 19% of rows are non-SAD; case numbers are truncated and not unique without state.

## 3. CourtListener REST API sample

- Provider: Free Law Project / CourtListener.
- Period used: 2013–2026.
- N: 4,304 dockets (paper sample).
- Role: defendant counts, duration, attorney scale.
- Access: CourtListener API; not redistributed here.
- Limitation: partial sample; not a census.

## 4. 知产查 U.S. document database

- Provider: 知产查 (commercial legal database).
- Period used: 2020–2026.
- N: 2,169 SAD titles; 170 full docket reports.
- Role: latest cases; procedural detail (sealing, TRO, default).
- Access: commercial subscription; not redistributed here.
- Limitation: title-based SAD filter; the 170 docket reports are a stratified sample, not representative.

## 5. What is not included and why

- Raw sellerdefense CSV: commercial index; redistribution is not authorized.
- Raw 知产查/知产宝 case texts: commercial database; redistribution is not authorized.
- Sealed court documents: not public.
- Party names, addresses, emails, phone numbers, store accounts: privacy and re-identification risk.

If you need raw data, contact the providers directly. The repository’s `DATA_USE.md` applies to the aggregated and synthetic data that are included.
