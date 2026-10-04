import pandas as pd

df = pd.read_csv("rotten_tomatoes_movies.csv")

print("Rows and columns:", df.shape) #rows gives us the number of movies and collums 
print()
print("Column titles:", df.columns.tolist()) #list of all column title - what information do I have?
print()
#Since we now know what all the columns are, we can select the ones we need for our analysis. 
#In this case, we will use the tomatometer_rating, audience_rating and genres columns - only 3 out of the 22 that we have 
print(df[["tomatometer_rating", "audience_rating", "genres"]].head(8)) #head 8 gives us the first 8 movies - this can be used to see how my data looks like 
print()
#we only want to filter the data from the columms that we are going to use 
print("Empty cells per column:") 
print(df[["tomatometer_rating", "audience_rating", "genres"]].isna().sum()) #counts empty cells in the data, if there are any they need need to be removed 
print()
print(df[["tomatometer_rating", "audience_rating"]].describe()) #shows the mean, std, min, max and quartiles of the data - this can be used to see if there are any outliers in the data 

#From the output we can see there are some empry cells in the data. They will be removed in the rotten_tomatoes.py file. 