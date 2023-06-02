import numpy as np
import pandas as pd

from helper import *
from sklearn.neighbors import NearestNeighbors



def main():
    # read in relevant datasets
    movies = read_files(fname="data2/movies.csv")
    ratings = read_files(fname="data2/ratings.csv")

    rating_pivot = ratings.pivot_table(values='rating', columns='userId', index='movieId').fillna(0)
    nn_algo = NearestNeighbors(metric='cosine')
    nn_algo.fit(rating_pivot)

    class Recommender:    
        def __init__(self):
            self.hist = []
            self.ishist = False
        
        def recommend_on_movie(self, movie, n_reccomend = 5):
            # self.ishist = True
            
            # check if movie entered is valid in database
            if movie not in movies['title'].unique():
                return print(movie, "not in database")

            # add movie id to history
            movieid = int(movies[movies['title'] == movie]['movieId'])
            # self.hist.append(movieid)

            # run nn to find most similar movies
            distance, neighbors = nn_algo.kneighbors([rating_pivot.loc[movieid]], n_neighbors=n_reccomend + 1)
            movieids = [rating_pivot.iloc[i].name for i in neighbors[0]]
            recommeds = [str(movies[movies['movieId'] == mid]['title']).split('\n')[0].split('    ')[-1] for mid in movieids if mid not in [movieid]]
            return recommeds[:n_reccomend]
        
        def recommend_on_history(self, n_reccomend = 5):
            # return if history is empty
            if self.ishist == False:
                return print('No history found')
            
            history = np.array([list(rating_pivot.loc[mid]) for mid in self.hist])
            distance, neighbors = nn_algo.kneighbors([np.average(history, axis=0)], n_neighbors=n_reccomend + len(self.hist))
            movieids = [rating_pivot.iloc[i].name for i in neighbors[0]]
            recommeds = [str(movies[movies['movieId'] == mid]['title']).split('\n')[0].split('    ')[-1] for mid in movieids if mid not in self.hist]
            return recommeds[:n_reccomend]
    
      
    print("\n\nThis program was created to provide users with movie recommendations using the nearest neighbors algorithm and collaborative filtering.\n",
          "Using a database of over 9500 movies and 600 users, the program can suggest to you which movies to watch.\n",
          "Follow the prompts to get your movie recommendations. You may type 'Stop' to quit.\n")
    
    inp = ""
    recommender = Recommender()

    while inp.lower() != "stop":
        print("\nYou may either ask for recommendations based on a movie you watched or your watch history.\n",
              "To add to your watch history you can input a .txt file or individually write out a movie name.\n",
              "[1] Movie title based recommendations\n",
              "[2] Watch history based recommendations\n",
              "[3] Add to my watch history individually\n",
              "[4] Add to my watch history via .txt file\n",
              "[5] Remove from my watch history\n",
              "Select a number to choose an option or type 'Stop' to quit.\n")
        
        inp = input("Enter number: ")
        out = ''
        
        if inp == '1':
            out = input("What movie would you like recommendations based on? This movie will NOT be added to your watch history >> ")
            strn = ''
            while strn != 'y':
                print("\n", recommender.recommend_on_movie(out), "\n")
                strn = input("Are you done viewing? (y/n) ")
                
        elif inp == '2':
            while out != 'y':
                print("\n", recommender.recommend_on_history(), "\n")
                out = input("Are you done viewing? (y/n) ")

        elif inp == '3':
            while out != 'n':
                inp = input("What movie would you like to add to your watch history? ")
                if inp not in movies['title'].unique():
                    print(inp, "not in movie database")
                else:
                    movieid = int(movies[movies['title'] == inp]['movieId'])
                    if movieid in recommender.hist:
                        print(inp, "already in your watch history\n")
                    else:
                        recommender.hist.append(movieid)
                        recommender.ishist = True
                        print(inp, "succuessfully added to your watch history\n")

                out = input("Would you like to add another movie? (y/n) ")

        elif inp == '4':
            while out != 'n':
                inp = input("Your .txt file should follow the format 'movie title' followed by new line.\n,",
                            "Enter file name here (including.txt): ")
                
                file = open(inp, "r")
                userMovies = file.readlines()

                for item in userMovies:
                    if item not in movies['title'].unique():
                        print(item, "not in movie database\n")
                    else:
                        movieid = int(movies[movies['title'] == item]['movieId'])
                        recommender.hist.append(movieid)
                        recommender.ishist = True
                        print(item, "succuessfully added to watch history\n")

                out = input("Would you like to add another .txt file? (y/n) ")
        
        elif inp == '5':
            if recommender.ishist == False:
                print('No history found')
            else:
                while out != 'n':
                    for item in recommender.hist:
                        mov = movies[movies['movieId'] == item]['title']
                        print(mov)

                    inp = input("What movie would you like to remove from your watch history? ")
                    if inp not in movies['title'].unique():
                        print(inp, "not in movie database")
                    else:
                        movieid = int(movies[movies['title'] == inp]['movieId'])
                        if movieid not in recommender.hist:
                            print(inp, "is not in yout watch history\n")
                        else:
                            recommender.hist.remove(movieid)
                            if len(recommender.hist) == 0:
                                recommender.ishist = False
                            print(inp, "succuessfully removed from your watch history\n")

                    out = input("Would you like to remove another movie? (y/n) ")
    
    print("Thanks for being here! See you next time.")




if __name__ == "__main__":
    main()
