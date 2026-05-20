"""
A base module for creating data models and handling repository operations.

This module provides classes for managing data models (`BaseDataModel`)
and persisting them into a JSON-based repository (`JsonRepository`). It
includes capabilities for defining reusable data models, converting
models to and from dictionary representations, and handling data using
repository patterns in JSON format.
"""
import inspect
import os
from typing import List, Dict, Any, Type, TypeVar

T = TypeVar("T", bound='BaseDataModel')

class BaseDataModel:
	"""
	BaseDataModel serves as a foundational class for constructing data models. It provides
	essential utility methods for data manipulation, such as validation, dictionary
	conversion, and equality comparison. The class is also designed with extensibility
	in mind, allowing subclasses to inherit and expand upon its functionality.

	Its purpose is to manage the representation and validation of domain-specific
	data, enabling easy integration into broader applications.

	:ivar id_field: Name of the field that will be treated as an identifier for instances.
	:type id_field: str
	"""
	_id_field: str = "item_id"
	_db_path: str = os.path.join(os.getcwd(), "data_store.json")

	def __init__(self, **kwargs):
		"""
		Initializes an instance of a class by dynamically assigning attributes based
		on provided keyword arguments.

		This constructor checks each key-value pair in the provided ``kwargs`` argument.
		If the value is truthy, it sets an instance attribute with the corresponding
		key and value.

		:param kwargs: Dictionary of attribute names and their values. For each key that
		    has a truthy value, an instance attribute will be created with the key as
		    the attribute name and the corresponding value.
		"""
		for key, value in kwargs.items():
			if value:
				setattr(self, key, value)


	def to_dict(self) -> dict[str, Any]:
		"""
		Converts the public attributes of the current object to a dictionary representation.

		The method excludes any private, protected, or internal attributes
		starting with an underscore from the resulting dictionary.

		:return: A dictionary containing public attributes of the object and their values.
		:rtype: dict[str, Any]
		"""
		return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

	def __repr__(self) -> str:
		"""
		Provide a string representation of the object for debugging purposes.

		The ``__repr__`` method returns a string that includes the class name and
		a representation of all its attributes with their associated values. This is
		particularly useful for debugging or understanding the state of an object.

		:return: A string representing the object, formatted as
		         ClassName(attribute1=value1, attribute2=value2, ...).
		:rtype: str
		"""
		class_name = self.__class__.__name__
		attributes = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
		return f"{class_name}({attributes})"

	def __eq__(self, other) -> bool:
		"""
		Compares the current object with another object for equality. The equality is determined
		by checking if both objects are of the same class and have the same attributes and values.

		:param other: The object to compare with the current instance.
		:type other: Any
		:return: True if the objects are equal, False otherwise. If the types differ,
		         NotImplemented is returned.
		:rtype: bool
		"""
		if not isinstance(other, self.__class__):
			return NotImplemented
		return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

	def validate(self, required_fields=None) -> tuple[bool, list]:
		"""
		Validates the presence and non-emptiness of specified fields in the instance's attributes. If no fields are specified,
		all attributes of the instance are validated. Fields are considered missing if they are not found in the instance
		or if they are empty (e.g., None, an empty string, an empty list, or an empty dictionary).

		:param required_fields: An optional list of attribute names to validate, if provided. If not supplied, all attributes
		    of the instance are validated.
		:type required_fields: list or None
		:return: A tuple containing a boolean value and a list of missing fields. The boolean indicates whether all required
		    fields are present and non-empty. If validation fails, the list contains the names of missing or invalid fields.
		:rtype: tuple[bool, list]
		"""
		missing_fields = []
		fields_to_check = required_fields if required_fields else self.__dict__.keys()
		for field in fields_to_check:
			if field not in self.__dict__:
				missing_fields.append(field)
				continue
			value = self.__dict__[field]
			if value is None or value == "" or (isinstance(value, (list, dict)) and len(value) == 0):
				missing_fields.append(field)
		if missing_fields:
			return False, missing_fields
		return True, []

	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> 'BaseDataModel':
		"""
		Creates an instance of the class from a dictionary. The dictionary should contain
		keys corresponding to the class's constructor arguments. If a key-value pair
		is missing in the dictionary and the corresponding constructor argument has a
		default value, the default will be used. If a required argument is missing in
		the dictionary and has no default value, it will not be included in `init_params`.

		:param data: The dictionary containing the data to initialize
		             the class instance. Keys in the dictionary should
		             match constructor argument names.
		:type data: Dict[str, Any]
		:return: An instance of the class populated with values from the provided dictionary.
		:rtype: BaseDataModel
		"""
		signature = inspect.signature(cls.__init__)
		init_params = {}

		for name, param in signature.parameters.items():
			if name == 'self':
				continue
			if name in data:
				init_params[name] = data[name]
			elif param.default != inspect.Parameter.empty:
				init_params[name] = None
			else:
				pass
		return cls(**init_params)


	def _get_id_value(self) -> None:
		"""
		Retrieves the value associated with the ID field of the instance.

		The method accesses the internal dictionary of the instance to retrieve
		the value of the private `_id_field`. If the `_id_field` is not found in
		the instance's dictionary, a `ValueError` is raised.

		:raises ValueError: If the ID field specified by `_id_field` is not found in
		    the instance's dictionary.
		:return: The value associated with the `_id_field` in the instance's dictionary.
		"""
		if self._id_field not in self.__dict__:
			raise ValueError(f"ID field '{self._id_field}' not found in {self.__class__.__name__} instance.")
		return self.__dict__[self._id_field]



