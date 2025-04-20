from sqlalchemy import select, or_, func
from db import Session
from models import Product

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
                



if __name__ == "__main__":
    #Chapter2.database_tables_1()
    #Chapter2.database_tables_2()
    #Chapter2.database_tables_3()
    #Chapter2.database_tables_4()
    #Chapter2.database_tables_5()
    #Chapter2.database_tables_6()
    #Chapter2.database_tables_7()
    assert Chapter2.database_tables_8() == 17