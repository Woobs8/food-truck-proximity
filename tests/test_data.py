import datetime

# location used for test requests
test_location = (37.7201, -122.3886)

# expected results for name search (search string, count, ordered ids)
test_name = ('Liang', 5, [8, 11, 14, 16, 17])

# expected results for item search (search string, count, ordered ids)
test_item = ('sandwiches', 12, [6, 1, 2, 4, 8, 10, 11, 12, 14, 15, 16, 17])

# expected results for different search radius {radius: (count, oredered ids)}
test_radius = {10: (0, []), 
            100: (1, [5]), 
            400: (8, [5, 6, 7, 1, 2, 3, 4, 8]), 
            500: (17, [5, 6, 7, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])}

# test data used to populate the database for testing purposes
test_data = [
  {
    "days_hours": "Mo/We/Fr:10AM-2PM", 
    "food_items": "Corndogs: fried burrito: rice placet: soda: water: sandwiches: soup: noodle plates", 
    "latitude": 37.7226292175983, 
    "longitude": -122.390061846327, 
    "name": "Eva's Catering", 
    "uuid": 1
  }, 
  {
    "days_hours": "Mo-Fr:8AM-9AM", 
    "food_items": "Cold Truck: Sandwiches: Noodles:  Pre-packaged Snacks: Candy: Desserts Various Beverages", 
    "latitude": 37.723078757516, 
    "longitude": -122.387525704017, 
    "name": "Anas Goodies Catering", 
    "uuid": 2
  }, 
  {
    "days_hours": "Mo-Fr:12PM-1PM", 
    "food_items": "Ice Cream: Pre-Packaged Chips: Candies: Bottled Water & Canned SODA", 
    "latitude": 37.716991290324, 
    "longitude": -122.38959908417, 
    "name": "Singh Brothers Ice Cream", 
    "uuid": 3
  }, 
  {
    "days_hours": "Mo-Su:10AM-11AM", 
    "food_items": "Cold Truck: Sandwiches: fruit: snacks: candy: hot and cold drinks", 
    "latitude": 37.717779453627, 
    "longitude": -122.391654765179, 
    "name": "May Catering", 
    "uuid": 4
  },
  {
    "days_hours": "Mo-Fr:2PM-3PM", 
    "food_items": "Ice Cream: Pre-Packaged Chips: Candies: Bottled Water & Canned SODA", 
    "latitude": 37.7201747226493, 
    "longitude": -122.389407114342, 
    "name": "Singh Brothers Ice Cream", 
    "uuid": 5
  }, 
  {
    "days_hours": "Mo-Fr:7AM-8AM", 
    "food_items": "Cold Truck: Sandwiches: Noodles:  Pre-packaged Snacks: Candy: Desserts Various Beverages", 
    "latitude": 37.7214508397335, 
    "longitude": -122.389353445076, 
    "name": "Anas Goodies Catering", 
    "uuid": 6
  }, 
  {
    "days_hours": "Mo-Fr:12PM-1PM", 
    "food_items": "Ice Cream: Pre-Packaged Chips: Candies: Bottled Water & Canned SODA", 
    "latitude": 37.7189398190959, 
    "longitude": -122.390517872066, 
    "name": "Singh Brothers Ice Cream", 
    "uuid": 7
  }, 
  {
    "days_hours": "Mo-Fr:9AM-10AM", 
    "food_items": "Cold Truck: Pre-packaged sandwiches: snacks: fruit: various beverages", 
    "latitude": 37.7230565093389, 
    "longitude": -122.391111940642, 
    "name": "Liang Bai Ping", 
    "uuid": 8
  }, 
  {
    "days_hours": "Mo-Fr:1PM-2PM", 
    "food_items": "Ice Cream: Pre-Packaged Chips: Candies: Bottled Water & Canned SODA", 
    "latitude": 37.7227936887593, 
    "longitude": -122.391719666472, 
    "name": "Singh Brothers Ice Cream", 
    "uuid": 9
  }, 
  {
    "days_hours": "Mo-Fr:7AM-8AM", 
    "food_items": "Cold Truck: Sandwiches: Noodles:  Pre-packaged Snacks: Candy: Desserts Various Beverages", 
    "latitude": 37.7235768564887, 
    "longitude": -122.390059101399, 
    "name": "Anas Goodies Catering", 
    "uuid": 10
  }, 
  {
    "days_hours": "Mo-Fr:7AM-8AM", 
    "food_items": "Cold Truck: Pre-packaged sandwiches: snacks: fruit: various beverages", 
    "latitude": 37.7232598663241, 
    "longitude": -122.391172885969, 
    "name": "Liang Bai Ping", 
    "uuid": 11
  }, 
  {
    "days_hours": "Mo-Su:9AM-10AM", 
    "food_items": "Cold Truck: Sandwiches: fruit: snacks: candy: hot and cold drinks", 
    "latitude": 37.7164430021474, 
    "longitude": -122.389937879321, 
    "name": "May Catering", 
    "uuid": 12
  }, 
  {
    "days_hours": "Mo-Fr:12PM-1PM", 
    "food_items": "Ice Cream: Pre-Packaged Chips: Candies: Bottled Water & Canned SODA", 
    "latitude": 37.7164430021474, 
    "longitude": -122.389937879321, 
    "name": "Singh Brothers Ice Cream", 
    "uuid": 13
  }, 
  {
    "days_hours": "Mo-Fr:7AM-8AM/10AM-11AM", 
    "food_items": "Cold Truck: Pre-packaged sandwiches: snacks: fruit: various beverages", 
    "latitude": 37.7238788408325, 
    "longitude": -122.387010878785, 
    "name": "Liang Bai Ping", 
    "uuid": 14
  }, 
  {
    "days_hours": "Mo-Su:10AM-11AM", 
    "food_items": "Cold Truck: Pre-packaged Sandwiches: Various Beverages: Salads: Snacks", 
    "latitude": 37.7171741618036, 
    "longitude": -122.392222474624, 
    "name": "Golden Catering", 
    "uuid": 15
  }, 
  {
    "days_hours": "Mo-Fr:9AM-10AM/12PM-1PM", 
    "food_items": "Cold Truck: Pre-packaged sandwiches: snacks: fruit: various beverages", 
    "latitude": 37.7241728927613, 
    "longitude": -122.389735429011, 
    "name": "Liang Bai Ping", 
    "uuid": 16
  }, 
  {
    "days_hours": "Mo-Fr:9AM-10AM", 
    "food_items": "Cold Truck: Pre-packaged sandwiches: snacks: fruit: various beverages", 
    "latitude": 37.7244132432963, 
    "longitude": -122.390157239611, 
    "name": "Liang Bai Ping", 
    "uuid": 17
  }
]

test_users = [
    {
        'username': 'admin',
        'password': '1234321',
        'admin': True
    },
    {
        'username': 'user1',
        'password': '1234',
        'admin': False
    },
]