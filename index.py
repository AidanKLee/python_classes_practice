from datetime import datetime

# Class Creation
class Business:
  def __init__(self, name, franchises = []):
    self.name = name
    self.franchises = franchises
  
  def add_restaurants(self, restaurants):
    def add(self, restaurant):
      if type(restaurant) == Restaurant:
        restaurant.update_business(self)
        self.franchises.append(restaurant)
    if isinstance(restaurants, list):
      for restaurant in restaurants:
        add(self, restaurant)
    else:
      add(self, restaurants)

class Restaurant:
  def __init__(self, name, address, opening_time, closing_time, franchise = None, menus = {}):
    self.name = name.title()
    self.franchise = franchise
    self.address = address
    self.menus = menus
    self.opening_time = opening_time
    self.closing_time = closing_time

  def __repr__(self):
    if self.franchise:
      franchise = self.franchise.name
    else:
      franchise = self.name
    return "{}\nName: {}\nOpening Times: {} to {}\nAddress: {}".format(franchise, self.name, self.opening_time, self.closing_time, self.address)

  def update_business(self, business):
    if type(business) == Business:
      self.franchise = business
  
  def add_menu(self, menu):
    if type(menu) == Menu:
      self.menus[menu.name.lower().replace(' ', '_')] = menu

  def all_menus(self):
    return [menu for menu in self.menus.values()]

  def available_menus(self, time = None):
    available = []
    for menu in self.menus.values():
      start_hour = int(menu.start_time.split(':')[0])
      end_hour = int(menu.end_time.split(':')[0])
      if time:
        if isinstance(time, str):
          current_hour = int(time.split(':')[0])
        elif isinstance(time, int):
          current_hour = time
        else:
          return print('If entering a time, it must be a string for the hour or time (11 / 11:00).')
        if (current_hour >= start_hour) and (current_hour < end_hour):
          available.append(menu)
      else:
        current_hour = int(datetime.now().hour)
        if (current_hour >= start_hour) and (current_hour < end_hour):
          available.append(menu)
    return available

  def calculate_bill(self, purchased_items, menu = ''):
    if (len(menu) > 0) and menu in self.menus:
      total = self.menus[menu].calculate_bill(purchased_items)
    else:
      total = 0
      for item in purchased_items:
        for key, value in self.menus.items():
          if item in value.items:
            total += value.calculate_bill([item])
            break
    self.orders.append({
      'purchased_items': purchased_items,
      'total': total
    })
    return total
  
  orders = []


class Menu:
  def __init__(self, name, items, start_time, end_time):
    self.name = name.title()
    self.items = items
    self.start_time = start_time
    self.end_time = end_time

  def __repr__(self):
    return "{} menu available from {} to {}".format(self.name, self.start_time, self.end_time)

  def calculate_bill(self, purchased_items):
    total = 0
    for item in purchased_items:
      if item in self.items:
        total += self.items[item]
    return total

# Menu Items
brunch_items = {
  'pancakes': 7.50, 'waffles': 9.00, 'burger': 11.00, 'home fries': 4.50, 'coffee': 1.50, 'espresso': 3.00, 'tea': 1.00, 'mimosa': 10.50, 'orange juice': 3.50
}
early_bird_items = {
  'salumeria plate': 8.00, 'salad and breadsticks (serves 2, no refills)': 14.00, 'pizza with quattro formaggi': 9.00, 'duck ragu': 17.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 1.50, 'espresso': 3.00
}
dinner_items = {
  'crostini with eggplant caponata': 13.00, 'caesar salad': 16.00, 'pizza with quattro formaggi': 11.00, 'duck ragu': 19.50, 'mushroom ravioli (vegan)': 13.50, 'coffee': 2.00, 'espresso': 3.00
}
kids_items = {
  'chicken nuggets': 6.50, 'fusilli with wild mushrooms': 12.00, 'apple juice': 3.00
}

# Restaurant Creation
flagship_store = Restaurant('The Horseshoe', '1232 West End Road', '11:00', '23:00')
new_installment = Restaurant('The Kings Head', '12 East Mulberry Street', '11:00', '23:00')
arepas_place = Restaurant('Take a\' Arepa', '189 Fitzgerald Avenue', '11:00', '23:00')

# Menu Creation
brunch = Menu('Brunch', brunch_items, '11:00', '16:00')
early_bird = Menu('Early Bird', early_bird_items, '15:00', '18:00')
dinner = Menu('Dinner', dinner_items, '17:00', '23:00')
kids = Menu('Kids', kids_items, '11:00', '21:00')

restaurant_menus = [brunch, early_bird, dinner, kids]

# Adding Menus To Restaurant
for menu in restaurant_menus:
  flagship_store.add_menu(menu)
  new_installment.add_menu(menu)

# Business Creation
basta = Business("Basta Fazoolin' with my Heart")
basta.add_restaurants([flagship_store, new_installment, arepas_place])

# Testing Bill Calculation
flagship_store.calculate_bill(['burger', 'home fries', 'coffee'])
flagship_store.calculate_bill(['salumeria plate', 'mushroom ravioli (vegan)'])

print(basta.franchises[0].orders)