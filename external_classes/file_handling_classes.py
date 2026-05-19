"""

"""
import inspect
import os
from typing import List, Dict, Any, Type, TypeVar

T = TypeVar("T", bound='BaseDataModel')

class BaseDataModel:
	"""

	"""
	_id_field: str = "item_id"
	_db_path: str = os.path.join(os.getcwd(), "data_store.json")

	def to_dict(self) -> dict[str, Any]:
		"""

		:return:
		"""
		return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

	def __repr__(self) -> str:
		"""

		:return:
		"""
		class_name = self.__class__.__name__
		attributes = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
		return f"{class_name}({attributes})"

	def __eq__(self, other) -> bool:
		"""

		:param other:
		:return:
		"""
		if not isinstance(other, self.__class__):
			return NotImplemented
		return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

	def validate(self, required_fields=None) -> tuple[bool, list]:
		"""

		:param required_fields:
		:return:
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

		:param data:
		:return:
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

		:return:
		"""
		if self._id_field not in self.__dict__:
			raise ValueError(f"ID field '{self._id_field}' not found in {self.__class__.__name__} instance.")
		return self.__dict__[self._id_field]



class JsonRepository:
	"""

	"""

	def __init__(self, target_class: Type[T], filepath: str):
		self.target_class = target_class
		self.filepath = filepath

	def _load_raw_entries(self) -> List[Dict[str, Any]]:
		"""

		:return:
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

		:param data:
		:return:
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

		:param model_instance:
		:return:
		"""
		if not isinstance(model_instance, self.target_class):
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

		:return:
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

		:param identity:
		:return:
		"""
		id_field = self.target_class._id_field
		for instance in self.read_all():
			if instance._get_id_value() == identity:
				return instance
		raise KeyError(f"Instance with {id_field} '{identity}' not found.")

	def update(self, model_instance: T) -> None:
		"""

		:param model_instance:
		:return:
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

		:param identity:
		:return:
		"""
		current_data = self._load_raw_entries()
		id_field = self.target_class._id_field
		new_data = [item for item in current_data if item.get(id_field) != identity]
		if len(current_data) == len(new_data):
			raise KeyError(f"Instance with {id_field} '{identity}' not found.")
		self._save_raw_entries(new_data)