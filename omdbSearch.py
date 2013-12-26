# --------------------#
# Author: sleepyotaku #
# Spawned: 2013-09-18 #
# --------------------#


from json import loads
from urllib.request import urlopen


def omdbSearch(query):
    try:
        omdb_url = urlopen("http://www.omdbapi.com/?t=%s" % (query))
        response = omdb_url.read()
        response = response.decode()
        json_response = loads(response)

        genre = json_response['Genre']
        imdbRating = json_response['imdbRating']
        plot = json_response['Plot']
        runtime = json_response['Runtime']
        title = json_response['Title']
        year = json_response['Year']

        genre = "\xf1Genre:\xf1 %s " % genre
        imdbRating = "\xf1IMDB Rating:\xf1 %s " % imdbRating
        plot = "\xf1Plot:\xf1 %s " % plot
        runtime = "\xf1Length:\xf1 %s " % runtime
        titleYear = "\x1f\002%s (%s),\002\x1f " % (title, year)

        movie_data = titleYear + imdbRating + genre + runtime + plot

        return movie_data
    except:
        return "Sorry, couldn't find that movie."
