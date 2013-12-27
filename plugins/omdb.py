# --------------------#
# Author: sleepyotaku #
# Spawned: 2013-09-18 #
# --------------------#


from json import loads
from urllib.request import urlopen
import send


def omdbSearch(query):
    try:
        query = query.replace(' ', '+')
        print(query)
        omdb_url = urlopen("http://www.omdbapi.com/?t=%s" % (query))
        response = omdb_url.read()
        response = response.decode('utf-8')
        json_response = loads(response)

        genre = json_response['Genre']
        imdbRating = json_response['imdbRating']
        plot = json_response['Plot']
        runtime = json_response['Runtime']
        title = json_response['Title']
        year = json_response['Year']

        genre = "\x1fGenre:\x1f %s " % genre
        imdbRating = "\x1fIMDB Rating:\x1f %s " % imdbRating
        plot = "\x1fPlot:\x1f %s " % plot
        runtime = "\x1fLength:\x1f %s " % runtime
        titleYear = "\x1f\002%s (%s),\002\x1f " % (title, year)

        movie_data = titleYear + imdbRating + genre + runtime + plot

        return movie_data
    except KeyError:
#        omdb_url = urlopen("http://www.omdbapi.com/?s=%s" % (query))
#        response = omdb_url.read()
#        response = response.decode('utf-8')
#        json_response = loads(response)
#        print(json_response)

        return "Sorry, couldn't find that movie."
    except: 
        print("ERROR LOL")
        for i in sys.exc_info(): print(i)

def imdb(user, host, channel, query):
    print(query)
    r = omdbSearch(query)
    print(r)
#    send.msg(channel, r)
    return "PRIVMSG %s %s\r\n" % (channel, r)
