"""

"""
from file_handling_classes import BaseDataModel, JsonRepository


# 1. Definition der reinen Datenstruktur (Super schlank!)
class ProductModel(BaseDataModel):
	_id_field = "product_key"  # Sagt dem Manager, wie die ID heißt

	def __init__(self, product_key: int, name: str, price: float):
		super().__init__()
		self.product_key = product_key
		self.name = name
		self.price = price


def main():
	# 2. Wir erstellen den Manager exklusiv für Produkte
	product_repo = JsonRepository(target_class=ProductModel, filepath="storage/products.json")

	# 3. Daten-Objekte erzeugen (reine Daten, keine Methoden für Dateien)
	apple = ProductModel(product_key=1, name="Apfel", price=0.99)
	banana = ProductModel(product_key=2, name="Banane", price=1.49)

	# 4. CRUD Operationen laufen jetzt über das Repository
	print("--- Speichern ---")
	product_repo.create(apple)
	product_repo.create(banana)

	print("--- Auslesen ---")
	all_products = product_repo.read_all()
	print(f"Aus der Datei geladen: {all_products}")

	print("--- Gezieltes Löschen über ID ---")
	product_repo.delete(identity=1)  # Löscht den Apfel direkt über die ID
	print(f"Nach Löschen: {product_repo.read_all()}")


if __name__ == "__main__":
	main()
