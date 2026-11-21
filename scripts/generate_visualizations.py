import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

os.makedirs('figures', exist_ok=True)

# Load and clean dataset
df = pd.read_csv('spotify_tracks.csv')
df_clean = df.drop_duplicates().copy()
df_clean = df_clean[df_clean['acousticness'] >= 0].copy()
df_clean['duration_min'] = df_clean['duration_ms'] / 60000.0
df_clean['decade'] = (df_clean['year'] // 10) * 10

key_map = {-1: 'No Key', 0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E', 5: 'F', 
           6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'}
df_clean['key_name'] = df_clean['key'].astype(int).map(key_map)

# -------------------------------------------------------------
# Figure 1: Univariate Core Distributions
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Popularity
ax = axes[0, 0]
sns.histplot(df_clean['popularity'], bins=40, kde=True, color='#1DB954', ax=ax, edgecolor='black', alpha=0.6)
ax.axvline(df_clean['popularity'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df_clean['popularity'].mean():.1f}")
ax.axvline(df_clean['popularity'].median(), color='blue', linestyle='-', linewidth=2, label=f"Median: {df_clean['popularity'].median():.1f}")
ax.set_title("Popularity Score Distribution (Zero-Inflated)")
ax.set_xlabel("Popularity (0 - 100)")
ax.set_ylabel("Track Count")
ax.legend()

# 2. Duration (Minutes, capped at 12 for visualization)
ax = axes[0, 1]
dur_cap = df_clean['duration_min'].clip(upper=10)
sns.histplot(dur_cap, bins=35, kde=True, color='#2E86AB', ax=ax, edgecolor='black', alpha=0.6)
ax.axvline(df_clean['duration_min'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df_clean['duration_min'].mean():.2f} min")
ax.axvline(df_clean['duration_min'].median(), color='blue', linestyle='-', linewidth=2, label=f"Median: {df_clean['duration_min'].median():.2f} min")
ax.set_title("Track Duration (Minutes, Capped at 10 min)")
ax.set_xlabel("Duration (Minutes)")
ax.set_ylabel("Track Count")
ax.legend()

# 3. Loudness
ax = axes[1, 0]
sns.histplot(df_clean['loudness'], bins=40, kde=True, color='#E74C3C', ax=ax, edgecolor='black', alpha=0.6)
ax.axvline(df_clean['loudness'].mean(), color='darkred', linestyle='--', linewidth=2, label=f"Mean: {df_clean['loudness'].mean():.1f} dB")
ax.axvline(df_clean['loudness'].median(), color='blue', linestyle='-', linewidth=2, label=f"Median: {df_clean['loudness'].median():.1f} dB")
ax.set_title("Loudness Distribution (dB)")
ax.set_xlabel("Loudness (dB)")
ax.set_ylabel("Track Count")
ax.legend()

# 4. Tempo
ax = axes[1, 1]
sns.histplot(df_clean['tempo'], bins=40, kde=True, color='#9B59B6', ax=ax, edgecolor='black', alpha=0.6)
ax.axvline(df_clean['tempo'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df_clean['tempo'].mean():.1f} BPM")
ax.axvline(df_clean['tempo'].median(), color='blue', linestyle='-', linewidth=2, label=f"Median: {df_clean['tempo'].median():.1f} BPM")
ax.set_title("Tempo Distribution (BPM)")
ax.set_xlabel("Estimated Tempo (BPM)")
ax.set_ylabel("Track Count")
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig1_univariate_core.png')
plt.close()

# -------------------------------------------------------------
# Figure 2: Normalized Audio Features (Boxplots & Violin)
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

norm_features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness', 'liveness']

# Box plot
ax = axes[0]
sns.boxplot(data=df_clean[norm_features], palette='Set2', ax=ax, fliersize=2)
ax.set_title("Boxplot of Normalized Audio Features [0.0 - 1.0]")
ax.set_ylabel("Feature Value")
ax.set_xticklabels(norm_features, rotation=30, ha='right')

# Violin plot
ax = axes[1]
sns.violinplot(data=df_clean[norm_features], palette='Set2', ax=ax, cut=0)
ax.set_title("Density & Distribution Shape (Violin Plots)")
ax.set_ylabel("Density / Value")
ax.set_xticklabels(norm_features, rotation=30, ha='right')

plt.tight_layout()
plt.savefig('figures/fig2_univariate_perceptual.png')
plt.close()

# -------------------------------------------------------------
# Figure 3: Categorical & Discrete Distributions
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# Key
ax = axes[0, 0]
key_order = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
key_counts = df_clean['key_name'].value_counts()
sns.barplot(x=key_counts.index, y=key_counts.values, ax=ax, palette='Blues_r', order=key_order)
ax.set_title("Track Count by Musical Key (0 to 11)")
ax.set_xlabel("Musical Key")
ax.set_ylabel("Track Count")
ax.tick_params(axis='x', rotation=30)

# Mode
ax = axes[0, 1]
mode_df = df_clean['mode'].map({1: 'Major (1)', 0: 'Minor (0)'}).value_counts()
sns.barplot(x=mode_df.index, y=mode_df.values, ax=ax, palette=['#3498DB', '#E67E22'])
ax.set_title(f"Modality Distribution (Major: {mode_df['Major (1)']/len(df_clean)*100:.1f}%, Minor: {mode_df['Minor (0)']/len(df_clean)*100:.1f}%)")
ax.set_xlabel("Mode")
ax.set_ylabel("Track Count")

# Time Signature
ax = axes[1, 0]
ts_counts = df_clean['time_signature'].astype(int).value_counts().sort_index()
sns.barplot(x=ts_counts.index.astype(str) + "/4", y=ts_counts.values, ax=ax, palette='Purples_r')
ax.set_title("Time Signature Distribution (Beats per Measure)")
ax.set_xlabel("Time Signature")
ax.set_ylabel("Track Count")

# Language
ax = axes[1, 1]
lang_counts = df_clean['language'].value_counts()
sns.barplot(x=lang_counts.index, y=lang_counts.values, ax=ax, palette='Greens_r')
ax.set_title("Language Distribution of Lyrics")
ax.set_xlabel("Language Category")
ax.set_ylabel("Track Count")
ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig('figures/fig3_categorical_distributions.png')
plt.close()

# -------------------------------------------------------------
# Figure 4: Correlation Heatmap
# -------------------------------------------------------------
plt.figure(figsize=(11, 9))
features_for_corr = ['popularity', 'energy', 'loudness', 'danceability', 'valence', 
                     'tempo', 'duration_min', 'acousticness', 'instrumentalness', 'speechiness', 'liveness']
corr_mat = df_clean[features_for_corr].corr()

mask = np.triu(np.ones_like(corr_mat, dtype=bool))
sns.heatmap(corr_mat, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-0.8, vmax=0.8, 
            square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title("Correlation Heatmap: Audio Features vs. Popularity", fontsize=15, pad=15)
plt.tight_layout()
plt.savefig('figures/fig4_correlation_heatmap.png')
plt.close()

# -------------------------------------------------------------
# Figure 5: Bivariate Relationships vs Popularity
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# Loudness vs Popularity
ax = axes[0, 0]
sns.regplot(data=df_clean.sample(5000, random_state=42), x='loudness', y='popularity', ax=ax,
            scatter_kws={'alpha': 0.15, 'color': '#E74C3C', 's': 10}, line_kws={'color': 'darkred', 'linewidth': 2})
ax.set_title("Loudness vs. Popularity (Pearson r = +0.20)")
ax.set_xlabel("Loudness (dB)")
ax.set_ylabel("Popularity (0 - 100)")
ax.set_xlim(-30, 2)

# Energy vs Popularity
ax = axes[0, 1]
sns.regplot(data=df_clean.sample(5000, random_state=42), x='energy', y='popularity', ax=ax,
            scatter_kws={'alpha': 0.15, 'color': '#F39C12', 's': 10}, line_kws={'color': 'black', 'linewidth': 2})
ax.set_title("Energy vs. Popularity (Pearson r = +0.15)")
ax.set_xlabel("Energy Score [0.0 - 1.0]")
ax.set_ylabel("Popularity (0 - 100)")

# Acousticness vs Popularity
ax = axes[1, 0]
sns.regplot(data=df_clean.sample(5000, random_state=42), x='acousticness', y='popularity', ax=ax,
            scatter_kws={'alpha': 0.15, 'color': '#2980B9', 's': 10}, line_kws={'color': 'navy', 'linewidth': 2})
ax.set_title("Acousticness vs. Popularity (Pearson r = -0.14)")
ax.set_xlabel("Acousticness Score [0.0 - 1.0]")
ax.set_ylabel("Popularity (0 - 100)")

# Danceability vs Popularity
ax = axes[1, 1]
sns.regplot(data=df_clean.sample(5000, random_state=42), x='danceability', y='popularity', ax=ax,
            scatter_kws={'alpha': 0.15, 'color': '#27AE60', 's': 10}, line_kws={'color': 'darkgreen', 'linewidth': 2})
ax.set_title("Danceability vs. Popularity (Pearson r = +0.04)")
ax.set_xlabel("Danceability Score [0.0 - 1.0]")
ax.set_ylabel("Popularity (0 - 100)")

plt.tight_layout()
plt.savefig('figures/fig5_bivariate_relationships.png')
plt.close()

# -------------------------------------------------------------
# Figure 6: Categorical & Structural Influences on Popularity
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# Language vs Popularity
ax = axes[0, 0]
lang_order = df_clean.groupby('language')['popularity'].mean().sort_values(ascending=False).index
sns.barplot(data=df_clean, x='language', y='popularity', order=lang_order, palette='viridis', ax=ax, errorbar='ci')
ax.set_title("Mean Popularity by Language Category (95% CI)")
ax.set_xlabel("Language")
ax.set_ylabel("Mean Popularity")
ax.tick_params(axis='x', rotation=30)

# Mode vs Popularity (Boxplot)
ax = axes[0, 1]
mode_plot_df = df_clean.copy()
mode_plot_df['mode_label'] = mode_plot_df['mode'].map({1: 'Major (1)', 0: 'Minor (0)'})
sns.boxplot(data=mode_plot_df, x='mode_label', y='popularity', palette=['#3498DB', '#E67E22'], ax=ax, showmeans=True,
            meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
ax.set_title("Popularity Distribution by Mode (Major vs. Minor)")
ax.set_xlabel("Modality")
ax.set_ylabel("Popularity")

# Musical Key vs Popularity
ax = axes[1, 0]
key_pop_order = df_clean.groupby('key_name')['popularity'].mean().sort_values(ascending=False).index
sns.barplot(data=df_clean, x='key_name', y='popularity', order=key_pop_order, palette='mako', ax=ax, errorbar='ci')
ax.set_title("Mean Popularity across Musical Keys (Ranked)")
ax.set_xlabel("Musical Key")
ax.set_ylabel("Mean Popularity")
ax.tick_params(axis='x', rotation=30)

# Time Signature vs Popularity
ax = axes[1, 1]
ts_plot = df_clean[df_clean['time_signature'].isin([1, 3, 4, 5])].copy()
ts_plot['ts_label'] = ts_plot['time_signature'].astype(int).astype(str) + "/4"
sns.barplot(data=ts_plot, x='ts_label', y='popularity', order=['4/4', '3/4', '5/4', '1/4'], palette='plasma', ax=ax, errorbar='ci')
ax.set_title("Mean Popularity by Time Signature")
ax.set_xlabel("Time Signature Meter")
ax.set_ylabel("Mean Popularity")

plt.tight_layout()
plt.savefig('figures/fig6_categorical_vs_popularity.png')
plt.close()

# -------------------------------------------------------------
# Figure 7: Multivariate Top 25% (Q4) Recipe vs Rest
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

q4_thresh = df_clean['popularity'].quantile(0.75)
df_clean['segment'] = np.where(df_clean['popularity'] >= q4_thresh, 'Top 25% (Hit Quadrant)', 'Bottom 75%')

features_compare = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'speechiness']
mean_comp = df_clean.groupby('segment')[features_compare].mean().T

# Bar comparison
ax = axes[0]
mean_comp.plot(kind='bar', ax=ax, color=['#95A5A6', '#1DB954'], edgecolor='black', alpha=0.85)
ax.set_title("Acoustic Feature Comparison: Top 25% Hits vs. Bottom 75%")
ax.set_ylabel("Mean Score [0.0 - 1.0]")
ax.set_xticklabels(features_compare, rotation=30, ha='right')
ax.legend(title="Track Segment")

# Top 25% Audio Profile Across Languages
ax = axes[1]
top_25_df = df_clean[df_clean['segment'] == 'Top 25% (Hit Quadrant)']
lang_means = top_25_df.groupby('language')[['danceability', 'energy', 'valence']].mean()
lang_means.plot(kind='bar', ax=ax, colormap='Accent', edgecolor='black', alpha=0.85)
ax.set_title("Top 25% Hits Sound Profile across Languages")
ax.set_ylabel("Score [0.0 - 1.0]")
ax.set_xlabel("Language")
ax.tick_params(axis='x', rotation=30)
ax.legend(title="Audio Dimension")

plt.tight_layout()
plt.savefig('figures/fig7_multivariate_profile.png')
plt.close()

# -------------------------------------------------------------
# Figure 8: Historical / Temporal Trends Across Decades
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

decade_df = df_clean[df_clean['decade'] >= 1970].groupby('decade').agg({
    'loudness': 'mean',
    'duration_min': 'mean',
    'energy': 'mean',
    'danceability': 'mean',
    'valence': 'mean',
    'acousticness': 'mean'
}).reset_index()

# 1. Loudness Wars
ax = axes[0, 0]
ax.plot(decade_df['decade'], decade_df['loudness'], marker='o', color='#E74C3C', linewidth=2.5, markersize=8)
ax.set_title("The Loudness War: Track Loudness over Decades")
ax.set_xlabel("Decade")
ax.set_ylabel("Average Loudness (dB)")
for _, r in decade_df.iterrows():
    ax.annotate(f"{r['loudness']:.1f} dB", (r['decade'], r['loudness'] + 0.2), ha='center', fontweight='bold')

# 2. Track Duration Decay
ax = axes[0, 1]
ax.plot(decade_df['decade'], decade_df['duration_min'], marker='s', color='#2980B9', linewidth=2.5, markersize=8)
ax.set_title("Song Length Evolution: Duration Shrinkage")
ax.set_xlabel("Decade")
ax.set_ylabel("Average Duration (Minutes)")
for _, r in decade_df.iterrows():
    ax.annotate(f"{r['duration_min']:.2f} m", (r['decade'], r['duration_min'] + 0.05), ha='center', fontweight='bold')

# 3. Energy & Danceability Shifts
ax = axes[1, 0]
ax.plot(decade_df['decade'], decade_df['energy'], marker='^', color='#F39C12', linewidth=2.5, label='Energy')
ax.plot(decade_df['decade'], decade_df['danceability'], marker='d', color='#27AE60', linewidth=2.5, label='Danceability')
ax.plot(decade_df['decade'], decade_df['acousticness'], marker='v', color='#8E44AD', linewidth=2.5, label='Acousticness')
ax.set_title("Production Shifts: Energy, Danceability & Acousticness")
ax.set_xlabel("Decade")
ax.set_ylabel("Average Score [0.0 - 1.0]")
ax.legend()

# 4. Emotional Valence Trajectory
ax = axes[1, 1]
ax.plot(decade_df['decade'], decade_df['valence'], marker='o', color='#D35400', linewidth=2.5, markersize=8)
ax.set_title("Emotional Positivity (Valence) over Decades")
ax.set_xlabel("Decade")
ax.set_ylabel("Average Valence Score [0.0 - 1.0]")
for _, r in decade_df.iterrows():
    ax.annotate(f"{r['valence']:.3f}", (r['decade'], r['valence'] + 0.01), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('figures/fig8_temporal_trends.png')
plt.close()

print("All 8 figures successfully generated in figures/ directory!")

