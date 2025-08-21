#!/usr/bin/env python3
"""
Ad Performance Pipeline
- Loads data from data/prisma.csv, data/innovid.csv, data/gcm360.csv
- Cleans & merges on (date, campaign_id)
- Computes KPIs
- Exports outputs/consolidated.csv and outputs/report.xlsx
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def load_inputs():
    prisma = pd.read_csv(os.path.join(DATA_DIR, "prisma.csv"), parse_dates=["date"])
    innovid = pd.read_csv(os.path.join(DATA_DIR, "innovid.csv"), parse_dates=["date"])
    gcm = pd.read_csv(os.path.join(DATA_DIR, "gcm360.csv"), parse_dates=["date"])
    return prisma, innovid, gcm

def transform(prisma, innovid, gcm):
    # Basic cleaning: ensure keys exist and types are correct
    for df in (prisma, innovid, gcm):
        if "campaign_id" not in df.columns or "date" not in df.columns:
            raise ValueError("Missing required keys (date, campaign_id) in inputs.")
    # Merge
    merged = (
        prisma.merge(gcm, on=["date","campaign_id"], how="inner")
              .merge(innovid, on=["date","campaign_id"], how="left")
    )
    # KPI calculations
    merged["ctr"] = (merged["clicks"] / merged["impressions"]).fillna(0)
    merged["cpm"] = (merged["cost"] / merged["impressions"] * 1000).replace([pd.NA, float("inf")], 0).fillna(0)
    merged["vcr"] = (merged["video_completes"] / merged["video_starts"]).replace([pd.NA, float("inf")], 0).fillna(0)
    # Planned vs actual pacing
    merged["pacing_vs_plan"] = (merged["cost"] - merged["planned_spend"]) / merged["planned_spend"]
    return merged

def summarize(df):
    # Daily KPIs already in df; create an overall summary by campaign
    summary = (df.groupby(["campaign_id","campaign_name","channel"], as_index=False)
                 .agg({
                    "planned_spend":"sum",
                    "cost":"sum",
                    "impressions":"sum",
                    "clicks":"sum",
                    "video_starts":"sum",
                    "video_completes":"sum"
                 }))
    summary["ctr"] = (summary["clicks"] / summary["impressions"]).fillna(0)
    summary["cpm"] = (summary["cost"] / summary["impressions"] * 1000).fillna(0)
    summary["vcr"] = (summary["video_completes"] / summary["video_starts"]).replace([pd.NA, float("inf")], 0).fillna(0)
    summary["pacing_vs_plan"] = (summary["cost"] - summary["planned_spend"]) / summary["planned_spend"]
    return summary

def export_outputs(daily, summary):
    daily_out = os.path.join(OUT_DIR, "consolidated.csv")
    daily.to_csv(daily_out, index=False)
    # Excel report
    xlsx_out = os.path.join(OUT_DIR, "report.xlsx")
    with pd.ExcelWriter(xlsx_out, engine="openpyxl") as writer:
        daily.to_excel(writer, sheet_name="Daily KPI", index=False)
        summary.to_excel(writer, sheet_name="Summary KPI", index=False)
    print(f"Wrote: {daily_out}")
    print(f"Wrote: {xlsx_out}")

def main():
    prisma, innovid, gcm = load_inputs()
    daily = transform(prisma, innovid, gcm)
    summary = summarize(daily)
    export_outputs(daily, summary)

if __name__ == "__main__":
    main()
