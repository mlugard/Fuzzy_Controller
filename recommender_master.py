from FuzzyController.fuzzy_controller import MovieController
import time
import pandas as pd

if __name__ == '__main__':
    starttime = time.time()

    print('Welcome to Fuzzy Movie Recommender System\n')
    name = input('What is your name? ')
    print(f'Welcome {name}.\n')

    user_mood = int(input('How would you rate your mood now from 1 (Very Upset) to  10 (Very Happy)? '))
    print('Thank You!\n')

    user_state = int(input('How would you rate your physical state now from 1 (Exhausted) to 10 (Very Lively)? '))
    print('')

    favorite_genre = input("What is your favorite movie genre? (Action, Drama, Comedy, Horror, Sci-Fi, Documentary): ").lower()
    print('Thank You! I am generating a few recommendations for you.\n')

    fuzzy = MovieController()
    fuzzy.create_sim_instance(name)
    fuzzy.calculate(user_mood, user_state)

    top_movies = fuzzy.get_top_movies_by_genre(favorite_genre)

    print("Top 5 movie recommendations:")
    for title, score in top_movies:
        print(f"{title} - Score: {score:.2f}")

    endtime = time.time()
    print(f"\nProcess completed in {endtime - starttime:.2f} seconds.")