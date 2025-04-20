import csv
from db import Model, engine, Session
from models import Product, Manufacturer


def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open("files/products.csv") as f:
                reader = csv.DictReader(f)
                all_manufacturers = {}

                for row in reader: # type: dict
                    row["year"] = int(row["year"])

                    manufacturer_name: str = row.pop("manufacturer")
                    product: Product = Product(**row)
                    if manufacturer_name not in all_manufacturers:
                        manufacturer: Manufacturer = Manufacturer(name=manufacturer_name)
                        session.add(manufacturer)
                        all_manufacturers[manufacturer_name] = manufacturer
                    all_manufacturers[manufacturer_name].products.append(product)


if __name__ == "__main__":
    main()