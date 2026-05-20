"""

"""
from animal_class_handling import AnimalModel as Animal
from external_classes.file_handling_classes import JsonRepository




def read_html_template(filepath: str) -> str:
	"""
	Reads and returns the content of an HTML file as a string. This function attempts to open the file
	specified by the `filepath` parameter, read its content, and return it. In case of any issues such as
	missing file or input/output errors, error messages are logged, and an empty string is returned.

	:param filepath: Path to the HTML file to be read.
	:type filepath: str
	:return: The content of the HTML file as a string. If the file cannot be found or read, an empty
	    string is returned instead.
	:rtype: str
	"""
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


def filter_animals_by_attribute(animals: list[Animal], attribute_name: str, search_term: str) -> list[Animal]:
	"""
	Filters a list of Animal objects based on a specific attribute and search term.

	This function iterates through a list of Animal objects and filters them based on the
	attribute specified by the `attribute_name` parameter. The function compares the given
	`search_term` against the attribute's value (converted to lowercase for case-insensitive
	search) and includes matching Animal objects in the filtered results.

	:param animals:
	    A list of Animal objects to filter.

	:param attribute_name:
	    A string representing the name of the attribute to filter on. The attribute must exist
	    in the Animal objects. If the attribute is not present, the function will assume a
	    default empty string for comparison.

	:param search_term:
	    A string used for filtering. The search is case-insensitive and checks for the
	    presence of the `search_term` within the attribute's value.

	:return:
	    A list of Animal objects that match the search criteria based on the specified
	    attribute and `search_term`.
	"""
	filtered_animals = []
	search_term = search_term.lower()
	for animal in animals:
		animal_value = getattr(animal, attribute_name, "")
		animal_value_str = str(animal_value.lower())
		if search_term in animal_value_str:
			filtered_animals.append(animal)
	return filtered_animals


def get_unique_attribute_values(animals: list[Animal], attribute_name: str) -> str:
	"""
	Retrieve unique values of a specified attribute from a list of Animal objects.

	This function iterates through a list of Animal objects, collects unique
	values of a specified attribute, and returns a comma-separated string of
	these values. If the attribute is not found or the value is empty, it is
	skipped.

	:param animals: List of Animal objects.
	:param attribute_name: The name of the attribute whose unique values are
	    to be retrieved.
	:return: A comma-separated string containing unique values of the specified
	    attribute.
	:rtype: str
	"""
	unique_values = set()
	for animal in animals:
		value = getattr(animal, attribute_name, "")
		if value:
			unique_values.add(value)
	return ", ".join(sorted(unique_values))

def generate_animal_page(animals: list[Animal], template_path: str, output_path: str) -> None:
	"""
	Generates an HTML page for a list of animals using a specified HTML template.

	This function reads an HTML template from a given file, processes a list of
	Animal objects to generate their corresponding HTML representations, and writes
	the final output to a specified file path. If no animals are provided, a default
	message with a 404-style response is included in the output.

	:param animals: List of Animal objects to be represented in the generated HTML file.
	:param template_path: Path to the HTML template file to be read for generating the page.
	:param output_path: Path where the generated HTML file will be written.
	:return: None
	"""
	html_template = read_html_template(template_path)
	if not html_template:
		return

	html_cards_list = [animal.to_html_card() for animal in animals]
	animals_info_string = "\n".join(html_cards_list)
	if not animals_info_string:
		animals_info_string = """
		<li class="cards__item">
		    <div class="card__title"><strong>404 - No animals found</strong></div>
		    <div class="card__text">
		        <p>Sorry, we couldn't find any animals matching your criteria.</p>
		        <p>Redirecting your "Unic" request ... </p>
		    </div>
		</li>
		
		<script>
		setTimeout(function() {
		window.location.href = "https://en.wikipedia.org/wiki/Unicorn";
		}, 3000);
		</script>
		"""
		
	final_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animals_info_string)

	with open(output_path, "w", encoding="utf-8") as file:
		file.write(final_html)

	print(f"Animal page generated successfully at '{output_path}'.")


def main():
	""""""
	animals_raw = JsonRepository(target_class=Animal, filepath="animals_data.json")
	print("\n----- Welcome to the Animals Web Generator! -----\n")

	print(" --Animals successfully loaded from JSON file.-- \n")
	user_filter_choice = input(
		"Do you want to filter animals by a specific attribute? (y/n)[Default: n]: ").strip().lower()
	if user_filter_choice not in ["y", "yes"]:
		print(" -No filtering will be applied.- \n -Generating page with all animals...- \n")
		# TODO change output_path to a more specific path if needed, and ensure the template path is correct.
		generate_animal_page(animals_raw.read_all(strict=False), "animals_template.html", "animal_page.html")
		return

	allowed_attributes = ["diet", "location", "animal_type", "skin_type"]
	print("\n --Which attribute do you want to filter by?-- \n")
	print(f" --Your possibilities are:-- \n - {"\n - ".join(allowed_attributes)}\n")
	while True:
		user_filter_attribute = input("Enter the attribute name [Hit Enter for Default[skin_type]: \n").strip().lower()
		if not user_filter_attribute:
			user_filter_attribute = "skin_type"
			print(f" -Defaulting to '{user_filter_attribute}' attribute.- \n")
			break
		if user_filter_attribute in allowed_attributes:
			break
		else:
			print(f" -'{user_filter_attribute}' is not a valid attribute.-- \n")
			print(f" -Please chose from:-- {'\n - '.join(allowed_attributes)}\n")

	available_options = get_unique_attribute_values(animals_raw.read_all(strict=False), user_filter_attribute)
	print(f" --Your available options for '{user_filter_attribute}' are:-- \n - {available_options}\n")

	while True:
		search_term = input("Enter the search term from the options above: \n").strip()
		if search_term:
			break
		else:
			print(f" -You have to enter something to proceed- \n")
			print(f" -Please choose from:-- \n - {available_options}\n")

	filtered_animals = filter_animals_by_attribute(animals_raw.read_all(strict=False), user_filter_attribute,
	                                               search_term)
	if not filtered_animals:
		print(" -No animals found matching your criteria.-- \n")
	else:
		print(f" -Generating page of animals filtered by {user_filter_attribute}...- \n")
	generate_animal_page(filtered_animals, "animals_template.html", "animal_page.html")


if __name__ == "__main__":
	main()
