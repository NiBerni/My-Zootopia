"""
Modul for testing and sorting thoughts
"""
from external_classes.file_handling_classes import BaseDataModel, JsonRepository


class Animal(BaseDataModel):
	"""

	"""
	_id_field = "name"

	def __init__(self,
	             name: str,
	             diet: str,
	             location: str,
	             animal_type: str
	             ):
		super().__init__()
		self.name = name
		self.diet = diet
		self.location = location
		self.type = animal_type

	def print_info(self):
		print(f"Name: {self.name}")
		print(f"Diet: {self.diet}")
		print(f"Location: {self.location}")
		print(f"Type: {self.type}")


data = JsonRepository(Animal, "animals_data.json")
data.read_all(strict=False)
