#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replication: Impact of Non-Cognitive Interventions (RQ1–RQ4)

Inputs (CSV):
  - data/stud_ex.csv : student-level summaries per experiment
  - data/dat.csv     : problem-level logs incl. post-test rows

Outputs:
  - outputs/rq1_response_time.csv
  - outputs/rq2_hint_usage.csv
  - outputs/rq3_mastery.csv
  - outputs/rq41_efficiency.csv
  - outputs/rq41_efficiency_followups.csv
  - outputs/rq42_posttest.csv
"""

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tools import add_constant
from statsmodels.stats.multitest import multipletests
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
from scipy import stats

# ------------------------- Config -------------------------
IN_STUD_EX = "data/stud_ex.csv"
IN_DAT     = "data/dat.csv"
OUT_DIR    = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------- Helper functions -------------------
def holm_adjust(pvals: pd.Series) -> pd.Series:
    mask = pvals.notna().values
    adj = np.full_like(pvals.astype(float).values, np.nan, dtype=float)
    if mask.sum() > 0:
        _, p_holm, _, _ = multipletests(pvals[mask].values, alpha=0.05, method="holm")
        adj[mask] = p_holm
    return pd.Series(adj, index=pvals.index)

def tidy_ols(y, Xcol, data) -> dict:
    X = add_constant(data[Xcol])
    res = sm.OLS(data[y], X).fit()
    return dict(Estimate=res.params[Xcol], StdErr=res.bse[Xcol],
                stat=res.tvalues[Xcol], p=res.pvalues[Xcol], N=len(data))

def tidy_logit(y, Xcol, data) -> dict:
    X = add_constant(data[Xcol])
    res = sm.Logit(data[y], X).fit(disp=False)
    b = res.params[Xcol]
    se = res.bse[Xcol]
    from scipy.stats import norm
    z  = b / se
    p  = 2*(1 - norm.cdf(abs(z)))
    ci = res.conf_int().loc[Xcol].tolist()
    return dict(Estimate=b, StdErr=se, stat=z, p=p,
                OR=np.exp(b), OR_low=np.exp(ci[0]), OR_high=np.exp(ci[1]), N=len(data))

def safe_binary(s):
    return (pd.Series(s).replace({True:1, False:0, "TRUE":1, "FALSE":0}).astype(float))

# ---------------------- Load datasets ---------------------
stud_ex = pd.read_csv('noncognitivestudy_replication/output/processed/stud_ex__replication_ready.csv')
dat     = pd.read_csv('')

# Coerce keys used below
for c in ["experiment", "treatment"]:
    if c in stud_ex.columns:
        if c == "treatment":
            stud_ex[c] = pd.to_numeric(stud_ex[c], errors="coerce")
        else:
            stud_ex[c] = stud_ex[c].astype(str)

# -------------------------- RQ1 ---------------------------