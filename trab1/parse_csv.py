'''
This script was used to parse the csv data to NT

Authors:
João Ferreira - 80041
João Magalhães - 79923
'''

import csv
from datetime import date


directorID = 0
actorID = 0

# URI
base = '<http://netflix-titles.com/'

movie_subject = base + 'movie/' #+ id
tv_series_subject = base + 'tv_series/' #+ id

type_pred = base + 'pred/type'
title_pred = base + 'pred/title'
directed_by_pred = base + 'pred/directed_by'
cast_pred = base + 'pred/cast'
country_pred = base + 'pred/country'
date_added_pred = base + 'pred/date_added'
release_year_pred = base + 'pred/release_year'
duration_pred = base + 'pred/duration'
listed_in_pred = base + 'pred/listed_in'


#dicts
directors = {} # director -> [movies, tv_series]
actors = {} #actor -> [movies, tv_series]

with open('netflix_titles.csv') as csv_file:
    with open('netflix_titles.nt', 'w') as output:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        for row in reader:
            if(row[1]=='Movie'):
                output.write(movie_subject + row[0] + '> ' + type_pred + '> '+ row[1] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                output.write(movie_subject + row[0] + '> ' + title_pred + '> ' + row[2] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                if(row[3]==""):
                    row[3] = "unknown"
                output.write(movie_subject + row[0] + '> ' + directed_by_pred + '> ' + row[3] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                #falta guardar os directores

                output.write(movie_subject + row[0] + '> ' + cast_pred + '> ' + row[4] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                #falta guardar os actores

                output.write(movie_subject + row[0] + '> ' + country_pred + '> ' + row[5] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(movie_subject + row[0] + '> ' + date_added_pred + '> ' + row[6] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(movie_subject + row[0] + '> ' + release_year_pred+ '> ' + row[7] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(movie_subject + row[0] + '> ' + duration_pred + '> ' + row[9] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(movie_subject + row[0] + '> ' + listed_in_pred+ '> ' + row[10] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

            elif(row[1]=='TV Show'):
                output.write(tv_series_subject + row[0] + '> ' + type_pred + '> ' + row[1] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                output.write(tv_series_subject + row[0] + '> ' + title_pred + '> ' + row[2] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                if(row[3]==""):
                    row[3] = "unknown"
                output.write(tv_series_subject + row[0] + '> ' + directed_by_pred + '> ' + row[3] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                #falta guardar os directores

                output.write(tv_series_subject + row[0] + '> ' + cast_pred + '> ' + row[4] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')
                #falta guardar os actores

                output.write(tv_series_subject + row[0] + '> ' + country_pred + '> ' + row[5] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(tv_series_subject + row[0] + '> ' + date_added_pred + '> ' + row[6] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(tv_series_subject + row[0] + '> ' + release_year_pred+ '> ' + row[7] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(tv_series_subject + row[0] + '> ' + duration_pred + '> ' + row[9] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

                output.write(tv_series_subject + row[0] + '> ' + listed_in_pred+ '> ' + row[10] + '"^^<http://www.w3.org/2001/XMLSchema#string> .\n')

output.close()

