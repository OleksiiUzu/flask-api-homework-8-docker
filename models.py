from sqlalchemy import Column, Integer, String, ForeignKey, select, insert, Boolean
from database import Base, engine, db_session


class Usertype(Base):
    __tablename__ = 'User_type'
    ID = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(120), unique=True, nullable=False)

    def __init__(self, Name=None):
        self.Name = Name

    def __repr__(self):
        return f'<User {self.name!r}>'


class User(Base):
    __tablename__ = 'User'
    ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Telephone = Column(Integer, unique=True, nullable=False)
    Email = Column(String(120), unique=True, nullable=False)
    Password = Column(String(50), nullable=False)
    Tg = Column(String(120), unique=True)
    Type = Column(Integer, ForeignKey('User_type.ID'), nullable=False)
    verification = Column(Boolean, default=False)

    def __init__(self, ID=None, Telephone=None, Email=None, Password=None, Tg=None, Type=None):
        self.ID = ID
        self.Telephone = Telephone
        self.Email = Email
        self.Password = Password
        self.Tg = Tg
        self.Type = Type

    def __repr__(self):
        return f'{self.ID!r}>'


class Address(Base):
    __tablename__ = 'Address'
    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    Town = Column(String(120), nullable=False)
    Street = Column(String(120), nullable=False)
    House = Column(String(120),  nullable=False)
    Apt = Column(String(120))
    Block = Column(Integer)
    Floor = Column(Integer)
    User = Column(Integer, ForeignKey(User.ID), nullable=False)

    def __init__(self, ID=None, Town=None, Street=None, House=None, Apt=None, Block=None, Floor=None, User=None):
        self.ID = ID
        self.Town = Town
        self.Street = Street
        self.House = House
        self.Apt = Apt
        self.Block = Block
        self.Floor = Floor
        self.User = User

    def __repr__(self):
        return f'<User {self.ID!r}>'


class Category(Base):
    __tablename__ = 'Category'
    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    Name = Column(String(120), nullable=False, unique=False)

    def __init__(self, ID=None, Name=None):
        self.ID = ID
        self.Name = Name

    def __repr__(self):
        return f'<User {self.ID!r} {self.Name!r}>'


class Dishes(Base):
    __tablename__ = 'Dishes'
    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    Dish_name = Column(String(120), nullable=False)
    Price = Column(Integer, nullable=False)
    Description = Column(String(256), nullable=True)
    Available = Column(Integer, nullable=False)
    Category = Column(Integer, ForeignKey(Category.ID), nullable=False)
    Photo = Column(String(256), nullable=True)
    Ccal = Column(Integer, nullable=False)
    Protein = Column(Integer, nullable=False)
    Fat = Column(Integer, nullable=False)
    Carb = Column(Integer, nullable=False)

    def __init__(self, ID=None, Dish_name=None, Price=None,
                 Description=None, Available=None, Category=None,
                 Photo=None, Ccal=None, Protein=None, Fat=None, Carb=None):

        self.ID = ID
        self.Dish_name = Dish_name
        self.Price = Price
        self.Description = Description
        self.Available = Available
        self.Category = Category
        self.Photo = Photo
        self.Ccal = Ccal
        self.Protein = Protein
        self.Fat = Fat
        self.Carb = Carb

    def __repr__(self):
        return f'<User {self.Dish_name!r}>'


class Status(Base):
    __tablename__ = 'Status'
    ID = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(120), unique=True, nullable=False)

    def __init__(self, status=None):
        self.status = status

    def __repr__(self):
        return f'<User {self.status!r}>'


class Orders(Base):
    __tablename__ = 'Orders'
    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    User = Column(Integer, ForeignKey(User.ID), nullable=False)
    Address = Column(Integer, ForeignKey(Address.ID), nullable=False)
    price = Column(Integer, nullable=False)
    Ccal = Column(Integer, nullable=False)
    Fat = Column(Integer, nullable=False)
    Protein = Column(Integer, nullable=False)
    Carbon = Column(Integer, nullable=False)
    Coment = Column(Integer)
    Order_date = Column(Integer, nullable=False)
    Rate = Column(Integer)
    Status = Column(String(120), ForeignKey(Status.ID), unique=True, nullable=False)

    def __init__(self, ID=None, User=None, Address=None,
                 price=0, Ccal=0, Fat=0,
                 Protein=0, Carbon=0, Coment=None,
                 Order_date=None, Rate=None, Status=None):

        self.ID = ID
        self.User = User
        self.Address = Address
        self.price = price
        self.Ccal = Ccal
        self.Fat = Fat
        self.Protein = Protein
        self.Carbon = Carbon
        self.Coment = Coment
        self.Order_date = Order_date
        self.Rate = Rate
        self.Status = Status

    def __repr__(self):
        return f'<User {self.ID!r}>'


class OrderedDishes(Base):
    __tablename__ = 'Ordered_dishes'
    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    dish = Column(String, ForeignKey(Dishes.ID), nullable=False)
    count = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey(Orders.ID), nullable=False)

    def __init__(self, ID=None, dish=None, count=None, order_id=None):
        self.ID = ID
        self.dish = dish
        self.count = count
        self.order_id = order_id

    def __repr__(self):
        return f'<User {self.ID!r}>'


class DishRate(Base):
    __tablename__ = 'Dish_rate'
    ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    Dish = Column(Integer, ForeignKey(Dishes.ID), nullable=False, unique=True)
    User = Column(Integer, ForeignKey(User.ID), nullable=False, unique=True)

    def __init__(self, ID=None, Dish=None, User=None):
        self.ID = ID
        self.Dish = Dish
        self.User = User

    def __repr__(self):
        return f'<User {self.ID!r}>'


class EmailVarification(Base):
    __tablename__ = 'Email_Varification'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.ID'), nullable=False)
    code = Column(String, nullable=False)

    def __int__(self, ID=None, user_id=None, code=None):
        self.email = user_id
        self.code = code
