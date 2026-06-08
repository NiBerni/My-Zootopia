"""
This module defines data models for movies, directors, and genres,
inheriting from `BaseDataModel` to facilitate data handling and
potential integration with database operations.

It includes classes:
- `Director`: Represents a movie director.
- `Genre`: Represents a movie genre.
- `MoviesClass`: Represents a movie with its associated director, genre, and rating.

These classes are designed to be easily initialized from dictionary data,
mimicking database query results, and provide methods for conversion
to and from dictionary representations, including handling of nested objects.
"""

from typing import Any, Dict, Optional

from file_handling_classes import BaseDataModel


class Director(BaseDataModel):
	"""
	Represents a movie director data model.

	This class extends `BaseDataModel` to provide a structured way to
	handle director information, including a unique identifier and name.
	It is designed to be easily instantiated from dictionary data, typical
	of database records.

	:ivar director_id: A unique identifier for the director.
	:type director_id: Optional[str]
	:ivar name: The full name of the director.
	:type name: Optional[str]
	"""
	_id_field: str = "director_id"

	def __init__(self, director_id: Optional[str] = None, name: Optional[str] = None, **kwargs: Any) -> None:
		"""
		Initializes an instance of the Director class.

		The constructor dynamically assigns attributes based on provided keyword arguments,
		with specific handling for `director_id` and `name`. If values for these
		parameters are provided, they are set as instance attributes.

		:param director_id: An optional unique identifier for the director.
							If provided, it will be set as `self.director_id`.
		:type director_id: Optional[str]
		:param name: An optional name of the director.
					 If provided, it will be set as `self.name`.
		:type name: Optional[str]
		:param kwargs: Arbitrary keyword arguments that are passed to the
					   `BaseDataModel` constructor for dynamic attribute assignment.
		:type kwargs: Any
		"""
		super().__init__(**kwargs)
		if director_id:
			self.director_id = director_id
		if name:
			self.name = name


class Genre(BaseDataModel):
	"""
	Represents a movie genre data model.

	This class extends `BaseDataModel` to provide a structured way to
	handle genre information, including a unique identifier and name.
	It is designed for easy instantiation from dictionary data, reflecting
	database entries for genres.

	:ivar genre_id: A unique identifier for the genre.
	:type genre_id: Optional[str]
	:ivar name: The name of the genre (e.g., "Sci-Fi", "Comedy").
	:type name: Optional[str]
	"""
	_id_field: str = "genre_id"

	def __init__(self, genre_id: Optional[str] = None, name: Optional[str] = None, **kwargs: Any) -> None:
		"""
		Initializes an instance of the Genre class.

		The constructor dynamically assigns attributes based on provided keyword arguments,
		with specific handling for `genre_id` and `name`. If values for these
		parameters are provided, they are set as instance attributes.

		:param genre_id: An optional unique identifier for the genre.
						 If provided, it will be set as `self.genre_id`.
		:type genre_id: Optional[str]
		:param name: An optional name of the genre.
					 If provided, it will be set as `self.name`.
		:type name: Optional[str]
		:param kwargs: Arbitrary keyword arguments that are passed to the
					   `BaseDataModel` constructor for dynamic attribute assignment.
		:type kwargs: Any
		"""
		super().__init__(**kwargs)
		if genre_id:
			self.genre_id = genre_id
		if name:
			self.name = name


