"""Do critics and audiences agree? Analysis of Rotten Tomatoes scores.
Run with:  python rotten_tomatoes.py

Some of the comments mention where the functions are found in my lecture notes 
Also why I used them
And the ones that do not appear in the lecture notes, I looked them up - label as EXTRA in the comments 
"""

import os      #EXTRA: used only to create the 'figures' folder
import random  #Used for the subsampling

#If it isnt already installed, write in your terminal: 
try: 
    import matplotlib.pyplot as plt  #Needed for data visualisation. If it isnt already installed, write on your terminal: ./.venv/bin/python -m pip install matplotlib
    import numpy as np               #If it is not already installed, write on your terminal: ./.venv/bin/python -m pip install numpy
    import pandas as pd              #If it is not already installed, write on your terminal: ./.venv/bin/python -m pip install pandas
    from scipy import stats          #Used for the correlation and the moments. If it isn't already installed, write on your terminal: ./.venv/bin/python -m pip install pandas numpy scipy matplotlib
except ImportError as error:
    print(f"Error: a required package is missing ({error}).")
    print("Install them with: python -m pip install pandas numpy scipy matplotlib")
    exit(1)

#Settings: change these to match YOUR csv file . 
#All settings are in one place, so nothing is hard-coded below.
DATA_FILE = "rotten_tomatoes_movies.csv"
CRITIC_COL = "tomatometer_rating"
AUDIENCE_COL = "audience_rating"
GENRE_COL = "genres"
MIN_MOVIES_PER_GENRE = 30


#PART 1: Loading and cleaning the data
#Reading the data and checking that the columns we need are in it
def load_data(path, needed_columns):
    df = pd.read_csv(path) #read the csv file into a dataframe 

    #We are using a for loop, if statement, input validation (defensive programming)
    #If a column name is wrong, we stop with a clear message instead of a confusing error later.
    missing = []
    for col in needed_columns:
        if col not in df.columns:
            missing.append(col)
    if len(missing) > 0:
        raise ValueError(f"These columns are missing in the file: {missing}")
    return df

#We already know from the understanding_my_data.py file that there are some empty cells in the data that need to be removed
def clean_scores(df, critic_col, audience_col):
    #This adds a 'difference' column = critic score - audience score 
    #A movie without both scores cannot be compared.
    #EXTRA: dropna() and between() are pandas methods that are not shown in the notes.
    df = df.dropna(subset=[critic_col, audience_col]).copy()

    #Scores must be between 0 and 100
    in_range = df[critic_col].between(0, 100) & df[audience_col].between(0, 100)
    df = df[in_range].copy()

    #We are adding a new column and subtraction 
    #This is the number that we analyse: positive = critics rated the movie higher than the audience.
    df["difference"] = df[critic_col] - df[audience_col]
    return df

def add_main_genre(df, genre_col):
    #Each movie has several genres in one text, we are going to leave one main genre that will allow us to compare genres
    #String operations, new column
    #EXTRA: .str.split(), .str[0] and .fillna() are pandas methods not shown in the notes.    df = df.copy()
    df["main_genre"] = df[genre_col].fillna("Unknown").str.split(",").str[0].str.strip()
    return df


#PART 2: Statistics
def describe_values(values):
    """Mean, spread, uncertainty, significance (sigma) and shape of a set of numbers."""
    values = np.asarray(values, dtype=float)  # COURSE: NumPy arrays (5.1.1)
    n = len(values)

    #Mean and standard deviation
    #Mean --> will tell us the typical difference between critics and audience; std = how much it varies per movie.
    #ddof=1 means divide by n-1 (sample std)
    mean = np.mean(values)
    std = np.std(values, ddof=1)

    #Uncertainty of a measurement (5.2.2)
    sem = std / np.sqrt(n)

    return {  # COURSE: dictionaries are used in 5.1.3
        "n": n,
        "mean": mean,
        "std": std,
        "sem": sem,
        #Significance in sigma = mean / SEM = how many uncertainties the mean is away from 0
        "sigma": mean / sem,
        #Moments of a distribution - skewness and kurtosis 
        #They tell us if the differences look Gaussian (skewness ~ 0, kurtosis ~ 0).
        "skewness": stats.skew(values),
        "kurtosis": stats.kurtosis(values),
    }


