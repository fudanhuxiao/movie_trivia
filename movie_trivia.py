import csv,string
#############Utility Fuctions######################
def create_actors_DB(actor_file):
	'''Create a dictionary keyed on actors from a text file'''
	f = open(actor_file)
	movieInfo = {}
	for line in f:
		line = line.rstrip().lstrip()
		actorAndMovies = line.split(',')
		actor = AdjustName(actorAndMovies[0])
		movies = [AdjustName(x.lstrip().rstrip()) for x in actorAndMovies[1:]]
		movieInfo[actor] = set(movies)
	f.close()
	return movieInfo

def create_ratings_DB(ratings_file):
	'''make a dictionary from the rotten tomatoes csv file'''
	scores_dict = {}
	with open(ratings_file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for row in reader:
			movieName=AdjustName(row[0])
			scores_dict[movieName] = [row[1], row[2]]
	return scores_dict

def insert_actor_info(actor,movies,movie_Db):
	actor=AdjustName(actor)
	for i in range(len(movies)): movies[i]=AdjustName(movies[i].strip())
	'''inser/update the movie database'''
	if actor not in movie_Db.keys():
		movie_Db[actor]=set(movies)
	else:
		movie_Db[actor]=movie_Db[actor] | set(movies)

def insert_rating(movie,ratings,ratings_Db):
	'''insert/update the rating database'''
	movie=AdjustName(movie)
	ratings_Db[movie]=[ratings[0],ratings[1]]

def delete_movie(movie,movie_Db,ratings_Db):
	'''delete a movie's info in both database'''
	movie=AdjustName(movie)
	for actor in movie_Db.keys():
		if movie in movie_Db[actor]:
			movie_Db[actor]-=set([movie])
	if movie in ratings_Db.keys():
		movie=AdjustName(movie)
		ratings_Db.pop(movie)

def select_where_actor_is(actorName, movie_Db):
	actorName=AdjustName(actorName)
	'''get the movies of a given actor'''
	if actorName in movie_Db.keys():
		return(movie_Db[actorName])
	else:
		return("not present")

def select_where_movie_is(movieName, movie_Db):
	'''get the actors of a given movie'''
	movieName=AdjustName(movieName)
	actorList=[]
	for actorName in movie_Db.keys():
		if movieName in movie_Db[actorName]: actorList.append(actorName)
	return(actorList)

def select_where_rating_is(targeted_rating, comparison, is_critic, ratings_Db):
	'''get a list of movies that satisfy a given condition'''
	movieList=[]
	for movie in ratings_Db.keys():
		if is_critic=='1':
			if comparison==">":
				if float(ratings_Db[movie][0])>targeted_rating: movieList.append(movie)
			elif comparison=="=":
				if float(ratings_Db[movie][0])==targeted_rating: movieList.append(movie)
			elif comparison=="<":
				if float(ratings_Db[movie][0])<targeted_rating: movieList.append(movie)
		else:
			if comparison==">":
				if float(ratings_Db[movie][1])>targeted_rating: movieList.append(movie)
			elif comparison=="=":
				if float(ratings_Db[movie][1])==targeted_rating: movieList.append(movie)
			elif comparison=="<":
				if float(ratings_Db[movie][1])<targeted_rating: movieList.append(movie)
	return(movieList)

#############User Questions######################
def get_co_actors(actorName,moviedb):
	actorName=AdjustName(actorName)
	'''Given an actor\'s name, find all the actors with whom he/she has acted.'''
	co_actors=[]
	if actorName not in moviedb.keys(): return("not present")
	else:
		for movie in moviedb[actorName]:
			for actor in moviedb.keys():
				if actor!=actorName and movie in moviedb[actor]:
					co_actors.append(actor)
		return(co_actors)

def get_common_movie(actor1, actor2, moviedb):
	actor1=AdjustName(actor1)
	actor2=AdjustName(actor2)
	'''Find out the movies in which both actors are present.'''
	if actor1 not in moviedb.keys(): return actor1+" not present"
	if actor2 not in moviedb.keys(): return actor2+" not present"
	if actor1 in moviedb.keys() and actor2 in moviedb.keys():
		common_movie=list(moviedb[actor1] & moviedb[actor2])
		if len(common_movie)==0: return "No common movie"
		else: return(common_movie)

def critics_darling(movie_Db, ratings_Db):
	'''Get the actors whose movies have the highest average rotten tomatoes rating, as per the critics.'''
	highest_average_rotten_tomatoes=0
	highest_average_rotten_tomatoes_actors=[]
	for actor in movie_Db.keys():
		critic_ratings=[]
		for movie in movie_Db[actor]:
			if movie in ratings_Db.keys(): critic_ratings.append(float(ratings_Db[movie][0]))
		if sum(critic_ratings)/len(critic_ratings) > highest_average_rotten_tomatoes:
			highest_average_rotten_tomatoes_actors=[actor]
		elif sum(critic_ratings)/len(critic_ratings) == highest_average_rotten_tomatoes:
			highest_average_rotten_tomatoes_actors.append(actor)
	return(highest_average_rotten_tomatoes_actors)

def audience_darling(movie_Db, ratings_Db):
	'''Get the actors whose movies have the highest average rotten tomatoes rating, as per the audience.'''
	highest_average_rotten_tomatoes=0
	highest_average_rotten_tomatoes_actors=[]
	for actor in movie_Db.keys():
		critic_ratings=[]
		for movie in movie_Db[actor]:
		    if movie in ratings_Db.keys(): critic_ratings.append(float(ratings_Db[movie][0]))
		if sum(critic_ratings)/len(critic_ratings) > highest_average_rotten_tomatoes:
			highest_average_rotten_tomatoes_actors=[actor]
		elif sum(critic_ratings)/len(critic_ratings) == highest_average_rotten_tomatoes:
			highest_average_rotten_tomatoes_actors.append(actor)
	return(highest_average_rotten_tomatoes_actors)

def good_movies(ratings_Db):
	'''returns the set of movies that both critics and the audience have rated above 85 '''
	good_movies_list=[]
	for movie in ratings_Db.keys():
		if float(ratings_Db[movie][0]) >= 85 and float(ratings_Db[movie][1]) >= 85:
			good_movies_list.append(movie)
	return(set(good_movies_list))

def get_common_actors(movie1, movie2, movies_Db):
	'''Given a pair of movies, return a list of actors that acted in both.'''
	movie1=AdjustName(movie1)
	movie2=AdjustName(movie2)
	common_actors=[]
	for actor in movies_Db.keys():
		if movie1 in movies_Db[actor] and movie2 in movies_Db[actor]: common_actors.append(actor)
	if len(common_actors)==0: return("No Common actor.")
	else: return(common_actors)

def get_bacon(actorName,movie_Db):
	'''get the bacon number of a given actor'''
	actorName=AdjustName(actorName)
	if actorName not in movie_Db.keys(): return('not present')
	else:
		actors=[actorName]
		bacon=0
		while 'Kevin Bacon' not in actors:
			bacon+=1
			temp=set([])
			for actorName in actors:
				temp=temp | set(get_co_actors(actorName,movie_Db))
			actors=list(temp)
		return(bacon)


def print_intro():
	print '''##########################################\n
Welcome to use our database!\n
Press <1>: Insert/Update actor infomation into movie database.
Press <2>: insert/Update movie ratings into rating database. 
Press <3>: Delete a movie in both database.
Press <4>: Get the movie list of a given actor.
Press <5>: Get the actors of a given movie.
Press <6>: Get a list of movies satisfy a given condition.
Press <7>: Find out the top rated actor.
Press <8>: Find out the co-actors with an actor.
Press <9>: Find out the common movies of two actors.
Press <10>: Find out the good movies.
Press <11>: Find out common actors of two movies.
Press <12>: Get the bacon of a given actor
Press <q>: Quit the program.\n
##########################################\n
	'''

def AdjustName(actorName):
	'''change the actor's name for case sensitivity'''
	actorName=actorName.strip().split()
	adjustedName=['']*len(actorName)
	for i in range(len(actorName)):
		adjustedName[i]+=actorName[i][0].upper()
		for j in range(1,len(actorName[i])): adjustedName[i]+=actorName[i][j].lower()
	return(" ".join(adjustedName))

def main():
	movie_DB = create_actors_DB('movies.txt')
	ratings_DB = create_ratings_DB('moviescores.csv')
	print_intro()
	user_command=raw_input("----------------------------------------\n#>>")
	while user_command!='q':
		if user_command=='1':
			user_input_actorName=raw_input("Please input the actor name you want to insert:\t")
			movies=raw_input("Please input the movie names you want to insert(comma split):\t")
			movies=movies.strip().split(",")
			insert_actor_info(user_input_actorName,movies,movie_DB)
		elif user_command=='2':
			movie=raw_input("Please input the movie name you want to insert:\t")
			critics=raw_input("Please input the critics rating of the movie :\t")
			audience=raw_input("Please input the audience rating of the movie :\t")
			insert_rating(movie,(critics,audience),ratings_DB)
		elif user_command=='3':
			movie=raw_input("Please input the movie name you want to delete:\t")
			delete_movie(movie,movie_DB,ratings_DB)
		elif user_command=='4':
			actorName=raw_input("Please input the actor name you want to search:\t")
			print select_where_actor_is(actorName, movie_DB)
		elif user_command=='5':
			movieName=raw_input("Please input the movie name you want to search:\t")
			print select_where_movie_is(movieName, movie_DB)
		elif user_command=='6':
			targeted_rating=float(raw_input("Please input the targeted rating:\t"))
			comparison=raw_input("Please input the comparison (>,= or <)\t")
			is_critic=raw_input("whether you are interested in critics rating (0/1)\t")
			print select_where_rating_is(targeted_rating, comparison, is_critic, ratings_DB)
		elif user_command=='7':
			user_choose=raw_input("Which rating do you want to choose, critics or audience:\t")
			while user_choose not in ['critics',"audience"]:
				user_choose=raw_input("Please make sure you chosse critics or audience, input again:\t")
			if user_choose=='critics': print critics_darling(movie_DB, ratings_DB)
			else: print audience_darling(movie_DB, ratings_DB)
		elif user_command=='8':
			user_input_actorName=raw_input("Please input the actor name you want to search for:\t")
			print get_co_actors(user_input_actorName,movie_DB)
		elif user_command=='9':
			actor1Name=raw_input("Please input the first actor name:\t")
			actor2Name=raw_input("Please input the second actor name:\t")
			print get_common_movie(actor1Name, actor2Name, movie_DB)
		elif user_command=='10':
			print good_movies(ratings_DB)
		elif user_command=='11':
			movie1=raw_input("Please input the first movie name:\t")
			movie2=raw_input("Please input the second movie name:\t")
			print get_common_actors(movie1, movie2, movie_DB)
		elif user_command=='12':
			actorName=raw_input("Please input the actor name you want to search the bacon:\t")
			print get_bacon(actorName,movie_DB)
		else: print "Plseae make sure you have input right number."
		user_command=raw_input("----------------------------------------\n#>>")
	

if __name__ == '__main__':
	main()

