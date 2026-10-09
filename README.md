# Do AML fines work? Testing the "fines don't work" hypothesis

**The prompt.** Jim Richards' LinkedIn post on the OCC's **$350M penalty against American Express National Bank** (Oct 8, 2026) said fines are "a pittance" relative to profits, and he concluded "FINES. DON'T. WORK." This repo checks that claim against the data. It asks three questions:

1. How big are AML penalties compared with penalties for other kinds of corporate misconduct (BP, VW, pharma, Boeing…)?
2. Have big fines in other industries stopped *other* firms in that industry from doing the same thing (general deterrence)?
3. Would bigger AML fines help, or is the lever more certain and faster enforcement, individual accountability, or business restrictions?

Contents: this report, a curated dataset of landmark penalties ([`data/key_cases.csv`](data/key_cases.csv)), and a script ([`analysis/analyze.py`](analysis/analyze.py)) that runs the same tests on a full Violation Tracker export.

---

## TL;DR

- **Richards' arithmetic holds up.** American Express Co. earned roughly **$70B** in net income across the June 2014–May 2025 conduct period. A $350M penalty is **~0.5%** of that, **~3%** of one year's profit, and **~2.7%** of the ~$13B in suspected flows. Among the AML cases collected here, it is the smallest relative to profit.
- **AML fines are not unusually small *as single fines*.** In the curated set, AML/sanctions penalties have a median of **~22% of one year's net income** and non-AML landmark penalties a median of **~28%**. The difference is in the tail. BP (Deepwater Horizon, ~$65B total cost) and VW (dieselgate, ~$19B in the US alone, plus prison terms for executives) cost **more than a full year's profit**. Only one-off AML cases do that (BNP, Danske, and Standard Chartered in a weak profit year).
- **AML is a small slice of corporate penalties overall.** Global AML/KYC/sanctions fines were **$6.6B (2023), $4.6B (2024) and $3.8B (2025)** per Fenergo. US corporate penalties of all types run at **$50B+ a year** per Violation Tracker, and "financial offenses" make up about **$322B of the >$1T** total since 2000. Most of that is crisis-era mortgage and securities cases, not AML.
- **The research does not support "bigger fines alone deter."** The largest systematic review of corporate crime deterrence (Simpson et al., Campbell Collaboration) found that **punitive sanctions on their own had no significant deterrent effect at the company level**. Combinations of measures did. In general deterrence research, **certainty of detection beats severity**.
- **Where general deterrence *has* been shown, the driver was certainty and visibility, not fine size.** One EPA fine cut violations at *other* plants in the same state by about **two-thirds** the next year (Shimshack & Ward 2005). One OSHA press release did as much for compliance as about **210 extra inspections** (Johnson 2020, *AER*). Both were small fines with high visibility, from a regulator seen as active.
- **Large fines have repeatedly failed to stop repeat offending in other industries too.** Pharma off-label marketing continued through multiple multi-billion settlements. Boeing breached its $2.5B 737 MAX deferred prosecution agreement. In AML, HSBC, Standard Chartered, Deutsche Bank and Western Union were all hit again after their landmark cases. In the Netherlands (ING then ABN AMRO) and Australia (CBA, then Westpac, then the casinos), large penalties were followed by peers being caught for the same failures.
- **The sanctions that seem to bite are non-monetary.** Examples: Wells Fargo's asset cap (2018–2025, an estimated $4B+ in forgone profit by 2020 alone, plus CEO exits), TD's asset cap and guilty plea, Binance's CEO going to prison, Danske leaving the Baltics, Banamex USA being shut down.
- **Richards' postscript is the deepest problem.** AML enforcement penalizes **process failures** ("suspected" activity going unreported), not measured harm. The deterrence models used in other industries (Becker: fine ≈ harm ÷ probability of detection) need both terms, and AML has neither. Pol (2020) estimates AML policy affects **<0.1% of criminal finances** while compliance costs exceed recoveries **>100×**. Pol calls those numbers poorly validated, but they point the same way.

**Bottom line:** the data supports "fines *as currently used* don't work" more than "fines can't work." Raising the dollar amount is the weakest lever the evidence supports. Faster and more certain detection, publicity, individual consequences, and restrictions on growth or business lines have better support. Linking enforcement to outcomes, as Richards asks, is the precondition for setting any of them sensibly.

---

## 1. Checking the AmEx numbers

