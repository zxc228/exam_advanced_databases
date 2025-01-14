__author__ = 'Pablo Ramos Criado'
__students__ = 'Ilya Istomin'

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from typing import Generator, Any, Self
from geojson import Point
from pymongo.collection import Collection
from pymongo.cursor import Cursor


import json
import pymongo
import yaml

def getLocationPoint(address: str) -> Point:
    """
    Gets the coordinates of an address in geojson.Point format
    Use the geopy API to get the coordinates of the address
    Be careful, the API is public and has a request limit, use sleeps.

    Parameters
    ----------
    address : str
    full address from which to get the coordinates
    Returns
    -------
    geojson.Point
    coordinates of the point of the address
    """
    import random
    import string

    location = None
    while location is None:
        length = random.randint(5, 25)
    
        letters_array = ''.join([random.choice(string.ascii_letters) for _ in range(length)])

        location = None
        geolocator = Nominatim(user_agent=letters_array)
        try:
            time.sleep(1)
            #DONE
            # It is You need to provide a user_agent to use the API
            # Use a random name for the user_agent
            location = geolocator.geocode(address)
        except GeocoderTimedOut:
            # May throw an exception if the timeout occurs
            # Try again
            print("GeocoderTimedOut: Retrying...")
        
    #DONE
    if location:
        point = Point((location.longitude, location.latitude))
        return point
    else:
        raise ValueError('Location not found')
        
def get_coordinates_as_dict(address: str) -> dict:
    #func for transforming geoLocation to dict
    location_point = getLocationPoint(address)
    return {"longitude": location_point['coordinates'][0], "latitude": location_point['coordinates'][1]}
    



def export_collection_to_json(collection: Collection, file_name: str) -> None:
    """
    Exports a MongoDB collection to a JSON file.
    
    Parameters
    ----------
    collection : Collection
        MongoDB collection to export.
    file_name : str
        Name of the file to export to.
    """
    cursor = collection.find({})
    data = list(cursor)
    # Change ObjectId to string for export purposes
    for document in data:
        if "_id" in document:
            document["_id"] = str(document["_id"])
    
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)


def load_data_from_json(filename="data.json"):
    with open(filename, "r") as json_file:
        return json.load(json_file)




