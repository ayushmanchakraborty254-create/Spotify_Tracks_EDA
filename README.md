# Exploratory Data Analysis (EDA) of Spotify Tracks
### Data-Driven Sound Engineering, Audio Feature Profiling & Listener Engagement Optimization

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Project%20Status-Completed-brightgreen.svg)]()

---

## 🎧 Project Overview & Persona

In the modern digital streaming ecosystem, automated recommendation algorithms, playlist curation, and listener skip behaviors dictate track longevity and commercial success. Music platforms and record labels face continuous challenges in identifying which acoustic and structural parameters drive listener engagement.

* **Target Persona:** Music Director & Mixing / Mastering Engineer
* **Core Objective:** Transition from speculative music production to evidence-based audio engineering by uncovering the statistical relationships between acoustic metrics (`loudness`, `energy`, `danceability`, `valence`, `tempo`), song architecture (`duration_ms`, `key`, `mode`, `time_signature`), and streaming popularity (`popularity`).
* **Analyzed Sample:** 62,204 validated track records released between 1971 and 2024.

---

## 📁 Repository Structure

```text
├── README.md                           # Comprehensive project documentation & findings
├── problem_statement.txt               # Evaluation rubric, questions & guidelines
├── spotify_tracks.csv                  # Full historical track dataset (62,317 raw rows)
├── spotify_data_description.csv        # Feature dictionary and definitions
├── spotify_tracks_eda.ipynb            # Fully executed, annotated Jupyter Notebook
├── Spotify_EDA_Subjective_Answers.pdf  # Comprehensive PDF report answering all subjective questions
├── figures/                            # High-resolution statistical visualization exports
│   ├── fig1_univariate_core.png        # Core distributions (Popularity, Duration, Loudness, Tempo)
│   ├── fig2_univariate_perceptual.png  # Boxplots & Violin plots of normalized audio features
│   ├── fig3_categorical_distributions.png # Key, Mode, Time Signature, and Language distributions
│   ├── fig4_correlation_heatmap.png    # Pearson correlation matrix heatmap
│   ├── fig5_bivariate_relationships.png# Regression plots vs. Popularity
│   ├── fig6_categorical_vs_popularity.png # Popularity by Language, Key, Mode & Meter
│   ├── fig7_multivariate_profile.png   # Top 25% Hits vs. Bottom 75% audio profile comparison
│   └── fig8_temporal_trends.png        # 5-Decade longitudinal trends (1970–2024)
└── scripts/                            # Dedicated pipeline & analysis scripts
    ├── generate_visualizations.py      # Script generating all figure assets
    ├── generate_notebook.py            # Script constructing the Jupyter Notebook structure
    ├── execute_notebook.py             # Runner executing all cells & capturing outputs
    ├── generate_pdf_report.py          # Script generating the publication-quality PDF deliverable
    └── compute_answers.py              # Script computing exact statistical question metrics
```

---

## 🔍 Data Hygiene & Auditing Findings

1. **Missing Values:** 0 null values across all 22 columns in the raw dataset.
2. **Exact Duplicates:** 78 duplicate rows were detected and purged.
3. **Corrupted Audio Sentinel Rows:** Exactly **35 tracks** possessed audio metrics (`acousticness`, `danceability`, `energy`, etc.) coded as `-1.0` and `loudness` coded as `-100,000.0 dB`. These were identified as failed Spotify Web API extractions and removed to prevent statistical distortion.
4. **Cleaned Dimensions:** **62,204 valid records** spanning 1971 through 2024.

---

## 📊 Key Analytical Insights

### 1. Univariate Profiling
* **Popularity (0–100):** Heavily right-skewed and zero-inflated (Mean: **15.36**, Median: **7.00**, Skewness: **+1.23**). **28.41% (17,672 tracks)** have a score of 0.0. Only **6.77%** exceed 50.0 points.
* **Duration:** Average song length is **4.05 minutes (242,705 ms)** with median **3.94 minutes**. The interquartile range (IQR) spans **3.21 to 4.77 minutes**. Outliers range from 10-second skits to 76-minute unabridged audiobooks.
* **Key & Modality:** **C Major/Minor (13.0%)**, **G (11.2%)**, and **D (11.0%)** dominate the catalog. Major mode accounts for **58.7%** vs. Minor mode at **41.3%**.
* **Meter & Production:** **85.6%** of tracks are in 4/4 time. Over **66%** lean electronic/amplified (`acousticness` < 0.50), while **74.6%** are danceable (`danceability` > 0.50) and **68.5%** are high-energy (`energy` > 0.50).