def genre_summary(df, min_movies=30):
    """Mean difference (with SEM and sigma) per genre, ignoring genres with few movies."""
    #Grouping data 
    #To see if the difference between critics and audience depends on the genre.
    grouped = df.groupby("main_genre")["difference"].agg(["count", "mean", "std"])

    #Filtering. Genres with very few movies give a large uncertainty
    #(SEM = std / sqrt(n)), so we leave them out.
    grouped = grouped[grouped["count"] >= min_movies].copy()
    grouped["sem"] = grouped["std"] / np.sqrt(grouped["count"])
    grouped["sigma"] = grouped["mean"] / grouped["sem"]   #how many uncertainties the mean is away from 0
    return grouped.sort_values("mean")


def split_randomly(values, n_groups):
    """Shuffle a list of numbers and split it in n_groups random subsamples of equal size."""
    #Random numbers,for loop, lists (3.1.6).
    values = list(values)
    random.seed(1)
    random.shuffle(values)
    size = len(values) // n_groups
    groups = []
    for i in range(n_groups):
        groups.append(values[i * size:(i + 1) * size])
    return groups


# PART 3: Data visualisation
def plot_difference_histogram(differences, filename):
    #Histogram 
    #It shows the DISTRIBUTION of the differences (is it centred on 0? is it Gaussian?).
    #The legend shows how far the mean is from 0, in sigma.
    result = describe_values(differences)
    plt.hist(differences, bins=40, alpha=0.7, color="steelblue", edgecolor="black")
    plt.axvline(0, color="red", linestyle="--", linewidth=2, label="No difference (0)")
    plt.axvline(result["mean"], color="green", linewidth=2,
                label=f"Mean = {result['mean']:.2f} ({result['sigma']:.1f}σ from 0)")
    plt.title("Critic score minus audience score")
    plt.xlabel("Difference (score points)")
    plt.ylabel("Number of movies in each bar")
    plt.legend()
    plt.savefig(filename, dpi=200, bbox_inches="tight") #saves the figure 
    plt.show()


def plot_genre_errorbars(summary, filename):
    #Representing uncertainties with error bars and interpreting error bars (week 6 notes content)
    #It shows the mean difference per genre WITH its statistical uncertainty (error bars = n_sigma x SEM).
    #A genre is "clearly different" if its mean is more than n_sigma away from 0 (the bar does not touch the black line).
    n_sigma = 3
    plt.figure(figsize=(8, 5))
    for genre, mean, sem in zip(summary.index, summary["mean"], summary["sem"]):        
        sigma = mean / sem
        if sigma > n_sigma:
            color = "darkorange"      # more than n_sigma above 0: critics rate it higher
        elif sigma < -n_sigma:
            color = "steelblue"       # more than n_sigma below 0: audience rates it higher
        else:
            color = "gray"            # less than n_sigma away from 0: no clear difference
        plt.errorbar(mean, genre, xerr=n_sigma * sem, fmt="o", capsize=4,
                     color=color, markersize=7)

    #Empty plots, only to create the legend
    plt.plot([], [], "o", color="darkorange", label=f"Critics rate higher (more than {n_sigma}σ)")
    plt.plot([], [], "o", color="steelblue", label=f"Audience rates higher (more than {n_sigma}σ)")
    plt.plot([], [], "o", color="gray", label=f"No clear difference (less than {n_sigma}σ)")

    plt.axvline(0, color="black", linestyle="--", linewidth=1.5)
    plt.title(f"Mean difference per genre (error bars = ±{n_sigma}σ)")
    plt.xlabel("Critic minus audience score (points)")
    plt.ylabel("Genre")
    plt.grid(axis="x", alpha=0.3)
    plt.legend(loc="lower right")
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.show()