class Model:
    """
    Abstract model class
    Create as many classes that inherit from this class as
    collections/models you want to have in the database.
    """
    cache = None

    def __init__(self, **kwargs):
        """
        Initializes the model with the values provided in kwargs.
        Checks that the values are supported by the model and
        that the required variables are provided.
        """
        allowed_vars = self.required_vars | self.admissible_vars | {"_id"}

        missing_vars = self.required_vars - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

        invalid_vars = set(kwargs.keys()) - allowed_vars
        if invalid_vars:
            raise ValueError(f"Invalid fields provided: {invalid_vars}")

        # Assign all the values in kwargs to the instance attributes
        self.__dict__.update(kwargs)

    @classmethod
    def initialize_cache(cls, cache_instance):
        """
        Initializes the Redis cache with proper settings.
        """
        cls.cache = cache_instance
        cls.cache.config_set("maxmemory", "150mb")
        cls.cache.config_set("maxmemory-policy", "volatile-lru")

    @classmethod
    def init_class(cls, db_collection: Collection, required_vars: set[str], admissible_vars: set[str]) -> None:
        """
        Initializes the class variables at system initialization.
        """
        cls.db = db_collection
        cls.required_vars = required_vars
        cls.admissible_vars = admissible_vars

    @classmethod
    def find(cls, filter: dict[str, str | dict]) -> list[dict]:
        if cls.cache is None:
            raise ValueError("Cache has not been initialized. Use 'initialize_cache' first.")

        cache_key = f"find:{json.dumps(filter, sort_keys=True)}"
        cached_result = cls.cache.get(cache_key)

        if cached_result:
            cls.cache.expire(cache_key, 86400)
            print(f"Returning results from cache for filter: {filter}")
            return json.loads(cached_result)

        print(f"We don't have such query in cache\nQuerying MongoDB for filter: {filter}")
        cursor = cls.db.find(filter)
        results = list(cursor)

        # Cache results for 24 hours (86400 seconds)
        cls.cache.setex(cache_key, 86400, json.dumps(results, default=str))

        # Save document IDs related to this query
        document_ids = [str(doc["_id"]) for doc in results]
        for doc_id in document_ids:
            cls.cache.sadd(f"doc:{doc_id}:queries", cache_key)  # Associate document ID with query key
        print(f"Cached results for filter: {filter} with associated document IDs: {document_ids}")

        return results

    @classmethod
    def find_by_id(cls, id: str) -> dict | None:
        """
        Searches for a document by its id using the cache.
        If the document is not found, fetches it from the database.
        """
        if cls.cache is None:
            raise ValueError("Cache has not been initialized. Use 'initialize_cache' first.")

        # Check in cache
        cached_data = cls.cache.get(id)
        if cached_data:
            print(f"Returning cached data for ID {id}.")
            return json.loads(cached_data)

        # Fetch from database
        print(f"No cached data found for ID {id}. Querying MongoDB.")
        document = cls.db.find_one({'_id': id})
        if document:
            cls.cache.set(id, json.dumps(document, default=str), ex=86400)  # Save to cache
        return document

    def save(self) -> None:
        """
        Save the model in the database.
        If the model does not exist in the database, a new document is created
        with the model values. Otherwise, the existing document is updated with the new
        model values. Invalidates all related cache entries.
        """
        if not hasattr(self, '_id'):
            result = self.db.insert_one(self.__dict__)
            self._id = str(result.inserted_id)
        else:
            update_data = {key: value for key, value in self.__dict__.items() if key != '_id'}
            self.db.update_one({'_id': self._id}, {'$set': update_data})

        print(f"Invalidating cache for model {self.__class__.__name__} due to save...")
        self.invalidate_cache()

    def delete(self) -> None:
        """
        Deletes the model from the database and invalidates cache.
        """
        if not hasattr(self, '_id'):
            raise ValueError("Cannot delete a model without an ID.")

        self.db.delete_one({'_id': str(self._id)})
        print(f"Deleted from MongoDB: {self._id}")
        if self.cache:
            self.cache.delete(str(self._id))
            print(f"Removed from cache: {self._id}")

        print(f"Invalidating cache for model {self.__class__.__name__} due to delete...")
        self.invalidate_cache()

    def invalidate_cache(self):
        if self.cache is None:
            raise ValueError("Cache has not been initialized. Use 'initialize_cache' first.")

        if not hasattr(self, "_id"):
            raise ValueError("Cannot invalidate cache for a model without an ID.")

        # Get all queries associated with this document ID
        cache_keys = self.cache.smembers(f"doc:{self._id}:queries")
        for cache_key in cache_keys:
            self.cache.delete(cache_key)
            print(f"Invalidated cache key: {cache_key.decode('utf-8')}")

        # Remove document-to-query association
        self.cache.delete(f"doc:{self._id}:queries")

