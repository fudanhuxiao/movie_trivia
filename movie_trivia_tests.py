from movie_trivia import *
import unittest,csv

class TestMovies(unittest.TestCase):
	
	movieDb = {}
	ratingDb = {}
	
	def setUp(self):
		self.movieDb = create_actors_DB('movies.txt')
		self.ratingDb = create_ratings_DB('moviescores.csv')
	
	def testselect_where_movie_is(self):
		#write test code here using self.ratingDb and self.movieDb
		actors = select_where_movie_is('tom hanks', self.movieDb)
		#make some assertion about these actors
	
	def testinsert_actor_info(self):
		insert_actor_info('zhang ziyi',['Crouching Tiger Hidden Dragon','The Road Home','Hero'],self.movieDb)
	
	def testinsert_rating(self):
		insert_rating("Crouching Tiger Hidden Dragon",("80","85"),self.ratingDb)
	
	def testdelete_movie(self):
		delete_movie("JFK",self.movieDb,self.ratingDb)
	
	def testselect_where_actor_is(self):
		movies=select_where_actor_is("Dustin Hoffman",self.movieDb)
	
	def testselect_where_rating_is(self):
		select_where_rating_is("targeted_rating", "comparison", "is_critic", self.ratingDb)
	
	def testget_co_actors(self):
		get_co_actors("Brad Pitt",self.movieDb)

	def testget_common_movie(self):
		get_common_movie("Brad Pitt","Tom Hanks",self.movieDb)

	def testcritics_darling(self):
		critics_darling(self.movieDb,self.ratingDb)

	def testaudience_darling(self):
		audience_darling(self.movieDb,self.ratingDb)

	def testgood_movies(self):
		good_movies(self.ratingDb)

	def testget_common_actors(self):
		get_common_actors("Apollo 13","Philadelphia",self.movieDb)

	def testget_bacon(self):
		get_bacon("shirley maclaine",self.movieDb)

	def testAdjustName(self):
		AdjustName("zhang ziyi")

unittest.main()
