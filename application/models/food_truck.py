from application.haversine import haversine
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy import func
from sqlalchemy.orm import aliased
from flask_sqlalchemy import SQLAlchemy
from . import db, User

class FoodTruck(db.Model):
    """
    A class used to encapsulate Foodtruck database model

    Attributes
    ----------
    uuid (int)
        Unique identifer for truck (primary key for DB)

    name (string)
        Name of the truck
    
    longitude (float)
        Decimal longitude coordinate of truck
    
    latitude (float)
        Decimal latitude coordinate of truck
    
    days_hours (string)
        String representation of business days and hours

    food_items (string)
        String representation of menu items

    Methods
    -------
    serialize
        Returns a dictionary representation of a class instance

    great_circle_distance(lat, lon)
        Calculates the great-circle distance between an instance of FoodTruck
        and a specified coordinate.
    
    get_food_trucks_within_radius(lon, lat, radius, name, item)
        Queries database and returns the trucks in the database within radius distance
        of position specified by lon(gitude) and lat(itude). Optionally filters results
        by the trucks with names and/or menu items that contains the specified strings
    """

    __tablename__ = 'sf_food_trucks'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    longitude = db.Column(db.Float(), index=True)
    latitude = db.Column(db.Float(), index=True)
    days_hours = db.Column(db.String())
    food_items = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True, default=None)


    def __init__(self, name, longitude, latitude, days_hours, food_items, user_id):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.days_hours = days_hours
        self.food_items = food_items
        self.user_id = user_id


    def __repr__(self):
        return '<name {}>'.format(self.name)


    def serialize(self):
        """
        Returns a dictionary representation of a class instance
        """
        return {
            'uuid': self.uuid, 
            'name': self.name,
            'longitude': self.longitude,
            'latitude':self.latitude,
            'days_hours':self.days_hours,
            'food_items':self.food_items        
        }


    @hybrid_method
    def great_circle_distance(self, lat, lon):
        """
        Calculates the distance from a FoodTruck instance to the location specified
        by the coordinates lat(itude) and lon(gitude). Hybrid_method is a sqlalchemy
        decorator that allows for the definition of both instance-level and
        class-level behavior. This is the instance level method, and it is processed
        as a regular Python statement.

        Parameters:
            lat (float): latitude coordinate in decimal format
            lon (float): longitude coordinate in decimal format

        Returns:
            float: distance between instance and specified coordinate
        """
        return haversine(lat, lon, self.latitude, self.longitude)


    @great_circle_distance.expression
    def great_circle_distance(cls, lat, lon):
        """
        Calculates the distance between an element in the FoodTruck model 
        and the location specified by the coordinates lat(itude) and lon(gitude). 
        Hybrid_method is a sqlalchemy decorator that allows for the definition of 
        both instance-level and class-level behavior. The {Hybrid_method}.expression 
        decorator defines class-level behavior for the method, and will map the 
        Python statement to SQL when used in a SQLAlchemy expresseion.

        Parameters:
            lat (float): latitude coordinate in decimal format
            lon (float): longitude coordinate in decimal format

        Returns:
            float: distance between model element and specified coordinate
        """
        return haversine(lat, lon, cls.latitude, cls.longitude, math=func)


    @classmethod
    def get_food_trucks_within_radius(cls, lat, lon, radius, name=None, item=None):
        """
        Class method that queries the database and returns the trucks in the 
        database within a distance of radius from the position specified by 
        lon(gitude) and lat(itude).
        
        Parameters:
            lat (float): latitude coordinate in decimal format
            lon (float): longitude coordinate in decimal format
            radius (int): search radius in meters
            name (str): substring that names must contain
            item (str): substring that food_items must contain

        Returns:
            list: list of FoodTruck objects
        """
        # ensure correct data types
        lat = float(lat)
        lon = float(lon)
        radius = float(radius)

        # subquery great-circle distance between coordinate and elements in database
        stmt = db.session.query(cls,
                                cls.great_circle_distance(lat, lon)
                                .label('dist')).subquery()
        food_truck_alias = aliased(cls, stmt)

        # filter by search radius
        food_trucks = db.session.query(food_truck_alias).filter(stmt.c.dist <= radius)

        # filter by name if specified
        if name:
            food_trucks = food_trucks.filter(stmt.c.name.ilike('%{}%'.format(name)))
        
        # filter by item if specified
        if item:
            food_trucks = food_trucks.filter(stmt.c.food_items.ilike('%{}%'.format(item)))
        
        # sort by distance ascending
        food_trucks = food_trucks.order_by(stmt.c.dist)

        return food_trucks.all()