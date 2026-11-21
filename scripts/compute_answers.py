import pandas as pd
import numpy as np
from scipy import stats

# Load dataset
df = pd.read_csv('spotify_tracks.csv')

# Clean data: drop exact duplicates and corrupted sentinel rows
df_clean = df.drop_duplicates().copy()
df_clean = df_clean[df_clean['acousticness'] >= 0].copy()

# Add duration in minutes
df_clean['duration_min'] = df_clean['duration_ms'] / 60000.0

# Decade column
df_clean['decade'] = (df_clean['year'] // 10) * 10

print("="*60)
print("SECTION 1: UNIVARIATE ANALYSIS")
print("="*60)

# 1. Popularity distribution
pop = df_clean['popularity']
print(f"Popularity: Mean={pop.mean():.2f}, Std={pop.std():.2f}, Median={pop.median():.2f}, Skewness={pop.skew():.2f}")
print(f"Quartiles: Q1={pop.quantile(0.25)}, Q2={pop.quantile(0.50)}, Q3={pop.quantile(0.75)}, IQR={pop.quantile(0.75)-pop.quantile(0.25)}")
print(f"Zeros count: {(pop == 0).sum()} ({(pop == 0).mean()*100:.2f}%)")
print(f"Scores > 50: {(pop > 50).sum()} ({(pop > 50).mean()*100:.2f}%)")

# 2. Duration
dur = df_clean['duration_ms']
dur_m = df_clean['duration_min']
print(f"\nDuration: Mean={dur.mean():.1f} ms ({dur_m.mean():.2f} min), Median={dur.median():.1f} ms ({dur_m.median():.2f} min)")
print(f"Duration IQR: Q1={dur_m.quantile(0.25):.2f} min, Q3={dur_m.quantile(0.75):.2f} min, Range=[{dur_m.min():.2f}, {dur_m.max():.2f}] min")

# 3. Keys
key_map = {-1: 'No Key', 0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E', 5: 'F', 
           6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'}
df_clean['key_name'] = df_clean['key'].astype(int).map(key_map)
key_counts = df_clean['key_name'].value_counts()
print(f"\nKey distribution (Top 5):\n{key_counts.head(5)}")

# 4. Tempo
tempo = df_clean['tempo']
print(f"\nTempo: Mean={tempo.mean():.2f} BPM, Median={tempo.median():.2f} BPM, Std={tempo.std():.2f}, Range=[{tempo.min():.1f}, {tempo.max():.1f}]")

# 5. Acousticness
acoust = df_clean['acousticness']
print(f"\nAcousticness: Mean={acoust.mean():.3f}, Median={acoust.median():.3f}, % > 0.5: {(acoust > 0.5).mean()*100:.2f}% (electronic lean)")

# 6. Loudness
loud = df_clean['loudness']
print(f"\nLoudness: Mean={loud.mean():.2f} dB, Median={loud.median():.2f} dB, Range=[{loud.min():.2f}, {loud.max():.2f}] dB, Std={loud.std():.2f}")

# 7. Danceability
dance = df_clean['danceability']
print(f"\nDanceability: Mean={dance.mean():.3f}, Median={dance.median():.3f}, % > 0.5: {(dance > 0.5).mean()*100:.2f}% (danceable lean)")

# 8. Energy
energy = df_clean['energy']
print(f"\nEnergy: Mean={energy.mean():.3f}, Median={energy.median():.3f}, % > 0.5: {(energy > 0.5).mean()*100:.2f}% (high energy lean)")

# 9. Time Signature
ts_counts = df_clean['time_signature'].astype(int).value_counts()
print(f"\nTime signature distribution:\n{ts_counts}")

# 10. Speechiness
speech = df_clean['speechiness']
print(f"\nSpeechiness: Mean={speech.mean():.3f}, Median={speech.median():.3f}, % < 0.33 (music): {(speech < 0.33).mean()*100:.2f}%")

# 11. Valence
val = df_clean['valence']
print(f"\nValence: Mean={val.mean():.3f}, Median={val.median():.3f}, Skewness={val.skew():.3f}")

# 12. Instrumentalness
inst = df_clean['instrumentalness']
print(f"\nInstrumentalness: Mean={inst.mean():.3f}, Median={inst.median():.3f}, % < 0.1 (vocal): {(inst < 0.1).mean()*100:.2f}%")

# 13. Liveness
live = df_clean['liveness']
print(f"\nLiveness: Mean={live.mean():.3f}, Median={live.median():.3f}, % < 0.8 (studio): {(live < 0.8).mean()*100:.2f}%")

# 14. Mode
mode_counts = df_clean['mode'].astype(int).value_counts()
print(f"\nMode distribution: 1 (Major) = {mode_counts.get(1, 0)} ({mode_counts.get(1, 0)/len(df_clean)*100:.1f}%), 0 (Minor) = {mode_counts.get(0, 0)} ({mode_counts.get(0, 0)/len(df_clean)*100:.1f}%)")

# 16. Modal energy level (binning)
energy_bins = pd.cut(df_clean['energy'], bins=10)
print(f"\nModal Energy bin (10 bins):\n{energy_bins.value_counts().head(3)}")

# 17. Language distribution
lang_counts = df_clean['language'].value_counts()
print(f"\nLanguage distribution:\n{lang_counts}")

print("\n" + "="*60)
print("SECTION 2: BIVARIATE ANALYSIS (CORRELATIONS & RELATIONSHIPS)")
print("="*60)

corr_features = ['duration_ms', 'danceability', 'energy', 'loudness', 'acousticness',
                 'valence', 'instrumentalness', 'liveness', 'tempo']

for feat in corr_features:
    p_corr, p_val = stats.pearsonr(df_clean[feat], df_clean['popularity'])
    s_corr, _ = stats.spearmanr(df_clean[feat], df_clean['popularity'])
    print(f"{feat:16s}: Pearson r={p_corr:+.4f} (p={p_val:.2e}), Spearman rho={s_corr:+.4f}")

# Language vs Popularity
print("\nLanguage vs Popularity (Mean, Median, Count):")
print(df_clean.groupby('language')['popularity'].agg(['count', 'mean', 'median', 'std']).sort_values('mean', ascending=False))

# Key & Mode vs Popularity
print("\nMode vs Popularity:")
print(df_clean.groupby('mode')['popularity'].agg(['count', 'mean', 'median']))

print("\nKey vs Popularity (Top 5 by Mean Popularity):")
print(df_clean.groupby('key_name')['popularity'].agg(['count', 'mean', 'median']).sort_values('mean', ascending=False).head(5))

# Time Signature vs Popularity
print("\nTime Signature vs Popularity:")
print(df_clean.groupby('time_signature')['popularity'].agg(['count', 'mean', 'median']))

print("\n" + "="*60)
print("SECTION 3: MULTIVARIATE ANALYSIS")
print("="*60)

# Highest popularity quartile (Q4)
q4_threshold = df_clean['popularity'].quantile(0.75)
top_25 = df_clean[df_clean['popularity'] >= q4_threshold]
bottom_75 = df_clean[df_clean['popularity'] < q4_threshold]

print(f"Q4 Threshold (Top 25% Popularity): >= {q4_threshold}")
print(f"Top 25% count: {len(top_25)}, Bottom 75% count: {len(bottom_75)}")

print("\nFeature Comparison: Top 25% vs Bottom 75%:")
compare_cols = ['danceability', 'energy', 'valence', 'loudness', 'tempo', 'acousticness', 'instrumentalness', 'speechiness', 'liveness', 'duration_min']
comp_df = pd.DataFrame({
    'Top 25% Mean': top_25[compare_cols].mean(),
    'Bottom 75% Mean': bottom_75[compare_cols].mean(),
    'Top 25% Median': top_25[compare_cols].median(),
    'Bottom 75% Median': bottom_75[compare_cols].median()
})
print(comp_df.round(3))

# High popularity recipes by language
print("\nTop 25% Popularity Audio Profile by Language:")
print(top_25.groupby('language')[['danceability', 'energy', 'valence', 'loudness', 'tempo']].mean().round(3))

# Key, Mode & Time signature combined
top_25['combo'] = top_25['key_name'] + " " + top_25['mode'].map({1: 'Major', 0: 'Minor'}).fillna('Unknown') + " (" + top_25['time_signature'].astype(int).astype(str) + "/4)"
print("\nTop 5 Musical Key/Mode/Time_Signature Combos in Top 25% Popularity:")
print(top_25['combo'].value_counts().head(5))

print("\n" + "="*60)
print("SECTION 4: TIME-SERIES & TEMPORAL TRENDS")
print("="*60)

print("\nDecade Evolution (Mean Values):")
decade_summary = df_clean.groupby('decade')[['popularity', 'loudness', 'duration_min', 'energy', 'danceability', 'valence', 'acousticness', 'instrumentalness', 'speechiness', 'liveness']].mean()
print(decade_summary.round(3))

