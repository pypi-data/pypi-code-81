import requests
import csv


def get_api_key():
	"""
	Function reading api key
	from key.txt
	"""
	with open('key.txt', 'r') as file:
		api_key = file.readline()

	return api_key


def parse_value(value):
	"""
	function parsing given
	str to int
	"""
	value = value.strip()

	if value == 'N/A':
		return 0

	value = value.replace('$', '')
	value = value.replace(',', '')

	return int(value)


def get_movies_from_api(movies):
	"""
	request every movie
	in the given array
	"""
	url_base = 'http://www.omdbapi.com/'
	arr = []
	api_key = get_api_key()

	for movie in movies:
		params = "+".join(movie.split())
		full_url = (
			url_base +
			'?apikey=' +
			api_key +
			'&t=' +
			params
		)
		response = requests.get(full_url)

		if response.status_code == 200 and response.json()['Response'] == 'True':
			arr.append(response.json())

	return arr


def add_movies_to_csv_file(movies):
	"""
	function adding given
	movies to the CSV file
	"""
	try:
		f = open('movies.csv')
		f.close()
		with open('movies.csv', 'a') as file:
			for movie in movies:
				if not 'imdbRating' in movie:
					movie['imdbRating'] = 'N/A'

				if not 'BoxOffice' in movie:
					movie['BoxOffice'] = 'N/A'

				file.write(f"\n{movie['Title']};{movie['imdbRating']};{movie['BoxOffice']}")

	except OSError:
		with open('movies.csv', 'w') as file:
			file.write('Title;imdbRating;BoxOffice')

			for movie in movies:
				if not 'imdbRating' in movie:
					movie['imdbRating'] = 'N/A'

				if not 'BoxOffice' in movie:
					movie['BoxOffice'] = 'N/A'

				file.write(f"\n{movie['Title']};{movie['imdbRating']};{movie['BoxOffice']}")


def sort_movies_by_imdb():
	"""
	function sorting all
	movies by IMDB rating
	"""
	try:
		with open('movies.csv', 'r') as file:
			movies = [x.split(';') for x in list(file)]
			del movies[0]
			sorter = lambda x: (x[1], x[0], x[2])
			movies = sorted(movies, key=sorter, reverse=True)

		return movies
			
	except OSError:
		return False


def titles():
	"""
	function returning
	array of all titles
	"""
	try:
		with open('movies.csv', 'r') as file:
			movies = [x.split(';') for x in list(file)]
			del movies[0]
			arr_of_titles = []

			for movie in movies:
				arr_of_titles.append(movie[0])

		return arr_of_titles

	except OSError:
		return False


def most_profitable():
	"""
	function returning most
	profitable movie
	"""
	try:
		with open('movies.csv', 'r') as file:
			movies = [x.split(';') for x in list(file)]
			del movies[0]
			max_value = 0
			movie_with_max = None

			for movie in movies:
				value = parse_value(movie[2])

				if value > max_value:
					max_value = value
					movie_with_max = movie

			return movie_with_max

	except OSError:
		return False


def avg_rating():
	"""
	function returning
	average IMDB rating
	"""
	try:
		with open('movies.csv', 'r') as file:
			movies = [x.split(';') for x in list(file)]
			del movies[0]
			sum_of_imdb = 0

			for movie in movies:
				sum_of_imdb += float(movie[1])

		return round(sum_of_imdb / len(movies), 2)

	except OSError:
		return False