class ModelCursor:
    """
    Cursor to iterate over the documents of the result of a query. The documents must be returned in the form of model objects.

    Attributes
    ----------
    model_class : Model
    Class to create the models of the documents that are iterated.
    cursor : pymongo.cursor.Cursor
    pymongo cursor to iterate over

    Methods
    -------
    __iter__() -> Generator
    Returns an iterator that iterates over the cursor elements
    and returns the documents as model objects.
    """

    def __init__(self, model_class: Model, cursor: pymongo.cursor.Cursor):
        """
        Initializes the cursor with the pymongo model class and cursor

        Parameters
        ----------
        model_class : Model
        Class to create the models of the documents being iterated over.
        cursor: pymongo.cursor.Cursor
        Pymongo cursor to iterate
        """
        self.model = model_class
        self.cursor = cursor

    def __iter__(self) -> Generator:
        """
        Returns an iterator that iterates through the elements of the cursor
        and returns the documents as model objects.
        Use yield to generate the iterator
        Use the next function to get the next document from the cursor
        Use alive to check if there are more documents.
        """
        for document in self.cursor:
            yield self.model(**document)
        

    def initApp(definitions_path: str = "./models.yml", mongodb_uri="mongodb://localhost:27017/", db_name="abd") -> None:
        """
        Declare the classes that inherit from Model for each of the
        models in the collections defined in definitions_path.
        Initializes the model classes by providing the supported and required variables for each of them and the connection to the database collection.

        Parameters
        ----------
        definitions_path : str
        path to the model definitions file
        mongodb_uri : str
        database connection uri
        db_name : str
        database name
        """
        #DONE
        # Initialize database
        client = pymongo.MongoClient(mongodb_uri)
        db = client[db_name]
        
        #DONE
        # Declare as many model collection classes as exist in the database
        # Read the model definition file to get the collections
        # and the allowed and required variables for each of them.
        # Example of model declaration for collection called MyModel 
        with open(definitions_path, "r") as file:
            models_definitions = yaml.safe_load(file)
        # Ignore the warning from Pylance about MyModel, it is unable to detect
        # that the class has been declared in the previous line since it is done
        # at runtime.
        for model_name, model_info in models_definitions.items():
            # Extract required and admissible variables from the YAML file
            required_vars = set(model_info['required_vars'])
            admissible_vars = set(model_info['admissible_vars'])

            # Dynamically create model classes
            globals()[model_name] = type(model_name, (Model,), {})
            
            # Initialize the model class with the appropriate collection and variables
            globals()[model_name].init_class(db_collection=db[model_name.lower()], required_vars=required_vars, admissible_vars=admissible_vars)
        return globals()
    


