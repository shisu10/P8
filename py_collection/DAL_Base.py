# crud/base.py
from config import settings
if settings.DATABASE_ORM == "SA":
    from DAL.SA import User_DA, Role_DA, Access_DA
else:
    from DAL.TO import User_DA, Role_DA, Access_DA

