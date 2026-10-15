# MAT2007 - Individual project 
# Do critics and audiences agree? Rotten Tomatoes scores

Author: Silvia Jimeno Ferrer (i6377278)

## Project description 

This project compares Rotten Tomatoes critic scores (Tomatometer) with audience
scores to answer two questions:

1. Do critics and audiences give different average scores?
2. Does the difference depend on the genre of the movie?

For each movie the difference *critic score − audience score* is computed. The
mean difference, its standard error of the mean (SEM = std / √n) and its
significance (mean / SEM, in σ) are calculated for all movies and for each
genre. A difference of 3σ or more is treated as significant.
Do Rotten Tomatoes critics and audiences give different scores on average, and does the answer depend on the genre?

## Data
`rotten_tomatoes_movies.csv`: Rotten Tomatoes movies dataset (17,712 movies, 22 columns), downloaded from Kaggle
(https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset).
Only three out of the 22 columns are used:
- `tomatometer_rating`: critic score (% of positive reviews from approved critics)
- `audience_rating`: audience score (% of positive user ratings)
- `genres`: genres of the movie (several genres in one cell)

## Files
| File | Description |
|------|-------------|
| `rotten_tomatoes_movies.csv` | Input dataset (17,712 movies, 22 columns) |
| `understanding_my_data.py` | Data exploration: columns, empty cells, score ranges |
| `rotten_tomatoes.py` | Main analysis: tests, cleaning, differences, SEM/sigma, genre comparison, subsampling, figures |
| `figures/` | Output plots: `difference_histogram.png`, `genre_errorbars.png` (created by the script) |
| `genre_results.csv` | Per-genre results table (created by the script) |
| `report.tex` | Project report (LaTeX) |

## How to run
## Requirements

- Python 3
- pandas
- numpy
- matplotlib
- scipy

1. Include the `rotten_tomatoes_movies.csv` file in the same folder as `rotten_tomatoes.py`.
2. Open a terminal in that folder and run:
   `python rotten_tomatoes.py`
3. Close each plot window to continue. The script prints the results, saves the figures in `figures/`. 

## What the script does
1. Runs small tests on its own functions (`All tests passed.`).
2. Loads the data and checks the columns exist.
3. Removes movies without both scores (17,712 to 17,407) and keeps the first listed genre of each movie.
4. Calculates, for the difference critic minus audience: mean, standard deviation, uncertainty (SEM) and significance in sigma (mean / SEM), plus the Pearson correlation.
5. Repeats the calculation per genre (genres with at least 30 movies).
6. Subsampling: splits the movies randomly in 10 groups to check the result is stable.
7. Saves a histogram of the differences and an error-bar plot per genre (error bars = 3 sigma).

## Main results
- Overall mean difference: **0.19 ± 0.16 points (1.2σ)** — no average difference.
- Standard deviation per movie: 21.6 points — individual movies differ a lot.
- Six genres differ by more than 3σ:
  - Critics rate higher: Documentary, Classics, Art House & International, Horror
  - Audiences rate higher: Comedy, Action & Adventure


## Limitations
- Only the first listed genre is used for each movie (genres appear to be
  listed alphabetically, so early-alphabet genres are over-represented).
- 305 movies without both scores were excluded.
- Subsampling shows the result is stable but does not prove the movies are
  independent.