if __name__ == '__main__':
    
    # PROJECT 1
    print("\nInitializing models from models_product.yml...")

    # #for local use

    ModelCursor.initApp(definitions_path="./models_product.yml", 
                       mongodb_uri = "mongodb://localhost:27017/", 
                        db_name="db1")
    

    
    # for cloud use (I use several computers and i have to use cloud)
    # Use MongoDB cluster (add your cluster URI and credentials)

    # from settings import Config
    # ModelCursor.initApp(definitions_path="./models_product.yml", 
    #         mongodb_uri=f"mongodb+srv://{Config.username}:{Config.password}@cluster0.og2pp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", 
    #         db_name="db1")

    
   
    #I am using local data.json file for inserting data into my mongo db collections
    data = load_data_from_json()
    
    for elem in data['customers']:
        customer = Customer(

            name=elem['name'],
            billing_addresses=elem['billing_addresses'],
            coordinates_billing_adresses = get_coordinates_as_dict(elem['billing_addresses']),
            registration_date=elem['registration_date'],
            shipping_addresses=elem['shipping_addresses'],
            coordinates_shipping_adresses = get_coordinates_as_dict(elem['shipping_addresses']),
            payment_cards=elem['payment_cards'],
            last_access_date=elem['last_access_date']
        )
        customer.save()
    
    for elem in data['products']:
        product = Product(
            name=elem['name'],
            supplier_product_code=elem['supplier_product_code'],
            price_without_vat=elem['price_without_vat'],
            price_with_vat=elem['price_with_vat'],
            shipping_cost=elem['shipping_cost'],
            discount_date_range=elem['discount_date_range'],
            dimensions=elem['dimensions'],
            weight=elem['weight'],
            suppliers=elem['suppliers']
        )
        product.save()
    
    for elem in data['purchases']:
        purchase = Purchase(
            products=elem['products'],
            customer=elem['customer'],
            purchase_price=elem['purchase_price'],
            purchase_date=elem['purchase_date'],
            shipping_address=elem['shipping_address'],
            shipping_coordinates=get_coordinates_as_dict(elem['shipping_address'])
        )
        purchase.save()

    for elem in data['suppliers']:
        supplier = Supplier(
            name=elem['name'],
            warehouse_addresses=elem['warehouse_addresses'],
            warehouse_coordinates=get_coordinates_as_dict(elem['warehouse_addresses'])
        )
        supplier.save()
   

    # Export all collections
    export_collection_to_json(Customer.db, "customer.json")
    export_collection_to_json(Product.db, "product.json")
    export_collection_to_json(Purchase.db, "purchase.json")
    export_collection_to_json(Supplier.db, "supplier.json")
    
    # Tests for each model

    # Test for Customer model
    print("\n==== Customer Test ====")
    customer = Customer(
        name="Tony Stark", 
        billing_addresses="1600 Pennsylvania Ave NW, Washington, DC 20500, USA",
        registration_date="2010-05-02", 
        coordinates_billing_adresses=get_coordinates_as_dict("1600 Pennsylvania Ave NW, Washington, DC 20500, USA"), 
        payment_cards="4111111111111111",
        last_access_date="2024-10-01"
    )
    customer.save()
    print(f"Created Customer: {customer.name}, Billing Address: {customer.billing_addresses}")

    # Update and verify
    address_billing = "United Nations Secretariat Building, 405 E 42nd St, New York, NY 10017, USA"
    customer.billing_addresses = address_billing
    customer.coordinates_billing_adresses = get_coordinates_as_dict(customer.billing_addresses)
    customer.save()
    print(f"Updated Billing Address: {customer.billing_addresses}")

    # Attempt to add invalid field
    try:
        customer.age = 54
    except ValueError as e:
        print(f"Error: {e}")


    # Test for Product model
    print("\n==== Product Test ====")
    product = Product(
        name="Iron Man Suit", 
        supplier_product_code="IMSUIT001", 
        price_without_vat=1000000, 
        price_with_vat=1210000, 
        shipping_cost=500, 
        discount_date_range={
                "start_date": "2024-01-01",
                "end_date": "2024-12-31"
            },
        dimensions={
                "length": 180,
                "width": 70,
                "height": 30
            }, 
        weight=95,
        suppliers="Stark Industries"
    )
    product.save()
    print(f"Created Product: {product.name}, Price with VAT: {product.price_with_vat}")

    # Обновление и проверка
    product.price_with_vat = 1250000
    product.save()
    print(f"Updated Price with VAT: {product.price_with_vat}")

    # Attempt to add invalid field
    try:
        product.status = "Verified"
    except ValueError as e:
        print(f"Error: {e}")

    # Test for Purchase model
    print("\n==== Purchase Test ====")
    purchase = Purchase(
        products=["Smartphone", "Tablet",  "Smart Speaker"], 
        customer="Tony Stark", 
        purchase_price=282.50, 
        purchase_date="2024-10-01",
    )
    purchase.save()
    print(f"Created Purchase: {purchase.products}, Customer: {purchase.customer}, Purchase Price: {purchase.purchase_price}")

    # Update and verify
    purchase.purchase_price = 300.00
    purchase.save()
    print(f"Updated Purchase Price: {purchase.purchase_price}")

    # Attempt to add invalid field
    try:
        purchase.status = "Verified"
    except ValueError as e:
        print(f"Error: {e}")


    # Test for Supplier model
    print("\n==== Supplier Test ====")
    
    supplier = Supplier(
        name="Avengers Inc.", 
        warehouse_addresses="701 D St NW, Washington, DC 20024, USA",
        warehouse_coordinates=get_coordinates_as_dict("701 D St NW, Washington, DC 20024, USA")
    )
    supplier.save()
    print(f"Created Supplier: {supplier.name}, Warehouse: {supplier.warehouse_addresses}")

    # Update and verify
    
    supplier.warehouse_addresses = "401 Van Ness Ave, San Francisco, CA 94102, USA"
    supplier.warehouse_coordinates = get_coordinates_as_dict(supplier.warehouse_addresses)
    supplier.save()
    print(f"Updated Warehouse Address: {supplier.warehouse_addresses}")

    # Attempt to add invalid field
    try:
        supplier.owner = "Steve Rogers"
    except ValueError as e:
        print(f"Error: {e}")


 
    # PROJECT 2
    # Run queries Q1, Q2, etc. and display them
    #TODO
    #Example
    #Q1_r = MyModel.aggregate(Q1)

