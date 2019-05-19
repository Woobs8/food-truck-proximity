from . import db

class FoodTruck(db.Model):
    """
    A class used to encapsulate Foodtruck database model

    Attributes
    ----------
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
    
    get_food_trucks_within_radius(lon, lat, radius)
        Queries database and returns the trucks in the database within radius distance
        of position specified by lon(gitude) and lat(itude)
    """

    __tablename__ = 'sf_food_trucks'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    longitude = db.Column(db.Float(), index=True)
    latitude = db.Column(db.Float(), index=True)
    days_hours = db.Column(db.String())
    food_items = db.Column(db.String())

    def __init__(self, name: str, longitude: float, latitude: float, days_hours: str, food_items: str):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.days_hours = days_hours
        self.food_items = food_items

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

    @classmethod
    def get_food_trucks_within_radius(cls, lon, lat, radius):
        """
        Queries database and returns the trucks in the database within radius distance
        of position specified by lon(gitude) and lat(itude)
        """
        query = db.text("""
            SELECT *
            FROM (
                SELECT 
                    *,
                    2 * 6371 * asin(sqrt((sin(radians((:lat - latitude) / 2))) ^ 2 + 
                    cos(radians(latitude)) * cos(radians(:lat)) * (sin(radians((:lon - longitude) / 2))) ^ 2)) 
                    as distanceInKM                            
                FROM "sf_food_trucks") sfft
            WHERE sfft.distanceInKM*1000 <= :dist
            ORDER BY sfft.distanceInKM
            """)

        food_trucks = cls.query.from_statement(query).params(
            lat=float(lat),
            lon=float(lon),
            dist=int(radius)).all()

        return food_trucks