"""

"""
from animal_class_handling import AnimalModel as Animal
from external_classes.file_handling_classes import JsonRepository

animals_raw = JsonRepository(target_class=Animal, filepath="animals_data.json")
for animal in animals_raw.read_all(strict=False):
	print(animal.to_html_card())