### 2. Bivariate Correlations with Popularity
| Feature | Pearson $r$ | $p$-value | Spearman $\rho$ | Studio Engineering Significance |
| :--- | :---: | :---: | :---: | :--- |
| **Loudness (dB)** | **+0.2012** | $< 10^{-300}$ | **+0.2040** | **#1 positive predictor.** Denser, competitive masters command higher engagement. |
| **Energy** | **+0.1474** | $< 10^{-298}$ | **+0.1314** | Driving rhythmic arrangements significantly outperform laid-back tracks. |
| **Acousticness** | **-0.1384** | $< 10^{-262}$ | **-0.1200** | **#1 negative predictor.** Organic/acoustic tracks face streaming headwinds. |
| **Instrumentalness** | **-0.1271** | $< 10^{-221}$ | **-0.0893** | Lack of lead vocals severely penalizes track popularity (-46.6%). |
| **Duration (ms)** | **-0.0404** | $6.13 \times 10^{-24}$ | **-0.0547** | Shorter tracks (3.0–3.8 min) yield higher replay loops and fewer skips. |
| **Danceability** | **+0.0421** | $9.21 \times 10^{-26}$ | **-0.0150** | Moderate baseline danceability floor ($\ge 0.60$) is mandatory for hits. |
| **Valence** | **+0.0092** | $0.0225$ | **-0.0322** | Near-zero linear effect: melancholic and euphoric tracks are equally viable. |

### 3. Multivariate "Hit Recipe" (Top 25% Popularity Quartile vs. Bottom 75%)
* **Energy:** 0.660 vs. 0.584 (**+13.0% higher energy**)
* **Loudness:** -7.25 dB vs. -9.53 dB (**+2.28 dB louder**)
* **Acousticness:** 0.297 vs. 0.386 (**-23.1% lower acousticness**)
* **Instrumentalness:** 0.080 vs. 0.169 (**-52.7% reduction**; vocals are critical)
* **Top Harmonic Combos:** C Major (4/4), D Major (4/4), G Major (4/4), and C#/Db Major (4/4).

### 4. Longitudinal Trends (1970–2024)
* **The Loudness War:** Average track loudness rose from **-10.21 dB** (1970s) to **-8.52 dB** (2010s), reflecting multi-decade limiting and compression evolution.
* **Duration Shrinkage:** Average duration declined from 4.25 minutes (1990s) to **3.78 minutes** (2020s), aligned with streaming monetization thresholds (30-second play counts).
* **Melancholic Drift:** Mean valence declined from **0.56** (1970s) to **0.48** (2020s), capturing a cultural preference for moodier songwriting.
* **Linguistic Globalization:** Non-English tracks (Korean, Tamil, Hindi) grew from < 15% pre-2000 to over **41%** of current streaming entries, with Korean leading all languages in average popularity (**27.56**).

---

## 🧪 Statistical Hypothesis Tests