class JsonRepository:
	"""
	A repository class responsible for managing data persistence to and retrieval from a JSON file.

	This class provides a CRUD interface to handle instances of the target class, persist them to a
	JSON file, and load them back into instances of the same class. It relies on the target class
	implementing the methods `from_dict`, `to_dict`, and `_get_id_value`, and defining the field
	`_id_field` for identification.

	:ivar target_class: The class representing the type of objects this repository manages.
	:type target_class: Type[T]
	:ivar filepath: The path to the JSON file used for persistence.
	:type filepath: str
	"""

	def __init__(self, target_class: Type[T], filepath: str):
		"""
		Initializes an instance of the class with a specified target class and a filepath.

		:param target_class: The class type to be used as a target.
		:param filepath: The filepath as a string.
		"""
		self.target_class = target_class
		self.filepath = filepath

	def _load_raw_entries(self) -> List[Dict[str, Any]]:
		"""
		Loads raw entries from a JSON file located at the specified filepath.

		This method attempts to read the file containing JSON data. The JSON data is
		expected to be a list of dictionary objects. If the file does not exist, an
		empty list is returned. If the JSON data in the file is not in the expected
		format or cannot be decoded, an error message is logged, and the exception
		is re-raised.

		:return: List of dictionaries, each representing an entry in the JSON file.
		         Returns an empty list if the file does not exist.
		:rtype: List[Dict[str, Any]]

		:raises JSONDecodeError: If the provided file contains invalid JSON data
		                         that cannot be decoded.
		"""
		import json
		if not os.path.exists(self.filepath):
			return []
		try:
			with open(self.filepath, "r", encoding='utf-8') as file:
				data = json.load(file)
				return data if isinstance(data, list) else [data]
		except json.JSONDecodeError as e:
			print(f"[-] ToolKit-Log: Error loading data from {self.filepath}: {e}")
			raise e
		finally:
				file.close()

	def _save_raw_entries(self, data: List[Dict[str, Any]]) -> None:
		"""
		Saves raw entries to the specified file in JSON format.

		This method attempts to write a list of dictionaries to a file at the
		path specified by the `filepath` attribute. The data is serialized
		as a JSON array with an indentation of 4 for readability. If the
		directory structure leading to the file does not exist, this method
		will attempt to create it. Any I/O-related error during the process
		will result in an exception.

		:param data: A list of dictionaries representing the data to be
		    saved in JSON format.

		:raises IOError: If an error occurs while attempting to write data
		    to the specified file.
		"""
		import json
		try:
			dirname = os.path.dirname(self.filepath)
			if dirname:
				os.makedirs(dirname, exist_ok=True)
			with open(self.filepath, "w", encoding='utf-8') as file:
				json.dump(data, file, indent=4, ensure_ascii=False)
				print(f"[+] ToolKit-Log: Successfully saved data to {self.filepath}")
		except IOError as e:
			print(f"[-] ToolKit-Log: Error saving data to {self.filepath}: {e}")
			raise IOError(f"Error writing to file: {self.filepath}. {e}")
		finally:
			file.close()

	def create(self, model_instance: T) -> None:
		"""
		Creates a new entry in the data store with the provided model instance. If an
		entry with the same identifier already exists, a ValueError is raised.

		:param model_instance: The instance of the target class to be stored.
		:type model_instance: T
		:return: None
		:raises TypeError: If the provided model_instance is not of the expected type.
		:raises ValueError: If an entry with the same unique identifier already exists.
		"""
		if type(model_instance) is not self.target_class:
			raise TypeError(f"Expected {self.target_class.__name__}, got {type(model_instance).__name__}")
		current_data = self._load_raw_entries()
		my_id = model_instance._get_id_value()
		id_field = model_instance._id_field
		if any(item.get(id_field) == my_id for item in current_data):
			raise ValueError(f"An entry with {id_field} '{my_id}' already exists.")
		current_data.append(model_instance.to_dict())
		self._save_raw_entries(current_data)

	def read_all(self, strict: bool = True) -> list[T]:
		"""
		Reads and maps all raw entries to the target class instances. This method
		retrieves a list of raw data entries, attempts to map them into instances of
		the provided target class, and returns the successfully mapped instances.

		If the `strict` mode is enabled, any error during the mapping process will
		stop the execution and raise a `TypeError`. If `strict` is disabled, mapping
		errors will be logged as warnings, and the problematic entries will be
		skipped.

		:param strict: Flag indicating whether to enforce strict mapping behavior.
		    If `True`, failures during mapping will raise an error.
		:return: A list of successfully mapped instances of the target class.
		:rtype: list[T]
		"""
		raw_data = self._load_raw_entries()
		instances = []
		for index, item in enumerate(raw_data):
			try:
				new_instance = self.target_class.from_dict(item)
				instances.append(new_instance)
			except Exception as e:
				error_message = (
					f"Mapping Error for entry #{index + 1} for class '{self.target_class.__name__}'.\n"
					f"Data: {item} \nReason: {e}"
				)
				if strict:
					print(f"[-] ToolKit-Log: CRITICAL {error_message}")
					raise TypeError(error_message) from e
				else:
					print(f"[-] ToolKit-Log: WARNING {error_message} Skipping this entry.")
		return instances

	def read_by_id(self, identity: Any) -> T:
		"""
		Searches for an instance within a collection by its unique identity and
		retrieves it, if found. This method assumes the presence of an identifier
		field in the target class and that the `read_all` method provides access
		to all available instances. It raises a KeyError if an instance with the
		specified identity is not found.

		:param identity: The unique identifier used to search for the instance.
		:type identity: Any
		:return: The instance with the matching identity if found.
		:rtype: T
		:raises KeyError: If no instance with the specified identity is found.
		"""
		id_field = self.target_class._id_field
		for instance in self.read_all():
			if instance._get_id_value() == identity:
				return instance
		raise KeyError(f"Instance with {id_field} '{identity}' not found.")

	def update(self, model_instance: T) -> None:
		"""
		Updates an existing model instance in the stored data based on the unique identifier.

		This method retrieves the current data from storage, identifies the entry that
		matches the model instance's unique identifier, and updates that entry with the
		data from the provided model instance. If no matching entry is found, it raises
		a KeyError. After updating the entry, the modified data is saved back to storage.

		:param model_instance: The model instance to update in the stored data. The
		    instance must contain methods and attributes to retrieve its unique
		    identifier and serialized data as a dictionary.
		:type model_instance: T
		:raises KeyError: If no entry with the model instance's unique identifier exists
		    in the current storage.
		:return: None
		"""
		current_data = self._load_raw_entries()
		my_id = model_instance._get_id_value()
		id_field = model_instance._id_field
		updated = False
		for i, item in enumerate(current_data):
			if item.get(id_field) == my_id:
				current_data[i] = model_instance.to_dict()
				updated = True
				break
		if not updated:
			raise KeyError(f"Instance with {id_field} '{my_id}' not found.")
		self._save_raw_entries(current_data)

	def delete(self, identity: Any) -> None:
		"""
		Delete an instance from the stored data based on the provided identity.

		This method removes the entry matching the specified identity from the
		data storage. If no matching entry is found, a KeyError is raised.
		The identity is compared using the field defined by the target class's
		ID field.

		:param identity: The unique identifier of the instance to be deleted.
		    This value is compared against the entries in the data storage.

		:raises KeyError: If no entry matching the provided identity is found.

		:return: None
		"""
		current_data = self._load_raw_entries()
		id_field = self.target_class._id_field
		new_data = [item for item in current_data if item.get(id_field) != identity]
		if len(current_data) == len(new_data):
			raise KeyError(f"Instance with {id_field} '{identity}' not found.")
		self._save_raw_entries(new_data)