"""Test whether fines are big enough to matter and whether they deter.

Two modes:

  python analysis/analyze.py cases
      Summarise data/key_cases.csv (curated list of landmark penalties):
      penalty as a share of the firm's reference-year net income,
      AML/sanctions vs other misconduct.

  python analysis/analyze.py vt path/to/violation_tracker_export.csv
      Run on a CSV exported from Good Jobs First's Violation Tracker
      (https://violationtracker.goodjobsfirst.org/, Advanced Search -> download).
      Reports:
        1. AML/sanctions share of total penalties, overall and by industry
        2. Repeat AML offenders (parents with >= 2 AML penalties) and the gap between them
        3. Peer general-deterrence test: AML penalty counts in the financial sector
           in the N years before vs after each AML mega-fine (>= threshold)

Column names in Violation Tracker exports have changed over time; override them
with --col-* flags if needed.
"""

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
AML_PATTERN = re.compile(
    r"money.?laundering|bank secrecy|\bBSA\b|\bAML\b|sanction|OFAC|economic sanctions",
    re.IGNORECASE,
)


def run_cases(path: Path) -> None:
    df = pd.read_csv(path)
    df["pct_of_net_income"] = 100 * df["penalty_usd_bn"] / df["ref_net_income_usd_bn"]
    cols = ["year", "firm", "category", "penalty_usd_bn", "ref_net_income_usd_bn", "pct_of_net_income"]
    print(df[cols].sort_values(["category", "year"]).to_string(index=False, float_format="%.2f"))
    print("\nPenalty as % of one year's net income (rows with income data):")
    summary = df.dropna(subset=["pct_of_net_income"]).groupby("category")["pct_of_net_income"]
    print(summary.describe()[["count", "min", "50%", "max"]].round(1).to_string())


def is_aml(row: pd.Series, offense_cols: list[str]) -> bool:
    return any(AML_PATTERN.search(str(row[c])) for c in offense_cols if c in row and pd.notna(row[c]))


def run_vt(path: Path, args: argparse.Namespace) -> None:
    df = pd.read_csv(path, low_memory=False)
    missing = [c for c in (args.col_parent, args.col_year, args.col_amount) if c not in df.columns]
    if missing:
        sys.exit(f"Missing columns {missing}. Available: {list(df.columns)}")

    df[args.col_amount] = pd.to_numeric(
        df[args.col_amount].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce"
    ).fillna(0)
    df[args.col_year] = pd.to_numeric(df[args.col_year], errors="coerce")
    offense_cols = [c for c in (args.col_offense, args.col_offense_group, args.col_description) if c in df.columns]
    df["is_aml"] = df.apply(is_aml, axis=1, offense_cols=offense_cols)

    total = df[args.col_amount].sum()
    aml_total = df.loc[df["is_aml"], args.col_amount].sum()
    print(f"Records: {len(df):,}  Total penalties: ${total / 1e9:,.1f}bn")
    print(f"AML/sanctions: {df['is_aml'].sum():,} records, ${aml_total / 1e9:,.1f}bn ({100 * aml_total / total:.1f}%)")

    if args.col_industry in df.columns:
        by_ind = df.groupby(args.col_industry).agg(
            total_bn=(args.col_amount, lambda s: s.sum() / 1e9),
            aml_bn=(args.col_amount, lambda s: s[df.loc[s.index, "is_aml"]].sum() / 1e9),
        )
        by_ind["aml_share_pct"] = 100 * by_ind["aml_bn"] / by_ind["total_bn"]
        print("\nTop industries by total penalties:")
        print(by_ind.sort_values("total_bn", ascending=False).head(15).round(2).to_string())

    if args.col_offense_group in df.columns:
        print("\nPenalties by offense group ($bn):")
        print((df.groupby(args.col_offense_group)[args.col_amount].sum() / 1e9).sort_values(ascending=False).round(1).to_string())

    aml = df[df["is_aml"]].sort_values(args.col_year)
    repeat = aml.groupby(args.col_parent).agg(
        n=(args.col_year, "size"),
        first=(args.col_year, "min"),
        last=(args.col_year, "max"),
        total_bn=(args.col_amount, lambda s: s.sum() / 1e9),
    )
    repeat = repeat[repeat["n"] >= 2].sort_values("n", ascending=False)
    n_parents = aml[args.col_parent].nunique()
    print(f"\nRepeat AML offenders: {len(repeat)} of {n_parents} parents ({100 * len(repeat) / max(n_parents, 1):.0f}%) have >= 2 AML penalties")
    print(repeat.head(25).round(2).to_string())

    # Peer deterrence: does an AML mega-fine reduce AML penalties at *other* firms afterwards?
    # Caveat: penalty counts measure enforcement as much as misconduct, and lag conduct by years.
    mega = aml[aml[args.col_amount] >= args.mega_threshold]
    w = args.window
    rows = []
    for _, m in mega.iterrows():
        y, parent = m[args.col_year], m[args.col_parent]
        others = aml[aml[args.col_parent] != parent]
        before = others[(others[args.col_year] >= y - w) & (others[args.col_year] < y)]
        after = others[(others[args.col_year] > y) & (others[args.col_year] <= y + w)]
        rows.append({
            "year": int(y), "parent": parent, "penalty_bn": m[args.col_amount] / 1e9,
            f"peer_cases_{w}y_before": len(before), f"peer_cases_{w}y_after": len(after),
        })
    if rows:
        print(f"\nPeer AML cases {w}y before/after each AML penalty >= ${args.mega_threshold / 1e9:.1f}bn:")
        print(pd.DataFrame(rows).round(2).to_string(index=False))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="mode", required=True)
    c = sub.add_parser("cases")
    c.add_argument("path", nargs="?", default=ROOT / "data" / "key_cases.csv", type=Path)
    v = sub.add_parser("vt")
    v.add_argument("path", type=Path)
    v.add_argument("--col-parent", default="Current Parent Company Name")
    v.add_argument("--col-year", default="Penalty Year")
    v.add_argument("--col-amount", default="Penalty Amount")
    v.add_argument("--col-offense", default="Primary Offense Type")
    v.add_argument("--col-offense-group", default="Offense Group")
    v.add_argument("--col-description", default="Description")
    v.add_argument("--col-industry", default="Major Industry of Parent")
    v.add_argument("--mega-threshold", type=float, default=1e9)
    v.add_argument("--window", type=int, default=3)
    args = p.parse_args()
    if args.mode == "cases":
        run_cases(args.path)
    else:
        run_vt(args.path, args)


if __name__ == "__main__":
    main()
