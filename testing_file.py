"""
Modul for testing and sorting thoughts
"""
from external_classes.file_handling_classes import BaseDataModel, JsonRepository


class AnimalModel(BaseDataModel):
	"""

	"""
	_id_field = "name"

	def __init__(self,
	             name: str,
	             diet: str,
	             location: list[str],
	             animal_type: str
	             ):
		super().__init__()
		self.name = name
		self.diet = diet
		self.location = location
		self.type = animal_type

	@classmethod
	def from_dict(cls, data: dict) -> AnimalModel:
		"""
		:param data:
		:return:
		"""
		name = data.get("name")
		location = data.get("locations", [])
		characteristics = data.get("characteristics", {})
		diet = characteristics.get("diet", "unknown")
		animal_type = characteristics.get("type", "unknown")
		return cls(name, diet, location, animal_type)


	def print_info(self):

		print(f"Name: {self.name}")
		print(f"Diet: {self.diet}")
		print(f"Location: {', '.join(self.location) if self.location else 'No location specified'}")
		print(f"Type: {self.type}\n")


data = JsonRepository(AnimalModel, "animals_data.json")
print(data.read_all(strict=False))
for animal in data.read_all(strict=False):
	animal.print_info()