class MoviesClass(BaseDataModel):
	"""
	Represents a movie data model, including its title, director, genre, and user rating.

	This class extends `BaseDataModel` and encapsulates all relevant information
	for a movie. It handles nested `Director` and `Genre` objects,
	allowing for a rich and structured representation of movie data.
	The `rating` attribute is specifically typed as a float and is intended
	to be updated via user input.

	:ivar movie_id: A unique identifier for the movie.
	:type movie_id: Optional[str]
	:ivar title: The title of the movie.
	:type title: Optional[str]
	:ivar director: An instance of the `Director` class associated with the movie.
	:type director: Optional[Director]
	:ivar genre: An instance of the `Genre` class categorizing the movie.
	:type genre: Optional[Genre]
	:ivar rating: The user rating for the movie, expected as a float.
	:type rating: Optional[float]
	"""
	_id_field: str = "movie_id"

	def __init__(self, movie_id: Optional[str] = None, title: Optional[str] = None,
	             director: Optional[Director] = None, genre: Optional[Genre] = None,
	             rating: Optional[float] = None, **kwargs: Any) -> None:
		"""
		Initializes an instance of the MoviesClass.

		This constructor handles the initialization of movie-specific attributes
		such as `movie_id`, `title`, `director`, `genre`, and `rating`.
		It also ensures that `rating` is stored as a float. Nested objects
		(`Director` and `Genre`) are expected to be provided as instances of their
		respective classes.

		:param movie_id: An optional unique identifier for the movie.
						 If provided, it will be set as `self.movie_id`.
		:type movie_id: Optional[str]
		:param title: An optional title of the movie.
					  If provided, it will be set as `self.title`.
		:type title: Optional[str]
		:param director: An optional instance of the `Director` class representing
						 the movie's director. If provided, it will be set as `self.director`.
		:type director: Optional[Director]
		:param genre: An optional instance of the `Genre` class representing
					  the movie's genre. If provided, it will be set as `self.genre`.
		:type genre: Optional[Genre]
		:param rating: An optional user rating for the movie. If provided, it will be
					   converted to a float and set as `self.rating`.
		:type rating: Optional[float]
		:param kwargs: Arbitrary keyword arguments that are passed to the
					   `BaseDataModel` constructor for dynamic attribute assignment.
		:type kwargs: Any
		"""
		super().__init__(**kwargs)
		if movie_id:
			self.movie_id = movie_id
		if title:
			self.title = title
		if director:
			self.director = director
		if genre:
			self.genre = genre
		if rating is not None:
			self.rating = float(rating)

	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> 'MoviesClass':
		"""
		Creates a `MoviesClass` instance from a dictionary.

		This class method is responsible for reconstructing a `MoviesClass` object
		from a dictionary, typically representing a row from a database.
		It specifically handles the deserialization of nested `director` and `genre`
		data by recursively calling their `from_dict` methods to ensure they are
		correctly instantiated as `Director` and `Genre` objects.

		:param data: A dictionary containing the movie's attributes, including
					 potentially nested dictionaries for 'director' and 'genre'.
		:type data: Dict[str, Any]
		:return: A new instance of `MoviesClass` populated with the provided data.
		:rtype: MoviesClass
		"""
		director_data = data.get('director')
		if director_data and isinstance(director_data, dict):
			data['director'] = Director.from_dict(director_data)

		genre_data = data.get('genre')
		if genre_data and isinstance(genre_data, dict):
			data['genre'] = Genre.from_dict(genre_data)

		return super().from_dict(data)

	def to_dict(self) -> Dict[str, Any]:
		"""
		Converts the `MoviesClass` instance to a dictionary representation.

		This method serializes the `MoviesClass` object into a dictionary,
		which can be useful for storage or transmission (e.g., to a database or API).
		It specifically handles the serialization of nested `director` and `genre`
		objects by converting them into their dictionary representations using their
		`to_dict` methods.

		:return: A dictionary containing all public attributes of the movie,
				 with nested `Director` and `Genre` instances also converted to dictionaries.
		:rtype: Dict[str, Any]
		"""
		data = super().to_dict()
		if 'director' in data and isinstance(data['director'], Director):
			data['director'] = data['director'].to_dict()
		if 'genre' in data and isinstance(data['genre'], Genre):
			data['genre'] = data['genre'].to_dict()
		return data


if __name__ == "__main__":
	# --- Example Usage ---
	# This section demonstrates how to create and manipulate movie objects
	# using the defined data models.

	# 1. Simulate data retrieved from a SQL database
	#    The 'director' and 'genre' keys contain nested dictionaries.
	sql_data_row = {
			"movie_id": "MOV001",
			"title": "The Great Movie",
			"director": {"director_id": "DIR001", "name": "Jane Doe"},
			"genre": {"genre_id": "GEN001", "name": "Sci-Fi"},
			"rating": 8.5
	}

	print("--- Initializing Movie from Dictionary ---")
	# Initialize a MoviesClass instance using the from_dict class method.
	movie = MoviesClass.from_dict(sql_data_row)
	print(f"Initialized Movie: {movie}")
	print(f"Movie ID: {movie.movie_id}")
	print(f"Movie Title: {movie.title}")
	print(f"Director: {movie.director.name} (ID: {movie.director.director_id})")
	print(f"Genre: {movie.genre.name} (ID: {movie.genre.genre_id})")
	print(f"Rating: {movie.rating}")

	# 2. Get user input for the rating and update the movie object
	print("\n--- Updating Movie Rating via User Input ---")
	try:
		user_rating_input = input("Enter movie rating (e.g., 7.2): ")
		user_rating = float(user_rating_input)
		movie.rating = user_rating
		print(f"Updated movie rating: {movie.rating}")
	except ValueError:
		print("Invalid rating. Please enter a valid number.")

	# 3. Convert the updated movie object back to a dictionary
	print("\n--- Converting Movie Instance to Dictionary ---")
	movie_dict = movie.to_dict()
	print(f"Movie as Dictionary: {movie_dict}")
	print(f"Type of director in dict: {type(movie_dict['director'])}")
	print(f"Type of genre in dict: {type(movie_dict['genre'])}")

	# 4. Create a new movie with direct object instantiation for nested fields
	print("\n--- Creating another Movie with direct object instantiation ---")
	new_director = Director(director_id="DIR002", name="John Smith")
	new_genre = Genre(genre_id="GEN002", name="Fantasy")
	another_movie = MoviesClass(movie_id="MOV002", title="Fantasy Quest",
	                            director=new_director, genre=new_genre,
	                            rating=9.1)
	print(f"Another Movie: {another_movie}")
	print(f"Director type: {type(another_movie.director)}")
	print(f"Genre type: {type(another_movie.genre)}")