| Item | Value | Source |
|---|---|---|
| OCC civil money penalty | $350M, plus a parallel Fed cease-and-desist order on the parent | OCC/Fed, Oct 8 2026; AXP 8-K |
| Conduct period | ~June 2014 – May 2025 | OCC consent order (via press) |
| Suspected TBML not reported | ~$13B | OCC (via press) |
| AXP net income over the period | ≈ $70B (2014 H2 ≈ $2.9B; 2015–2024 ≈ $64B; 2025 Jan–May ≈ $4.5B) | Annual reports, approx. |
| Penalty / period net income | ≈ 0.5% | — |
| Penalty / one year's net income (2025 ≈ $10.8B) | ≈ 3% | — |
| Effect on guidance | None. "A portion… was reserved for in prior periods", no asset cap | AXP 8-K |

Richards' ~$68B and 0.52% match these figures. One nuance: the profit is the *parent's*, while the penalty was imposed on the *bank subsidiary*. Shareholders bear it in either case. The 8-K is the most telling detail: the company had **already reserved** for the penalty and said it **does not change guidance**. A sanction that does not move earnings guidance does not register as a cost to the market.

## 2. How big are AML fines compared with everything else?

### 2a. Totals

| Measure | Value | Notes |
|---|---|---|
| All US corporate penalties since 2000 (Violation Tracker) | > $1 trillion | Annual total rose from ~$7B/yr (early 2000s) to $50B+/yr |
| "Financial offenses" group | ≈ $322B (12,331 records) | Dominated by mortgage/crisis, securities, consumer finance |
| Most-penalized industries | Financial services, pharma, then oil & gas, autos, utilities | Banks are 6 of the top 10 parents; BofA alone ≈ $87B |
| Global AML/KYC/sanctions fines (Fenergo) | $6.6B (2023), $4.6B (2024), $3.8B (2025) | US-imposed AML fines fell ~58–61% in 2025 |

So AML is a single-digit-percent slice of annual corporate penalty dollars. (That compares global AML with US-only totals, so it is indicative only. Run `analysis/analyze.py vt` on an export to get the exact share.) AML is a frequent offense with modest penalties, not a mega-penalty category. The largest single AML/sanctions resolutions (BNP $8.9B, Binance $4.3B, TD $3.1B, Danske $2B, HSBC $1.9B) are far below BP's $20.8B consent decree, the largest single settlement DOJ has reached with one company.

### 2b. Penalty relative to the firm's profit (curated set)

`python analysis/analyze.py cases` on [`data/key_cases.csv`](data/key_cases.csv) gives:

| Category | n | min | median | max |
|---|---|---|---|---|
| AML/sanctions | 12 | 3% (AmEx 2026) | 22% | 140% (BNP 2014) |
| Non-AML | 9 | 15% (Wells Fargo 2020) | 28% | 125% (BP 2016) |

Selected rows:

| Year | Firm | Penalty ($bn) | % of one year's net income | Non-monetary consequence |
|---|---|---|---|---|
| 2012 | HSBC | 1.92 | 11% | DPA, monitor |
| 2014 | BNP Paribas | 8.97 | 140% | Guilty plea; USD-clearing suspension |
| 2018 | CBA | 0.53 | 8% | — |
| 2020 | Westpac | 0.92 | 20% | CEO/chair exits |
| 2022 | Danske | 2.0 | ~100% | Guilty plea; Baltic exit |
| 2024 | TD | 3.09 | 39% | Guilty plea; **asset cap** |
| 2026 | **AmEx** | **0.35** | **3%** | C&D only |
| 2016 | BP (civil) | 20.8 | 125% (≈390% incl. all ~$65B costs) | Guilty plea (2012) |
| 2016–17 | VW (US) | 19.0 | ≈130% | Executives imprisoned |
| 2020 | Wells Fargo | 3.0 | 15% | **Asset cap 2018–25** |
| 2021 | Boeing | 2.5 | 24% | DPA (later found in breach) |

These figures are approximate: reference-year income is rounded from annual reports, and currencies are converted at rough rates. The set is a hand-picked list of landmark cases, so it is biased toward large penalties. Read the ratios as orders of magnitude.

**Interpretation.** The typical big AML penalty and the typical big non-AML penalty are similar in size relative to profit, at a fraction of one year's earnings. The cases that changed corporate behavior on either side were the ones that **went past one year's profit or restricted the business**.

## 3. Do fines deter? The evidence

### 3a. Theory