| Hypothesis | Null ($H_0$) vs. Alternative ($H_1$) | Test Used | $p$-value | Decision & Business Meaning |
| :--- | :--- | :--- | :---: | :--- |
| **H1: Popularity Skew** | $H_0: \text{Median} = \mu \quad H_1: \text{Median} < \mu$ | Wilcoxon Signed-Rank | $< 10^{-300}$ | **Reject $H_0$:** Extreme right-skew (Median 7 vs. Mean 15.36; 28.4% zero scores). |
| **H2: Loudness Advantage** | $H_0: r = 0 \quad H_1: r > 0$ | Pearson Correlation | $< 10^{-300}$ | **Reject $H_0$:** Louder masters achieve significantly higher popularity ($r = +0.201$). |
| **H3: Radio Edit Duration** | $H_0: \mu_{\text{Radio}} = \mu_{\text{Long}} \quad H_1: \mu_{\text{Radio}} > \mu_{\text{Long}}$ | Welch's Two-Sample $t$-test | $2.41 \times 10^{-18}$ | **Reject $H_0$:** Tracks between 2.5–4.0m score 16.42 vs 13.88 for tracks > 4.5m (+18.3%). |
| **H4: Vocal vs. Instrumental** | $H_0: \mu_{\text{Vocal}} = \mu_{\text{Inst}} \quad H_1: \mu_{\text{Vocal}} > \mu_{\text{Inst}}$ | Welch's Two-Sample $t$-test | $< 10^{-100}$ | **Reject $H_0$:** Instrumental songs suffer a -46.6% popularity penalty (8.92 vs 16.71). |
| **H5: Language Difference** | $H_0: \mu_{\text{Korean}} = \mu_{\text{English}} \quad H_1: \mu_{\text{Korean}} > \mu_{\text{English}}$ | Welch's Two-Sample $t$-test | $< 10^{-150}$ | **Reject $H_0$:** Korean music achieves significantly higher average popularity (27.56 vs 14.77). |
| **H6: Meter Preference** | $H_0: \mu_{4/4} = \mu_{\text{Other}} \quad H_1: \mu_{4/4} > \mu_{\text{Other}}$ | Welch's Two-Sample $t$-test | $8.94 \times 10^{-65}$ | **Reject $H_0$:** 4/4 meter yields 15.95 popularity vs 11.83 for other time signatures. |

---

## 🎛️ Operational Directives for Studio Production

1. **Target the "Energetic & Danceable" Sound Profile:**
   * Spec: Danceability $\ge 0.62$, Energy $\ge 0.68$, Tempo $118–126\text{ BPM}$ in $4/4$ meter.
   * Action: Prioritize rhythm-forward mixes with tight low-end dynamics and punchy percussion.
2. **Master for Competitive Streaming Impact (-7.5 to -6.0 dB RMS):**
   * Spec: Aim for $-12$ to $-9\text{ LUFS}$ integrated loudness and $6–8\text{ dB}$ dynamic range.
   * Action: Use serial multi-band compression and soft clipping to project presence across mobile transducers without exceeding inter-sample peak thresholds.
3. **Structure Arrangements for Streaming Retention (3.0 to 3.8 Minutes):**
   * Spec: Keep intros $< 10$ seconds; introduce the hook/chorus within 45 seconds.
   * Action: Avoid prolonged outro vamps to prevent early skips, which depress algorithmic playlist velocity.
4. **Vocal-First Staging:**
   * Spec: Maintain instrumentalness $< 0.05$.
   * Action: Carve out competing instruments in the $1.5\text{ kHz} - 4.5\text{ kHz}$ vocal clarity range using dynamic sidechain EQ.
5. **International Collaborations & Multilingual Releases:**
   * Spec: Incorporate K-Pop-inspired dense arrangement layering and bilingual vocal hooks to access rapidly growing non-English streaming demographics.

---

## 🚀 Execution & Reproduction Guide

### Prerequisites
* Python 3.10+ (tested on Python 3.14)
* Recommended packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `reportlab`, `nbformat`

### Setup Instructions
```bash
# Clone the repository
git clone <repo-url>
cd spotify-tracks-eda

# Install dependencies
pip install pandas numpy matplotlib seaborn scipy reportlab nbformat

# Run full pipeline to regenerate visualizations, notebook, and PDF report
python scripts/generate_visualizations.py
python scripts/generate_notebook.py
python scripts/execute_notebook.py
python scripts/generate_pdf_report.py
```

---

## 📄 Deliverable Files Summary

* **Jupyter Notebook:** [spotify_tracks_eda.ipynb](file:///c:/Users/ayush/Desktop/Man%20hating/spotify_tracks_eda.ipynb)
* **Subjective Answers PDF:** [Spotify_EDA_Subjective_Answers.pdf](file:///c:/Users/ayush/Desktop/Man%20hating/Spotify_EDA_Subjective_Answers.pdf)
* **High-Resolution Figures:** [figures/](file:///c:/Users/ayush/Desktop/Man%20hating/figures/)

---
*Created as part of the Spotify Tracks Exploratory Data Analysis & Production Optimization Project.*

