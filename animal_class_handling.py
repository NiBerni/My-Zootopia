"""
Module for managing animal-related data, including information such as name, diet,
location, and type.

This module defines the AnimalModel class, which allows for the creation, manipulation,
and representation of animal instances with optional attributes.
"""
from external_classes.file_handling_classes import BaseDataModel


class AnimalModel(BaseDataModel):
	"""
	Represents an animal with associated details such as name, diet, location,
	and type. The class provides functionality to initialize an animal instance
	with specified attributes, create an instance from a dictionary, and retrieve
	a formatted string containing animal details.

	This class is primarily designed for managing animal-related data with flexibility
	to handle optional or missing attributes.

	:ivar name: The name of the animal.
	:type name: str
	:ivar diet: The dietary preference of the animal, if specified.
	:type diet: str | None
	:ivar location: A list of habitats where the animal is typically found, if
	    specified.
	:type location: list[str] | None
	:ivar type: The classification or type of the animal, if specified.
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
		Initializes an instance of the class with the given attributes, representing
		an animal with a name, dietary preferences, habitats, and type.

		:param name: The name of the animal.
		:type name: str
		:param diet: The dietary preference of the animal, or None if unspecified.
		:type diet: str | None
		:param location: A list of habitats where the animal is typically found, or
		    None if unspecified.
		:type location: list[str] | None
		:param animal_type: The classification or type of the animal, or None
		    if unspecified.
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
	def from_dict(cls, formated_data: dict) -> AnimalModel:
		"""
		Create an instance of the AnimalModel class from a dictionary representation.

		This method parses a dictionary to extract relevant information about an animal,
		such as its name, location, diet, and type, and returns an instance of the class
		initialized with the extracted values. If certain fields are missing in the input
		dictionary, default values will be used.

		:param formated_data: A dictionary containing information about an animal. Expected
		                      keys include 'name' (str), 'locations' (list), and
		                      'characteristics' (dict). 'characteristics' dictionary may
		                      further contain 'diet' and 'type' keys.
		:return: An instance of the AnimalModel class initialized with the extracted data.
		:rtype: AnimalModel
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
