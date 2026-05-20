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

	@staticmethod
	def _format_text(text: str) -> str:
		"""
		Formats a given text string by capitalizing the first character, if it is non-empty.

		If the provided text is a valid string and contains at least one character, the method
		returns the string with the first character converted to uppercase, leaving the rest
		of the string unchanged. If the input is not a valid string or is empty, the method
		returns the text as-is.

		:param text:
		    The input text string to be formatted.
		:type text: str
		:return:
		    A new string where the first character is capitalized if the input text is a non-empty
		    string. Otherwise, the original text is returned.
		:rtype: str
		"""
		if isinstance(text, str) and len(text) > 0:
			return text[0].upper() + text[1:]
		return text

	@classmethod
	def from_dict(cls, formated_data: dict) -> AnimalModel:
		"""
		Creates an AnimalModel instance from a dictionary input format.

		This class method is responsible for translating a dictionary containing
		animal-related information into an instance of the AnimalModel class.
		It parses specific keys to extract attributes such as name, location,
		diet, and type of the animal, and applies formatting to ensure consistency.

		:param formated_data: The dictionary containing information about an
		    animal. Expected keys include 'name', 'locations', and
		    'characteristics'.
		:type formated_data: dict

		:return: An instance of the AnimalModel class populated with data
		    extracted and formatted from the input dictionary.
		:rtype: AnimalModel
		"""
		name = formated_data.get("name", "Unknown")
		name = cls._format_text(name)
		locations_list = formated_data.get("locations", [])
		location = None
		if isinstance(locations_list, list) and len(locations_list) > 0:
			location = cls._format_text(locations_list[0])
		characteristics = formated_data.get("characteristics", {})
		diet = cls._format_text(characteristics.get("diet"))
		animal_type = cls._format_text(characteristics.get("type"))
		skin_type = cls._format_text(characteristics.get("skin_type"))
		return cls(name=name, diet=diet, location=location, animal_type=animal_type, skin_type=skin_type)

	def _get_availaible_attributes(self) -> dict:
		"""
		Retrieves a dictionary of attributes based on a display mapping, containing
		attribute values and corresponding labels. Only attributes existing in the
		object are considered.

		:return: Dictionary mapping labels to attribute values for attributes available
		         in the object.
		:rtype: dict
		"""
		return {
			label: getattr(self, attribute)
			for attribute, label in self._display_mapping.items()
			if hasattr(self, attribute)
		}


	def get_info(self) -> str:
		"""
		Compiles and returns a string that contains detailed information about the object's public
		attributes in a readable format. This can include the object's name and other available
		attributes parsed from a dictionary.

		All accessible public attributes are gathered and formatted as key-value pairs, where
		each pair is represented as a line in the resulting string. Attributes and values are
		fetched from a source that the method retrieves internally.

		:return: A string containing formatted information about the object's name and other publicly
		         available attributes.
		:rtype: str
		"""
		info_lines = [f"Name: {self.name}"]
		for attribute, value in self._get_availaible_attributes().items():
			info_lines.append(f"{attribute}: {value}")
		return "\n".join(info_lines) + "\n"

	def to_html_card(self) -> str:
		"""
		Converts the current object's data into an HTML card representation.

		This method generates a list item (`<li>`) styled as a card, containing the name
		of the object as a heading and available attributes with their corresponding
		values as paragraphs.

		:raise AttributeError: if an invalid attribute is accessed or if an issue occurs
		    while retrieving object attributes.
		:return: String containing the HTML representation of the object's data as a
		    list item styled as a card.
		:rtype: str
		"""
		html_lines = [
			"<li class='cards__item'>",
			f" <div class='cards__title'>{self.name}</div>",
			f" <div class='cards__text'>"
		]
		for attribute, value in self._get_availaible_attributes().items():
			html_lines.append(f"<p><strong>{attribute.capitalize()}:</strong> {value}</p>")
		html_lines.extend([
			"   </div>",
			"</li>"
		])
		return "\n".join(html_lines)
