from sqlalchemy import select
from db import Session
from models import Product


if __name__ == "__main__":
    q = select(Product)
    with Session() as session:
        r = session.execute(q)
    print(r)
