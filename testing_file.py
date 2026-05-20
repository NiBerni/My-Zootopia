"""
Modul for testing and sorting thoughts
Usually in my .gitignore, but for learning purposes I want to keep it
"""
from external_classes.file_handling_classes import BaseDataModel, JsonRepository


class Animal(BaseDataModel):
	"""
	Represents a model for storing information about animals.

	This class is designed to hold key details about an animal, such as its name,
	diet, geographical locations, and type. The information can be created from a
	dictionary and provides methods for printing stored animal details.

	:ivar name: The name of the animal.
	:type name: str | None
	:ivar diet: The dietary information of the animal (e.g., herbivore, carnivore).
	:type diet: str | None
	:ivar location: A list of geographical locations where the animal is found.
	:type location: list[str] | None
	:ivar type: The type or species classification of the animal.
	:type type: str | None
	"""
	_id_field = "name"

	def __init__(self,
	             name: str,
	             diet: str | None,
	             location: list[str] | None,
	             animal_type: str | None
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
		:type diet: str | None
		:param location: A list of geographic locations or habitats where the
		    animal typically lives.
		:type location: list[str] | None
		:param animal_type: the classification or type designation of the animal.
		:type animal_type: str | None
		"""
		super().__init__()
		self.name = name
		if diet:
			self.diet = diet
		if location:
			self.location = location
		if animal_type:
			self.type = animal_type

	@classmethod
	def from_dict(cls, formated_data: dict) -> Animal:
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
		:rtype: Animal
		"""
		name = formated_data.get("name", "Unknown")
		locations_list = formated_data.get("locations", [])
		location = None
		if isinstance(locations_list, list) and len(locations_list) > 0:
			location = locations_list[0]
		characteristics = formated_data.get("characteristics", {})
		diet = characteristics.get("diet")
		animal_type = characteristics.get("type")
		return cls(name=name, diet=diet, location=location, animal_type=animal_type)

	def get_info(self):
		"""
		Provides a formatted string containing details about the animal.

		The information includes the name, diet, locations (if specified), and
		type of the animal. If no location is specified, a default message is
		returned indicating this.

		:return: A string containing the formatted details about the animal.
		:rtype: str
		"""
		# TODO switch to returning a string instead of printing directly in final Version
		info_lines = []
		info_lines.append(f"Name: {self.name}")
		if hasattr(self, "diet"):
			info_lines.append(f"Diet: {self.diet}")
		if hasattr(self, "location"):
			info_lines.append(f"Location: {self.location}")
		if hasattr(self, "type"):
			info_lines.append(f"Type: {self.type}")
		formated_info = "\n".join(info_lines) + "\n"
		return formated_info


data = JsonRepository(target_class=Animal, filepath="animals_data.json")
print(data.read_all(strict=False))
info_list = []
for animal in data.read_all(strict=False):
	print(animal.print_info())
