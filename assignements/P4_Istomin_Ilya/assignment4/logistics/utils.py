



transport_params = {
    'road': {'time_per_100km': 60, 'load_unload_time': 5, 'cost_per_100km': 1.0},
    'railway': {'time_per_100km': 50, 'load_unload_time': 10, 'cost_per_100km': 0.8},
    'aerial': {'time_per_100km': 10, 'load_unload_time': 40, 'cost_per_100km': 3.5},
    'maritime': {'time_per_100km': 120, 'load_unload_time': 20, 'cost_per_100km': 0.3},
}




nodes = [
    {'id': 'Madrid', 'type': 'Warehouse', 'name': 'Madrid', 'color': 'red'},
    {'id': 'Barcelona', 'type': 'Warehouse', 'name': 'Barcelona', 'color': 'red'},
    {'id': 'Valencia', 'type': 'Intermediate', 'name': 'Valencia', 'color': 'blue'},
    {'id': 'Seville', 'type': 'City', 'name': 'Seville', 'color': 'blue'},
    {'id': 'Malaga', 'type': 'City', 'name': 'Malaga', 'color': 'blue'},
    {'id': 'Bilbao', 'type': 'City', 'name': 'Bilbao', 'color': 'blue'},
    {'id': 'Zaragoza', 'type': 'City', 'name': 'Zaragoza', 'color': 'blue'},
    {'id': 'Granada', 'type': 'City', 'name': 'Granada', 'color': 'blue'},
    {'id': 'Alicante', 'type': 'City', 'name': 'Alicante', 'color': 'blue'},
    {'id': 'Palma', 'type': 'City', 'name': 'Palma', 'color': 'green'},
]


edges = [
    {'from': 'Madrid', 'to': 'Barcelona', 'distance': 620, 'transports': ['road', 'railway', 'aerial']},
    {'from': 'Madrid', 'to': 'Valencia', 'distance': 360, 'transports': ['road', 'railway']},
    {'from': 'Madrid', 'to': 'Seville', 'distance': 530, 'transports': ['road', 'railway']},
    {'from': 'Madrid', 'to': 'Zaragoza', 'distance': 320, 'transports': ['road']},
    {'from': 'Madrid', 'to': 'Alicante', 'distance': 420, 'transports': ['road']},
    {'from': 'Madrid', 'to': 'Bilbao', 'distance': 400, 'transports': ['road', 'railway']},


    {'from': 'Barcelona', 'to': 'Valencia', 'distance': 350, 'transports': ['road', 'railway']},
    {'from': 'Barcelona', 'to': 'Palma', 'distance': 250, 'transports': ['aerial', 'maritime']},
    {'from': 'Barcelona', 'to': 'Zaragoza', 'distance': 300, 'transports': ['road', 'railway']},

  
    {'from': 'Valencia', 'to': 'Palma', 'distance': 270, 'transports': ['aerial', 'maritime']},
    {'from': 'Valencia', 'to': 'Alicante', 'distance': 180, 'transports': ['road']},
    {'from': 'Valencia', 'to': 'Seville', 'distance': 650, 'transports': ['road', 'railway']},

   
    {'from': 'Seville', 'to': 'Malaga', 'distance': 210, 'transports': ['road']},
    {'from': 'Seville', 'to': 'Granada', 'distance': 250, 'transports': ['road']},
    {'from': 'Seville', 'to': 'Bilbao', 'distance': 900, 'transports': ['road', 'railway']},

    
    {'from': 'Malaga', 'to': 'Palma', 'distance': 700, 'transports': ['aerial', 'maritime']},
    {'from': 'Malaga', 'to': 'Granada', 'distance': 125, 'transports': ['road']},
    {'from': 'Malaga', 'to': 'Valencia', 'distance': 650, 'transports': ['road']},


    {'from': 'Bilbao', 'to': 'Zaragoza', 'distance': 300, 'transports': ['road', 'railway']},
    {'from': 'Bilbao', 'to': 'Barcelona', 'distance': 610, 'transports': ['road', 'railway']},

 
    {'from': 'Zaragoza', 'to': 'Barcelona', 'distance': 300, 'transports': ['road', 'railway']},
    {'from': 'Zaragoza', 'to': 'Valencia', 'distance': 310, 'transports': ['road']},

    
    {'from': 'Alicante', 'to': 'Granada', 'distance': 300, 'transports': ['road']},
    {'from': 'Alicante', 'to': 'Malaga', 'distance': 480, 'transports': ['road']},

 
    {'from': 'Granada', 'to': 'Malaga', 'distance': 125, 'transports': ['road']},
    {'from': 'Granada', 'to': 'Seville', 'distance': 250, 'transports': ['road']},

   
    {'from': 'Palma', 'to': 'Barcelona', 'distance': 250, 'transports': ['aerial', 'maritime']},
    {'from': 'Palma', 'to': 'Valencia', 'distance': 270, 'transports': ['aerial', 'maritime']},
]



