# Codebook

## 1. SAD classification (case-level)

A case is classified as **SAD** if its case name contains any of:

- “Schedule A”
- “Unincorporated Associations”
- “Doe” / “Does”

and its nature-of-suit is trademark, copyright, or patent.

**Important:** “Doe + copyright” cases are usually BitTorrent downloader cases, not e-commerce seller cases. They must not be counted as SAD seller cases unless the facts show an online sale (see §2). For the seller sample, keep Doe + trademark/patent, and exclude Doe + copyright.

## 2. E-commerce coding (for the three internet courts)

### Q1. Does the dispute arise from an online sale?

Code **yes** only if the judgment or docket shows at least one of:

- a platform order or transaction record;
- a product listing/link on an e-commerce platform;
- shipping/logistics records for a sold product;
- a seller account/storefront on an e-commerce platform;
- online payment records.

Code **no** if the dispute is only about information dissemination (e.g., an article, image, or video posted online), even if a platform is mentioned. Mere mention of a platform in the judgment is not enough.

### Q2. Is a platform a defendant?

Code **yes** if any of the following (or their operating entities) appears in the defendant list:

- 淘宝 / 天猫 (Zhejiang Taobao Network, etc.)
- 拼多多 (Shanghai Xunmeng)
- 京东 (Beijing JD Sanbailiushidu)
- 抖音 / 快手
- 苏宁 / 唯品会 / 1688

Record the platform name. If several platforms are defendants, record all.

### Q3. Outcome and platform role

Record:

- platform role: co-defendant / sole defendant / third party;
- outcome: withdrawal (准予撤诉), deemed withdrawal (按撤诉处理), partial support, dismissal (驳回起诉), judgment for defendant, other;
- whether the judgment discusses the platform’s liability or only the seller’s.

## 3. Sampling design (if replicating the China cohort)

1. Population: IP cases in the Hangzhou, Beijing, and Guangzhou Internet Courts, 2020–2024.
2. Stratify by court × filing year.
3. Draw 300–400 cases per court (equal allocation; do not allocate proportionally, because Beijing dominates).
4. Within each stratum, sample random pages (the API supports deep pagination) and deduplicate by case number.
5. Pre-test 30 cases (10 per court); two coders; report Cohen’s kappa.
6. Weight by inverse sampling probability; report cohort rates with 95% confidence intervals.

## 4. Known limitations

- 知产宝 is a judgment database, not a full filing database; settled or withdrawn cases may be missing.
- The “网店” party-name proxy excludes sellers sued as individuals or companies without “网店” in the name.
- The “侵害作品发行权纠纷” cause includes offline sales; platform rates in that cohort are lower-bound approximations for e-commerce.
- Platform operating entities have multiple names; name-based searches may undercount.
- Case numbers are not unique across courts; always match on court + year + number.
