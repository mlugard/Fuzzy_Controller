import numpy as np
import pandas as pd
from datetime import datetime
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from FuzzyController.system import set_up_system

class MovieController:
    def __init__(self):
        self.data = pd.read_csv('Data/clean_data.csv', index_col=[0]).reset_index(drop=True)
        self.netflix_ctrl = set_up_system()
        
    def create_sim_instance(self, name):
        self.name = ctrl.ControlSystemSimulation(self.netflix_ctrl)
    
    def calculate(self, mood, physical_state):
        self.movie_set = {'Title' : [], 'Description' : [], 'Duration (minutes)' : [], 'Rotten_Scores' : [], 'Scores' : []}
        for index in range(len(self.data)):
            try:
                self.name.input['Mood'] = mood
                self.name.input['Physcial State'] = physical_state
                self.name.input['Year'] = self.data.release_year.iloc[index]
                self.name.input['Description Length'] = int(self.data.description_len.iloc[index])
                self.name.input['Movie Length'] = int(self.data.mv_dur.iloc[index])
                self.name.input['Polarity'] = int(self.data.polarity.iloc[index])
                self.name.input['Subjectivity'] = int(self.data.subjectivity.iloc[index])
                self.name.input['Reviews'] = int(self.data.rotten_score.iloc[index])
                self.name.input['Time of The Day'] = datetime.now().hour

                self.name.compute()
                self.movie_set['Title'].append(self.data.title.iloc[index])
                self.movie_set['Description'].append(self.data.description.iloc[index])
                self.movie_set['Duration (minutes)'].append(self.data.mv_dur.iloc[index])
                self.movie_set['Rotten_Scores'].append(self.data.rotten_score.iloc[index])
                self.movie_set['Scores'].append(self.name.output['Recommendation Score'])

            except Exception as e:
                pass

    def get_top_movies_by_genre(self, favorite_genre, bonus_factor=1.1, top_n=5):
        favorite_genre = favorite_genre.lower()
        filtered_movies = {}

        size = min(len(self.movie_set['Title']), len(self.movie_set['Scores']))

        for i in range(size):
            title = self.movie_set['Title'][i]
            score = self.movie_set['Scores'][i]
            genres_list = [g.strip().lower() for g in self.data[self.data['title'] == title].iloc[0]['genre'].split(',')]

            if favorite_genre in genres_list:
                score *= bonus_factor

            filtered_movies[title] = score

        top_movies = sorted(filtered_movies.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return top_movies

    def results(self):
        res = pd.DataFrame.from_dict(self.movie_set)
        first = res.sort_values(by=['Scores', 'Rotten_Scores'], ascending=[False, False])[0:5]
        return first