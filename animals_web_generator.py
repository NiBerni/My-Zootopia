"""

"""
from animal_class_handling import AnimalModel as Animal
from external_classes.file_handling_classes import JsonRepository

animals_raw = JsonRepository(target_class=Animal, filepath="animals_data.json")


# for animal in animals_raw.read_all(strict=False):
# 	print(animal.to_html_card())

def read_html_template(filepath: str) -> str:
	try:
		with open(filepath, "r", encoding="utf-8") as file:
			return file.read()
	except FileNotFoundError:
		print(f"Error: The file '{filepath}' was not found.")
		return ""
	except IOError as e:
		print(f"Error reading file '{filepath}': {e}")
		return ""
	finally:
		file.close()


def generate_animal_page(animals: list[Animal], template_path: str, output_path: str) -> None:
	html_template = read_html_template(template_path)
	if not html_template:
		return
	html_cards_list = []
	for animal in animals:
		html_cards_list.append(animal.to_html_card())
	animals_info_string = "\n".join(html_cards_list)
	final_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_info_string)
	with open(output_path, "w", encoding="utf-8") as file:
		file.write(final_html)
	print(f"Animal page generated successfully at '{output_path}'.")


# TODO change output_path to a more specific path if needed, and ensure the template path is correct.
generate_animal_page(animals_raw.read_all(strict=False), "animals_template.html", "animal_page.html")
