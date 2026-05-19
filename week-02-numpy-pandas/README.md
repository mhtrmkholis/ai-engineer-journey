# Week 2 — Spotify Songs EDA

Exploratory Data Analysis on Spotify Songs dataset (~33k tracks across 6 genres).

Bagian dari [AI Engineer Journey](https://github.com/mhtrmkholis/ai-engineer-journey).

## Goal

Eksplorasi karakteristik 6 genre musik di Spotify (EDM, Pop, Latin, R&B, Rap, Rock) 
dan menganalisis pola popularity, audio features, dan hubungan keduanya.

## Top Findings

1. **Most tracks are unpopular**: median popularity 45, with heavily right-skewed distribution
2. **Pop & Latin dominate popularity** despite EDM being the most energetic genre
3. **Audio features cluster predictably**: energy-loudness strongly positive (r=0.7), 
   energy-acousticness inverse (r=-0.6)
4. **No single sound formula for popularity**: every audio feature correlates with 
   popularity at |r| < 0.15 — virality is multi-factorial
5. **Each genre has distinct audio DNA**: rap leads danceability (0.72), rock lags (0.52); 
   R&B is most acoustic (0.26); Latin most cheerful (valence 0.61)

## Visualizations

![Summary](./plots/00_summary_dashboard.png)

[See full EDA notebook →](./notebooks/04_spotify_eda.ipynb)

## Tech Stack

- **Python 3.12** + **uv** (package management)
- **Pandas, NumPy** (data manipulation)
- **Matplotlib, Seaborn** (visualization)
- **Jupyter** (interactive analysis)

## Setup

```bash
uv sync
uv run jupyter notebook
```

Open `notebooks/04_spotify_eda.ipynb`.

## What I Learned

- NumPy fundamentals: vectorization, broadcasting, axis operations
- Pandas: filtering, groupby, agg, unstack, method chaining
- Data viz: histogram, boxplot, scatter, heatmap with seaborn
- EDA discipline: question → analysis → insight, not just plotting
- Data quality assessment: detect, decide, document

## Dataset

[Spotify Songs (TidyTuesday 2020-01-21)](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21).

---

← Back to [AI Engineer Journey](https://github.com/mhtrmkholis/ai-engineer-journey) main repo.