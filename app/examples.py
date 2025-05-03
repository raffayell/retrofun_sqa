from pprint import pprint

from sqlalchemy import select, or_, func, not_
from db import Session
from models import Product, Manufacturer

#Chapter 2 Database tables
class Chapter2:

    @staticmethod
    def database_tables_1():
        """
        The first three products in alphabetical order built in the year 1983
        """
        with Session() as session:
            with session.begin():
                q = (select(Product)
                        .where(Product.year == 1983)
                        .order_by(Product.name)
                        .limit(3)
                    )
                res = session.scalars(q).all()
                print(res)

    @staticmethod
    def database_tables_2():
        """
        Products that use the "Z80" CPU or any of its clones. Assume that all
        products based on this CPU have the word "Z80" in the cpu column
        """
        with Session() as session:
            with session.begin():
                q = (select(Product)
                        .where(Product.cpu.like("%Z80%"))
                     )
                res = session.scalars(q).all()
                print(res)

    @staticmethod
    def database_tables_3():
        """
        Products that use either the "Z80" or the "6502" CPUs, or any of its
        clones, built before 1990, sorted alphabetically by name
        """
        with Session() as session:
            with session.begin():
                q = (select(Product)
                        .where(
                            Product.year < 1990,
                            or_(Product.cpu.like("%Z80%"),
                                Product.cpu.like("%6502%")
                            )
                        )
                        .order_by(Product.name)
                    )
                res = session.scalars(q).all()
                for r in res:
                    print(r)

    @staticmethod
    def database_tables_4():
        """
        The manufacturers that built products in the 1980s.
        """
        with Session() as session:
            with session.begin():
                q = (select(Product.manufacturer)
                        .where(Product.year.between(1980, 1989))
                        .distinct()
                     )
                res = session.scalars(q).all()
                print(res)

    @staticmethod
    def database_tables_5():
        """
        Manufacturers whose names start with the letter "T", sorted
        alphabetically.
        """
        with Session() as session:
            with session.begin():
                q = (select(Product.manufacturer)
                      .where(Product.manufacturer.like("T%"))
                      .order_by(Product.manufacturer)
                      .distinct()
                     )
                res = session.scalars(q).all()
                print(res)

    @staticmethod
    def database_tables_6():
        """
        The first and last years in which products have been built in Croatia,
        along with the number of products built
        """
        with Session() as session:
            with session.begin():
                #q = select(
                    #func.min(Product.year), func.max(Product.year),
                    #func.count(Product.id)
                    #).where(Product.country == 'Croatia')
                
                q = (select(
                        Product.country,
                        func.min(Product.year),
                        func.max(Product.year),
                        func.count()
                    )
                        .where(Product.country == "Croatia")
                        .group_by(Product.country)
                )
                res = session.execute(q).first()
                print(q)
                print(res)

    @staticmethod
    def database_tables_7():
        """
        The number of products that were built each year. The results should
        start from the year with the most products, to the year with the least.
        Years in which no products were built do not need to be included.
        """
        with Session() as session:
            with session.begin():
                count_by_year = func.count(Product.id).label(None)
                q = (select(Product.year, count_by_year)
                        .group_by(Product.year)
                        .having(count_by_year > 0)
                        .order_by(count_by_year.desc())
                     )
                res = session.execute(q).all()
                print(res)
                print(len(res))

    @staticmethod
    def database_tables_8():
        """
        The number of manufacturers in the United States (note that the
        country field for these products is set to USA)
        """
        with Session() as session:
            with session.begin():
                q = (select(func.count(Product.manufacturer.distinct()))
                        .where(Product.country == 'USA'))

                #q = (select(func.count(Product.manufacturer.distinct()))
                #        .group_by(Product.country)
                #        .having(Product.country == "USA")
                #     )
                res = session.scalar(q)
            return res
                