#PART 4: Small tests (they run before the analysis) - Testing and debugging 
#Used to check that the functions give the right answer on examples where I know the result.

def run_tests():
    # Intuition/black box test
    result = describe_values([2, 4, 6, 8, 10])
    assert result["mean"] == 6
    assert abs(result["std"] - 3.1623) < 0.001

    #More data -> smaller statistical uncertainty
    small = describe_values([1, 2, 3, 4] * 5)
    large = describe_values([1, 2, 3, 4] * 500)
    assert large["sem"] < small["sem"]

    #Boundary check: missing values and scores above 100 must be removed
    df = pd.DataFrame({"critic": [50, None, 120, 80], "audience": [60, 70, 50, 75]})
    cleaned = clean_scores(df, "critic", "audience")
    assert len(cleaned) == 2
    assert list(cleaned["difference"]) == [-10, 5]

    #Only the first genre is kept
    df = pd.DataFrame({"genres": ["Comedy, Drama", None]})
    assert list(add_main_genre(df, "genres")["main_genre"]) == ["Comedy", "Unknown"]

    #Splitting in random subsamples: 100 numbers in 4 groups of 25
    groups = split_randomly(list(range(100)), 4)
    assert len(groups) == 4
    assert len(groups[0]) == 25

    print("All tests passed.")


#PART 5: Run everything and print after each one to make sure it runs. 
run_tests()
os.makedirs("figures", exist_ok=True)  #Creates the folder for the figures if it does not exist

#1. Load the data
try:
    df = load_data(DATA_FILE, [CRITIC_COL, AUDIENCE_COL, GENRE_COL])
except FileNotFoundError:
    print(f"Error: cannot find '{DATA_FILE}'. Put it in the same folder as this script.")
    exit(1)
print(f"Rows in file: {len(df)}")

#2.Clean the data - it shows the amount of movies that were removed
df = clean_scores(df, CRITIC_COL, AUDIENCE_COL)
df = add_main_genre(df, GENRE_COL)
print(f"Movies after cleaning: {len(df)}")

#3. Statistics --> here we have our quantitative results that we will use in our report
#Every number comes with its uncertainty (SEM) and its significance in sigma
#Quantitative results for the report.
diff_stats = describe_values(df["difference"])
print()
print("RESULT 1: do they give the same scores on average?")
print(f"  Mean difference (critic - audience): {diff_stats['mean']:.2f} +/- {diff_stats['sem']:.2f} (SEM)")
print(f"  Significance: {diff_stats['sigma']:.1f} sigma from 0")
print(f"  Standard deviation: {diff_stats['std']:.2f}")
print(f"  Skewness: {diff_stats['skewness']:.2f}, kurtosis: {diff_stats['kurtosis']:.2f}")

genres = genre_summary(df, MIN_MOVIES_PER_GENRE)
print()
print("RESULT 3: does it depend on the genre?")
print(genres[["count", "mean", "sem", "sigma"]].round(2))
genres.to_csv("genre_results.csv")

#4. Subsampling: is the result a coincidence of particular movies?
#If the result is real, random subsamples should give similar answers.
print()
print("SUBSAMPLING: mean difference in 10 random subsamples")
groups = split_randomly(df["difference"], 10)
inside = 0
for i in range(len(groups)):
    part = describe_values(groups[i])
    print(f"  Subsample {i + 1}: {part['mean']:.2f} +/- {part['sem']:.2f} ({part['sigma']:.1f} sigma from 0)")
    if abs(part["mean"] - diff_stats["mean"]) < part["sem"]:
        inside += 1
print(f"  Subsamples within 1 sigma of the overall mean: {inside} of 10 (expected about 7)")

#5. Figures: each one is saved as a .png file in the 'figures' folder
#The code that makes them is in PART 3, here we only call the functions
plot_difference_histogram(df["difference"], "figures/difference_histogram.png")
plot_genre_errorbars(genres, "figures/genre_errorbars.png")
print("Done.")