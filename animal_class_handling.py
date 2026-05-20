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

	_display_mapping = {
		"diet": "Diet: ",
		"location": "Location: ",
		"animal_type": "Type: "
		               ""
	}

	def __init__(self,
	             name: str,
	             **kwargs
	             ):
		"""
		Initializes an instance of the class with a specified name and additional keyword arguments.

		:param name: Name of the instance.
		:type name: str
		:param kwargs: Additional keyword arguments to be passed to the superclass initializer.
		"""

		self.name = name
		super().__init__(**kwargs)


	@classmethod
	def from_dict(cls, formated_data: dict) -> AnimalModel:
		"""
		Creates an instance of the AnimalModel class from a dictionary by extracting and
		mapping relevant fields.

		:param formated_data: A dictionary containing data to construct the AnimalModel object.
		                      Expected fields include:
		                      - "name" (optional): A string representing the name of the animal.
		                                          Defaults to "Unknown" if not provided.
		                      - "locations" (optional): A list where the first element, if present,
		                                                represents the primary location of the animal.
		                      - "characteristics" (optional): A dictionary containing attributes such as:
		                                                    - "diet": The dietary habit of the animal.
		                                                    - "type": The type/category of the animal.
		:type formated_data: dict
		:return: An instance of the AnimalModel class initialized with the extracted attributes.
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

	def _get_availaible_attributes(self) -> dict:
		""""""
		return {
			label: getattr(self, attribute)
			for attribute, label in self._display_mapping.items()
			if hasattr(self, attribute)
		}


	def get_info(self) -> str:
		""""""
		info_lines = [f"Name: {self.name}"]
		for attribute, value in self._get_availaible_attributes().items():
			info_lines.append(f"{attribute}: {value}")
		return "\n".join(info_lines) + "\n"

	def to_html_card(self) -> str:
		""""""
		html_lines = [
			"<li class='card'>",
			f"<h2>{self.name}</h2>",
		]
		for attribute, value in self._get_availaible_attributes().items():
			html_lines.append(f"<p><strong>{attribute.capitalize()}:</strong> {value}</p>")
		html_lines.append("</li>")
		return "\n".join(html_lines)
