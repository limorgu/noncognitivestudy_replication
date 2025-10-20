# noncognitivestudy_replication
A replication of the study Impact of Non-Cognitive Interventions on Student Learning Behaviors and Outcomes: https://dl.acm.org/doi/pdf/10.1145/3576050.3576073

# Non-Cognitive Interventions — Replication (LAK 2023)

This repository replicates the analyses from:

> Vanacore, K. P., Gurung, A., McReynolds, A. A., Lui, A., Shaw, S. T., & Heffernan, N. T. (2023).  
> *Impact of Non-Cognitive Interventions on Student Learning Behaviors and Outcomes.* LAK 2023.

---

## 📦 Contents

- **`outputs/replication_pipeline.ipynb`** — end-to-end pipeline that saves a pre-model dataset and results CSV for each RQ.  
- **`outputs/replication_pipeline_studex_only.ipynb`** — student-level pipeline (uses `stud_ex.csv` only); RQ4.2 falls back to OLS on `avg_pt_accuracy`.  
- **`outputs/replication_pipeline_with_events.ipynb`** — auto-detects `processed/events_all__clean.csv` and runs the full item-level mixed logistic for RQ4.2 when available.

Each notebook writes artifacts to `outputs/`:
- `rq1_*_dataset_*.csv`, `rq1_*_results.csv`
- `rq2_*_dataset_*.csv`, `rq2_*_results.csv`
- `rq3_*_dataset_*.csv`, `rq3_*_results.csv`
- `rq41_*_dataset_*.csv`, `rq41_*_results.csv`
- `rq42_*_dataset_*.csv`, `rq42_*_results.csv` (or `rq42_posttest_fallback_results.csv`)

---

## 🗂 Expected Data

data/
stud_ex.csv # student-level summary (RQ1–RQ4.1)
processed/
events_all__clean.csv # problem-level events (RQ4.2 item-level mixed logistic)

yaml
Copy code

> If `processed/events_all__clean.csv` is missing, the pipeline automatically switches to the RQ4.2 fallback (`avg_pt_accuracy ~ treatment`).

---

## ▶️ How to Run

**Option A — Local Jupyter (recommended)**

```bash
git clone https://github.com/limorgu/noncognitivestudy_replication.git
cd noncognitivestudy_replication

python -m venv .venv
source .venv/bin/activate    # Windows: .venv\\Scripts\\activate

pip install -U pip
pip install numpy pandas statsmodels scipy jupyter

jupyter notebook
Then open outputs/replication_pipeline_with_events.ipynb and run all cells.

Option B — VS Code
Open the repo folder, select your Python environment, and run the notebook directly.

📊 Statistical Models (per experiment)
RQ	Model	Type
RQ1	log(avg_first_response_time+1) ~ treatment	OLS
RQ2	(num_hints>0) ~ treatment	Logistic
RQ3	mastery ~ treatment	Logistic
RQ4.1	-z(skb_problem_count) ~ treatment (mastered only)	OLS
RQ4.2 (full)	`correct ~ treatment + (1	user_id) + (1
RQ4.2 (fallback)	avg_pt_accuracy ~ treatment	OLS

All p-values are Holm-adjusted within each RQ.


If you modify preprocessing, regenerate stud_ex.csv and events_all__clean.csv and re-run.

For exact RQ4.2 replication, ensure post-test item-level rows are in processed/events_all__clean.csv.