- **Becker / Polinsky–Shavell:** optimal fine ≈ harm ÷ probability of detection. If detection is rare, fines should be very large. Two problems for AML: (i) harm is not measured (Richards' PS), and (ii) the probability of detection is low and slow (11 years at AmEx).
- **Coffee's "deterrence trap":** the fine needed to deter, gain ÷ probability, often exceeds what a firm can pay without hurting innocent stakeholders. That pushes regulators to fines firms can absorb. Coffee proposes equity fines, which dilute shareholders, as one fix.
- **Who pays:** shareholders, not decision-makers. Agency theory predicts weak deterrence when the people deciding on compliance spending bear none of the cost.

### 3b. Empirical: corporate deterrence in general

| Study | Finding | Implication |
|---|---|---|
| Simpson et al. (Campbell systematic review, 106 studies) | Punitive sanctions alone: **no significant** deterrent effect at company level; effects weaker in better-designed studies | Raising fines alone is a weak lever |
| Schell-Busey, Simpson et al. (2016 meta-analysis) | Only *combinations* of interventions (sanctions + inspections + rules) show consistent deterrence | Fines work as part of a mix |
| Nagin (review) | **Certainty** of punishment deters far more reliably than **severity** (individual-level evidence) | Detect sooner rather than fine harder |
| Shimshack & Ward (2005, *JEEM*), water pollution | One fine → statewide violation rate falls ~⅔ the next year; spillover to *other* plants almost as large as to the fined plant | Strong **general** deterrence, driven by regulator reputation, not fine size |
| Johnson (2020, *AER*), OSHA press releases | One press release ≈ compliance gain of 210 inspections; peer violations fall sharply nearby | Publicity and certainty work; the policy was dropped in 2017 |
| Ferwerda & Zwiers (2021 WP, 713 penalties on 36 banks) | Fines for *own* misconduct hurt bank performance; fines for failing to stop *customers'* misconduct (AML) **do not**, and banks can profit from weak AML controls | AML fines in particular are not felt by the market |

### 3c. Other industries: did big fines stop the behavior across the industry?

| Industry / case | What happened after | Read |
|---|---|---|
| **Offshore oil (BP, 2010–16)** | Lost-time injury rates fell over the following decade (National Academies, 2023), but alongside a new regulator (BSEE), the SEMS and Well Control rules, and mandatory audits. Injury rates reportedly rose again in 2018–19 when rules were relaxed. | Improvement tracks **regulatory structure and enforcement intensity**; the effect of the fine itself can't be separated |
| **Autos (VW dieselgate)** | Other makers were later found with defeat devices (Daimler, FCA settlements), but that conduct largely *predated* the VW case. US executives were indicted and one was imprisoned. | Mixed. The prison terms and the scale of the buybacks were the novel deterrent |
| **Pharma off-label marketing** | Pfizer $430M (2004) → Pfizer $2.3B (2009, partly while under an earlier integrity agreement) → GSK $3B (2012) → J&J $2.2B (2013) | Classic failure of **multi-billion fines** to deter peers or the same firm |
| **Aerospace (Boeing)** | $2.5B DPA (2021), of which only ~$244M was a criminal fine → door-plug blowout Jan 2024 → DOJ finds DPA breached (May 2024) | A large headline number did not change the compliance culture |
| **Retail banking (Wells Fargo)** | $185M (2016) did little → Fed **asset cap** (2018) → CEO exits, $3B DOJ/SEC (2020), est. $4B+ forgone profit by 2020; cap lifted June 2025 | The **business restriction**, not the fine, forced change |
| **Cartels** | Antitrust uses fines, *leniency* (higher detection), and **prison for individuals**. How much recidivism remains is disputed: Connor counts many repeat players; DOJ argues there are almost no formal US recidivists | The individual-liability model is the closest analogue to what AML lacks |

### 3d. AML: the same firms and the same failures, again and again

| Firm / market | Sequence |
|---|---|
| Standard Chartered | NYDFS 2012 (sanctions) → NYDFS 2014 (AML monitoring) → $1.1B US/UK 2019 |
| HSBC | $1.92B + 5-yr DPA 2012 → FCA £63.9M 2021 for transaction monitoring failures 2010–18, overlapping the DPA |
| Deutsche Bank | $630M Russian mirror trades 2017 → Fed $186M 2023 |
| Western Union | $94M Southwest Border 2010 → $586M 2017 |
| Citi / Banamex | Fed C&D 2013 → $140M 2015 (Banamex USA closed) → $97M DOJ 2017 |
| Netherlands | ING €775M (2018) → ABN AMRO €480M (2021) → Rabobank under DNB orders and prosecution |
| Australia | CBA A$700M (2018) → Westpac A$1.3B (2020) → Crown A$450M (2023), Star, SkyCity |
| US mega-cases | HSBC (2012) → TD ($3.1B, 2024) → AmEx (2026); TD's failures ran 2014–2023, entirely **after** the HSBC "landmark" |

The US sequence is the strongest evidence against general deterrence by fines. TD's misconduct happened in the decade *after* HSBC's $1.9B case. AmEx's ran through the HSBC, Danske, Binance and TD resolutions. Every one of those should have been a warning, and none was enough.

One caution: a count of enforcement actions measures **enforcement activity** as well as misconduct, and lags the conduct by years. A rising count can mean better detection rather than more laundering. That is why the proper test (section 5) compares conduct periods, not penalty dates.

## 4. Bigger fines or better enforcement?

| Lever | Evidence it deters | AML status |
|---|---|---|
| Bigger fines | Weak alone (Simpson; Ferwerda & Zwiers; pharma; Boeing) | The default tool |
| Higher certainty / faster detection | Strong (Nagin; Shimshack & Ward) | Weak: 5–11 year lags are typical; US AML fines fell ~60% in 2025 |
| Publicity / regulator reputation | Strong (Johnson 2020; Shimshack & Ward) | Already high-profile, but routine enough to be priced in |
| Individual accountability | Plausible (cartels, VW). UK SM&CR evidence is thin: 1 enforcement action in ~5 years | Very rare for AML failures (Binance CEO is the exception) |
| Business restrictions (asset caps, license limits, exit orders) | Good case evidence (Wells Fargo, TD, Danske, Banamex) | Used selectively; **not** imposed on AmEx |
| Fines tied to gain or harm (% of revenue, like GDPR 4% or EU antitrust 10%) | Theory-backed; makes fines scale with the firm | Not used for AML; requires measuring harm/gain |
| Outcome-linked enforcement | Untested, but a precondition for setting all of the above | Richards' PS: AML penalizes "suspected" activity, not measured harm |

**Answer to "would raising the fine help?":** probably only marginally, and only alongside higher detection probability. Other industries suggest the changes come from (a) regulators perceived as watching, (b) consequences for named people, and (c) sanctions that limit growth. A bigger cheque from shareholders is the weakest of these.

## 5. Testing it properly with the full data

The curated set is illustrative. For a real test:

1. Export penalties from [Violation Tracker](https://violationtracker.goodjobsfirst.org/) (Advanced Search → CSV). Add FinCEN, OCC, Fed and FDIC enforcement action lists for AML actions without a penalty.
2. Run:
   ```bash
   python analysis/analyze.py vt violation_tracker_export.csv --mega-threshold 1e9 --window 3
   ```
   This reports the AML share of penalties by industry, repeat AML offenders, and peer AML case counts before and after each $1B+ AML penalty.
3. Upgrade to a causal design. Use **conduct start dates** from consent orders (not penalty dates) to ask whether misconduct *starting* after a mega-fine falls among peers of similar size and business model, compared with an unaffected control group (e.g. non-US banks or MSBs). Do the same for EPA (Shimshack-style), OSHA and pharma, to get a cross-industry benchmark of fine-driven general deterrence.

Network restrictions in this environment blocked downloading Violation Tracker, so the totals above come from Good Jobs First's and Fenergo's published figures, not a fresh query.

## Caveats

- Net-income denominators are approximate and rounded; currencies are converted at rough period rates.
- The landmark-case list is hand-picked, not a sample.
- Penalty counts reflect enforcement intensity as well as misconduct.
- Several secondary sources disagree on exact amounts (e.g. Standard Chartered 2012, Danske's dating). Check primary orders before citing a specific figure.

## Sources

- AmEx: [PYMNTS – OCC and Fed fine AmEx $350M](https://www.pymnts.com/legal/aml/2026/occ-and-fed-fine-american-express-350-million-over-aml-deficiencies/); [US News/Reuters](https://money.usnews.com/investing/news/articles/2026-10-08/american-express-national-bank-fined-350-million-for-insufficient-anti-money-laundering-program); [American Banker](https://www.americanbanker.com/news/fed-occ-order-amex-to-overhaul-aml-controls); [AXP 8-K](https://www.sec.gov/Archives/edgar/data/0000004962/000000496226000376/axp-20261008.htm); [Protos](https://protos.com/american-express-fined-350m-for-decade-of-suspected-money-laundering/)
- Totals: [Good Jobs First – High Cost of Misconduct (2024)](https://goodjobsfirst.org/the-high-cost-of-misconduct-corporate-penalties-reach-the-trillion-dollar-mark/); [Violation Tracker – financial offenses](https://violationtracker.goodjobsfirst.org/offense_group/financial+offenses); [Fenergo – 2025 fines (WealthBriefing)](https://www.wealthbriefing.com/html/article.php/regulatory-fines-down-in-the-us-in-2025--fenergo); [Fortune – biggest corporate fines](https://fortune.com/longform/biggest-corporate-fines-2000s-bp-bofa-jpmorgan-chase-volkswagen/amp/)
- TD: [American Banker](https://americanbanker.com/news/td-pleads-guilty-to-money-laundering-conspiracy-hit-with-asset-cap); [FinTech Futures](https://www.fintechfutures.com/regulatory-actions/td-bank-hit-with-3bn-in-fines-over-aml-failures)
- Repeat AML cases: [BankInfoSecurity – SCB 2014](https://www.bankinfosecurity.com/another-big-penalty-for-scb-a-5345); [Enzuzo – biggest AML fines](https://www.enzuzo.com/blog/biggest-aml-fines); [American Banker – Banamex](https://www.americanbanker.com/news/citi-affiliate-settles-aml-violations-probe-tied-to-mexico-bound-remittances); [Mondaq – Deutsche Bank Fed 2023](https://mondaq.com/unitedstates/white-collar-crime-anti-corruption-fraud/1348378/deutsche-bank-to-pay-millions-for-sanctions-and-money-laundering-failings); [AUSTRAC enforcement actions](https://www.austrac.gov.au/about-us/record-our-actions/enforcement-actions-taken); [ACAMS – Rabobank](https://www.acams.org/en/news/with-aml-overhaul-behind-schedule-rabobank-requests-deadline-extension); [ABN AMRO €480m](https://kuwaittimes.com/abn-amro-to-settle-e480m-criminal-probe); [Bloomberg – Cost of Dirty Money](https://www.bloomberg.com/graphics/2019-dirty-money/)
- Deterrence research: [Simpson et al. – Campbell systematic review](https://ccjs.umd.edu/project/systematic-review-corporate-crime-deterrence); [Schell-Busey et al. 2016](https://digitalscholarship.unlv.edu/cj_fac_articles/30); [NIJ – Five things about deterrence](https://nij.ojp.gov/topics/articles/five-things-about-deterrence); [Shimshack & Ward 2005 (MPRA)](https://mpra.ub.uni-muenchen.de/25994); [Johnson 2020 – Regulation by Shaming](https://www.openicpsr.org/openicpsr/project/114988/version/V1/view); [Ferwerda & Zwiers – bank fines](https://bahamasamlconference.centralbankbahamas.com/documents/2024-03-26-15-38-00-Ferwerda-and-Zwiers-2021-Bank-fines---version-submitted-for-Bahama-Conference.pdf); [Polinsky & Shavell (NBER)](https://www.nber.org/papers/w3008.pdf); [Coffee – Corporate Crime and Punishment (review)](https://clsbluesky.law.columbia.edu/2020/09/30/an-important-and-timely-book-john-c-coffee-jr-s-corporate-crime-and-punishment/); [Starling Insights – Are AML fines a rounding error?](https://insights.starlingtrust.com/content/observations/are-aml-fines-a-rounding-error-for-banks)
- AML effectiveness: [Pol 2020 summary (11:FS)](https://www.11fs.com/article/aml-is-the-worlds-most-ineffective-policy-experiment); [Marginal Revolution](https://marginalrevolution.com/marginalrevolution/2021/01/the-anti-money-laundering-fraud.html)
- Other industries: [National Academies – offshore safety since 2010](https://www.nationalacademies.org/read/26873/chapter/5); [JPT – offshore accidents amid rollbacks](https://jpt.spe.org/offshore-oil-and-gas-accidents-deaths-spike-amid-regulatory-rollbacks); [Pfizer 2009 8-K](https://www.sec.gov/Archives/edgar/data/0000078003/000007800309000189/x990902.htm); [NPR/MPR – Boeing DPA breach](https://www.mprnews.org/story/2024/05/14/npr-boeing-justice-department-charges); [American Banker – Wells asset cap cost](https://www.americanbanker.com/articles/wells-fargo-asset-cap-is-now-one-of-the-costliest-bank-penalties); [Banking Dive – $4B forgone](https://www.bankingdive.com/news/wells-fargo-has-missed-out-on-4b-in-profits-since-asset-cap-bloomberg/584075/); [Connor – Recidivism Revealed](https://mpra.ub.uni-muenchen.de/121386); [SM&CR – one enforcement action](https://professionaladviser.com/news/4022354/sm-sparks-enforcement-action-nearly); [Ashurst – SM&CR FOI](https://www.ashurst.com/en/insights/a-view-from-the-exchange-are-senior-managers-now-100-per-cent-faithful)
