# MAT2007 - Individual project 
# Do critics and audiences agree? Rotten Tomatoes scores

Author: Silvia Jimeno Ferrer (i6377278)

## Question
Do Rotten Tomatoes critics and audiences give different scores on average, and does the answer depend on the genre?

## Data
`rotten_tomatoes_movies.csv`: Rotten Tomatoes movies dataset (17,712 movies, 22 columns), downloaded from Kaggle
(https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset).
Only three out of the 22 columns are used:
- `tomatometer_rating`: critic score (% of positive reviews from approved critics)
- `audience_rating`: audience score (% of positive user ratings)
- `genres`: genres of the movie (several genres in one cell)

## Files
| File | What it is |
|---|---|
| `rotten_tomatoes.py` | The analysis (one script, run it from top to bottom) |
| `understanding_my_data.py` | First look at the data: columns, first rows, empty cells |
| `rotten_tomatoes_movies.csv` | The data (put it in the same folder as the script) |
| `figures/` | File that contains the plots made|
| `genre_error bars.png | Mean difference per genre with sigma |
| `difference_histogram.png | Difference between critic and audience scores|
| `report.pdf` | The report |

## How to run
1. Install Python 3 and the packages:
   `python -m pip install pandas numpy scipy matplotlib`
2. Include the `rotten_tomatoes_movies.csv` file in the same folder as `rotten_tomatoes.py`.
3. Open a terminal in that folder and run:
   `python rotten_tomatoes.py`
4. Close each plot window to continue. The script prints the results, saves the figures in `figures/`. 

## What the script does
1. Runs small tests on its own functions (`All tests passed.`).
2. Loads the data and checks the columns exist.
3. Removes movies without both scores (17,712 to 17,407) and keeps the first listed genre of each movie.
4. Calculates, for the difference critic minus audience: mean, standard deviation, uncertainty (SEM) and significance in sigma (mean / SEM), plus the Pearson correlation.
5. Repeats the calculation per genre (genres with at least 30 movies).
6. Subsampling: splits the movies randomly in 10 groups to check the result is stable.
7. Saves a histogram of the differences and an error-bar plot per genre (error bars = 3 sigma).

## Main results
- Mean difference (critic - audience) = 0.19 +/- 0.16 points = 1.2 sigma: no significant average difference.
- Pearson correlation r = 0.654.
- Six genres are more than 3 sigma away from 0: critics rate higher in Documentary, Classics, Art House and Horror; the audience rates higher in Comedy and Action & Adventure.