#Chapter 3 One-To-Many Relationship
class Chapter3:

    @staticmethod
    def one_to_many_1():
        """
        The list of products made by IBM and Texas Instruments.
        """
        with Session() as session:
            with session.begin():
                q = (
                    select(Product)
                        .join(Manufacturer)
                            .where(
                                or_(
                                    Manufacturer.name == "IBM",
                                    Manufacturer.name == "Texas Instruments"
                                )
                            )
                )
                res = session.scalars(q).all()
                print(res)

    @staticmethod
    def one_to_many_2():
        """
        Manufacturers that operate in Brazil.
        """
        with Session() as session:
            with session.begin():
                q = select(Manufacturer).join(Product).where(Product.country == "Brazil").distinct()
                res = session.scalars(q).all()
                print(res)

    @staticmethod
    def one_to_many_3():
        """
        Products that have a manufacturer that has the word "Research" in their name.
        """
        with Session() as session:
            with session.begin():
                # q = select(Product).join(Product.manufacturer).where(Manufacturer.name.contains("Research"))
                q = select(Product)\
                        .join(Product.manufacturer)\
                        .where(Manufacturer.name.like("%Research%"))
                res = session.scalars(q).all()
                pprint(res)

    @staticmethod
    def one_to_many_4():
        """
        Manufacturers that made products based on the Z80 CPU or any of its clones.
        """
        with Session() as session:
            with session.begin():
                q = select(Manufacturer).join(Product).where(Product.cpu.like("%Z80%")).distinct()
                res = session.scalars(q).all()
                pprint(res)

    @staticmethod
    def one_to_many_5():
        """
        Manufacturers that made products that are not based on the 6502 CPU or any of its clones.
        """
        with Session() as session:
            with session.begin():
                q = select(Manufacturer)\
                        .join(Manufacturer.products)\
                        .where(not_(Product.cpu.like("%6502%")))\
                        .distinct()
                res = session.scalars(q).all()
                pprint(len(res))

    @staticmethod
    def one_to_many_6():
        """
        Manufacturers and the year they went to market with their first product, sorted by the year.
        """
        with Session() as session:
            with session.begin():
                first_year = func.min(Product.year).label(None)
                q = (select(Manufacturer, first_year)
                     .join(Manufacturer.products)
                     .group_by(Manufacturer)
                     .order_by(first_year))
                # q = select(Manufacturer, Product.year)\
                #         .join(Manufacturer.products)\
                #         .group_by(Manufacturer)\
                #         .having(func.min(Product.year))\
                #         .order_by(Product.year)
                res = session.execute(q).all()
                pprint(len(res))

    @staticmethod
    def one_to_many_7():
        """
        Manufacturers that have 3 to 5 products in the catalog.
        """
        with Session() as session:
            with session.begin():
                q = select(Manufacturer).join(Product).group_by(Manufacturer).having(func.count(Product.id).between(3,5))
                res = session.scalars(q).all()
                pprint(len(res))
                pprint(res)

    @staticmethod
    def one_to_many_8():
        """
        Manufacturers that operated for more than 5 years
        """
        with Session() as session:
            with session.begin():
                min_year = func.min(Product.year).label(None)
                max_year = func.max(Product.year).label(None)
                q = select(Manufacturer).join(Product).group_by(Manufacturer).having((max_year - min_year) > 5)
                res = session.scalars(q).all()
                pprint(len(res))
                pprint(res)

if __name__ == "__main__":
    # Chapter2.database_tables_1()
    # Chapter2.database_tables_2()
    # Chapter2.database_tables_3()
    # Chapter2.database_tables_4()
    # Chapter2.database_tables_5()
    # Chapter2.database_tables_6()
    # Chapter2.database_tables_7()
    # Chapter3.one_to_many_1()
    # Chapter3.one_to_many_2()
    # Chapter3.one_to_many_3()
    # Chapter3.one_to_many_4()
    # Chapter3.one_to_many_5()
    # Chapter3.one_to_many_6()
    # Chapter3.one_to_many_7()
    Chapter3.one_to_many_8()