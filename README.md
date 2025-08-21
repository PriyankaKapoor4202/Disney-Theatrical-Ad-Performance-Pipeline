# 📊 Ad Performance Pipeline

Automated, end-to-end pipeline that consolidates **Prisma**, **Innovid**, and **GCM360** data into clean KPI outputs for reporting and dashboards.

## 🎯 Objective
Automate ingestion and transformation of cross-platform campaign data to deliver reliable KPIs with one command.

## ❌ Problem
Manual weekly reporting across CSV exports was slow and error-prone, leading to inconsistent metrics and delays.

## ✅ Solution / Approach
- **Ingest**: Read standardized CSVs for Prisma, Innovid, GCM360 (see `/data`).
- **Transform**: Merge on `(date, campaign_id)`, clean fields, and compute KPIs (CTR, CPM, VCR, Pacing).
- **Deliver**: Export `outputs/consolidated.csv` and `outputs/report.xlsx` with **Daily KPI** and **Summary KPI** sheets.

## 🔧 How It Was Solved
- Python ETL (`pandas`), clean merge logic, KPI calculations.
- Minimal dependencies (`pandas`, `openpyxl`).
- Simple, reproducible structure suitable for recruiters and teams.

## 🔄 Flowchart
```mermaid
flowchart TD
    A[CSV Inputs: prisma.csv, innovid.csv, gcm360.csv] --> B[ETL (pandas)]
    B --> C[Clean & Merge]
    C --> D[Compute KPIs: CTR, CPM, VCR, Pacing]
    D --> E[Outputs: consolidated.csv, report.xlsx]

## 🚀 Quickstart
```bash
# 1) Create a virtual environment (optional but recommended)
python -m venv .venv && . .venv/Scripts/activate  # Windows
# or
python -m venv .venv && source .venv/bin/activate  # macOS/Linux

# 2) Install requirements
pip install -r requirements.txt

# 3) Run the pipeline
python src/pipeline.py

# 4) See the results
#   - outputs/consolidated.csv
#   - outputs/report.xlsx (tabs: Daily KPI, Summary KPI)
```

## 📂 Project Structure
```
Ad_Performance_Pipeline_Full/
├─ data/            # Ready-to-run sample data
├─ outputs/         # Pipeline outputs (created on run)
├─ src/             # ETL code
├─ notebooks/       # (Optional) scratch space
├─ requirements.txt
└─ README.md
```

## 📈 KPIs Produced
- **CTR** = clicks / impressions  
- **CPM** = cost / impressions * 1000  
- **VCR** = video_completes / video_starts  
- **Pacing vs Plan** = (cost - planned_spend) / planned_spend  

> Run once, and the outputs are generated. No additional setup required.
