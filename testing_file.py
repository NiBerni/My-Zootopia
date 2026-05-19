"""
Modul for testing and sorting thoughts
"""
from external_classes.file_handling_classes import BaseDataModel, JsonRepository


class AnimalModel(BaseDataModel):
	"""
	Represents a model for storing information about animals.

	This class is designed to hold key details about an animal, such as its name,
	diet, geographical locations, and type. The information can be created from a
	dictionary and provides methods for printing stored animal details.

	:ivar name: The name of the animal.
	:type name: str
	:ivar diet: The dietary information of the animal (e.g., herbivore, carnivore).
	:type diet: str
	:ivar location: A list of geographical locations where the animal is found.
	:type location: list[str]
	:ivar type: The type or species classification of the animal.
	:type type: str
	"""
	_id_field = "name"

	def __init__(self,
	             name: str,
	             diet: str,
	             location: list[str],
	             animal_type: str
	             ):
		"""
		Initializes an instance of the animal class.

		The class is designed to represent various types of animals and includes
		attributes that define the name, diet, habitat locations, and the
		classification of the animal. The initialization method assigns these
		values upon creation of an instance.

		:param name: The name of the animal.
		:type name: str
		:param diet: The diet category of the animal, e.g., herbivore, carnivore,
		    omnivore, etc.
		:type diet: str
		:param location: A list of geographic locations or habitats where the
		    animal typically lives.
		:type location: list[str]
		:param animal_type: The classification or type designation of the animal.
		:type animal_type: str
		"""
		super().__init__()
		self.name = name
		self.diet = diet
		self.location = location
		self.type = animal_type

	@classmethod
	def from_dict(cls, data: dict) -> AnimalModel:
		"""
		Creates an instance of the class using a dictionary input. Extracts specific
		data from the provided dictionary to initialize the class instance.

		:param data: A dictionary containing the data to construct the object. It
		    should have a 'name' key for the animal's name, a 'locations' key
		    (optional), and a 'characteristics' key (optional) which may include
		    'diet' and 'type' information.
		:type data: dict

		:return: A class instance initialized with values extracted from the provided
		    dictionary.
		:rtype: AnimalModel
		"""
		name = data.get("name")
		location = data.get("locations", [])
		characteristics = data.get("characteristics", {})
		diet = characteristics.get("diet", "unknown")
		animal_type = characteristics.get("type", "unknown")
		return cls(name, diet, location, animal_type)


	def print_info(self):
		"""
		Provides a formatted string containing details about the object.

		The information includes the name, diet, locations (if specified), and
		type of the object. If no location is specified, a default message is
		returned indicating this.

		:return: A string containing the formatted details about the object.
		:rtype: str
		"""
		# TODO switch to returning a string instead of printing directly in final Version
		print(f"Name: {self.name} \n"
		      f"Diet: {self.diet} \n"
		      f"Location: {', '.join(self.location) if self.location else 'No location specified'} \n"
		      f"Type: {self.type}\n")


data = JsonRepository(target_class=AnimalModel, filepath="animals_data.json")
print(data.read_all(strict=False))
for animal in data.read_all(strict=False):
	animal.print_info()
