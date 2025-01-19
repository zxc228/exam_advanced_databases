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
        geolocator = Nominatim(user_agent=letters_array, timeout=10)
        try:
            #DONE
            # It is You need to provide a user_agent to use the API
            # Use a random name for the user_agent
            location = geolocator.geocode(address)
        except GeocoderTimedOut:
            
            # May throw an exception if the timeout occurs
            # Try again
            print("GeocoderTimedOut: Retrying...")
            time.sleep(1)
        
    #DONE
    if location:
        point = Point((location.longitude, location.latitude))
        return point
    else:
        raise ValueError('Location not found')
        

    



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

    Attributes
    ----------
    required_vars : set[str]
    set of variables required by the model
    admissible_vars : set[str]
    set of variables allowed by the model
    db : pymongo.collection.Collection
    connection to the database collection

    Methods
    -------
    __setattr__(name: str, value: str | dict) -> None
    Overrides the method for assigning values ​​to the object's
    variables in order to control which variables are assigned to the model and when they are modified.
    save() -> None
    Saves the model to the database
    delete() -> None
    Deletes the model from the database
    find(filter: dict[str, str | dict]) -> ModelCursor
    Performs a read query on the database.
    Returns a ModelCursor model cursor
    aggregate(pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor
    Returns the result of an aggregate query.
    find_by_id(id: str) -> dict | None
    Searches for a document by its id using the cache and returns it.
    If the document is not found, returns None.
    init_class(db_collection: pymongo.collection.Collection, required_vars: set[str], admissible_vars: set[str]) -> None
    Initializes class variables at system initialization.

    """
    required_vars: set[str]
    admissible_vars: set[str]
    db: Collection

    def __init__(self, **kwargs: dict[str, str | dict]):
        """
        Initializes the model with the values ​​provided in kwargs
        Checks that the values ​​provided in kwargs are supported
        by the model and that the required variables are provided.

        Parameters
        ----------
        kwargs : dict[str, str | dict]
        dictionary with the values ​​of the model variables
        """
        #DONE
        # Perform the necessary checks and actions
        # before the assignment.
        allowed_vars = self.required_vars | self.admissible_vars | {"_id"}

        missing_vars = self.required_vars - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
        
        invalid_vars = set(kwargs.keys()) - allowed_vars
        if invalid_vars:
            raise ValueError(f'Invalid fields provided: {invalid_vars}')
        
        # Assign all the values ​​in kwargs to the variables with
        # the name of the keys in kwargs
        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: str | dict) -> None:
        """ Override the method for assigning values ​​to the
        object's variables in order to control the variables that are assigned to the
        model and when they are modified. """
        #DONE
        if name != "_id" and name not in self.required_vars and name not in self.admissible_vars:
            raise ValueError(f'Invalid field provided: {name}')
        # Perform the necessary checks and actions
        # before the assignment.

        # Assign the value value to the variable name
        self. __dict__[name] = value

    def save(self) -> None:
        """
        Save the model in the database
        If the model does not exist in the database, a new document is created
        with the model values. Otherwise, the existing document is updated with the new
        model values.
        """
        #DONE
        if not hasattr(self, '_id'):
            result = self.db.insert_one(self.__dict__)
            self._id = result.inserted_id
        else:
            update_data = {key: value for key, value in self.__dict__.items() if key != '_id'}
            self.db.update_one({'_id': self._id}, {'$set': update_data})

    def delete(self) -> None:
        """
        Delete the model from the database
        """
        #DONE

        if hasattr(self, '_id'):
            self.db.delete_one({'_id': self._id})
        else:
            raise ValueError('Document does not exist in the database')
        pass
        
    @classmethod
    def find(cls, filter: dict[str, str | dict]) -> Any:
        """
        Uses the pymongo find method to perform a read query
        in the database.
        find must return a ModelCursor model cursor

        Parameters
        ----------
        filter : dict[str, str | dict]
        dictionary with the search criteria of the query
        Returns
        -------
        ModelCursor
        model cursor
        """
        #DONE
        cursor = cls.db.find(filter)
        # cls is the pointer to the class
        return ModelCursor(cls, cursor)

    @classmethod
    def aggregate(cls, pipeline: list[dict]) -> Cursor:
        """
        Returns the result of an aggregate query.
        There is nothing to do in this function.
        It will be used for the queries requested
        in the second project of the practice.

        Parameters
        ----------
        pipeline : list[dict]
        list of stages of the aggregate query
        Returns
        -------
        pymongo.command_cursor.CommandCursor
        pymongo cursor with the query result
        """
        return cls.db.aggregate(pipeline)

    @classmethod
    def find_by_id(cls, id: str) -> Self | None:
        """
        DO NOT IMPLEMENT UNTIL THIRD PROJECT
        Search for a document by its id using the cache and return it.
        If the document is not found, return None.

        Parameters
        ----------
        id : str
        id of the document to search
        Returns
        -------
        Self | None
        Model of the found document or None if not found
        """
        #TODO
        pass

    @classmethod
    def init_class(cls, db_collection: pymongo.collection.Collection, required_vars: set[str], admissible_vars: set[str]) -> None:
        """
        Initializes the class variables at system initialization.
        In principle, nothing to do here unless you want to perform
        some other initialization/checks or additional changes.

        Parameters
        ----------
        db_collection : pymongo.collection.Collection
        Connection to the database collection.
        required_vars : set[str]
        Set of variables required by the model
        admissible_vars : set[str]
        Set of variables allowed by the model
        """
        cls.db = db_collection
        cls.required_vars = required_vars
        cls.admissible_vars = admissible_vars

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
        globals()[model_name].init_class(db_collection=db[model_name], required_vars=required_vars, admissible_vars=admissible_vars)

# # TODO
# # PROJECT 2
# # Store the query pipelines in Q1, Q2, etc.
# # EXAMPLE
# # Q0: List of all people with a given name
# name = "Quijote"
# Q0 = [{'$match': {'name': name}}]

# # Q1:
# Q2 = []

# # Q2:
# Q2 = []

# # Q3:
# Q3 = []

# # Q4: etc.

if __name__ == '__main__':
    
    # PROJECT 1
    print("\nInitializing models from models_product.yml...")

    # #for local use

    initApp(definitions_path="./models_product.yml", 
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
            coordinates_billing_adresses = getLocationPoint(elem['billing_addresses']),
            registration_date=elem['registration_date'],
            shipping_addresses=elem['shipping_addresses'],
            coordinates_shipping_adresses = getLocationPoint(elem['shipping_addresses']),
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
            shipping_coordinates=getLocationPoint(elem['shipping_address'])
        )
        purchase.save()

    for elem in data['suppliers']:
        supplier = Supplier(
            name=elem['name'],
            warehouse_addresses=elem['warehouse_addresses'],
            warehouse_coordinates=getLocationPoint(elem['warehouse_addresses'])
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
        coordinates_billing_adresses=getLocationPoint("1600 Pennsylvania Ave NW, Washington, DC 20500, USA"), 
        payment_cards="4111111111111111",
        last_access_date="2024-10-01"
    )
    customer.save()
    print(f"Created Customer: {customer.name}, Billing Address: {customer.billing_addresses}")

    # Update and verify
    address_billing = "United Nations Secretariat Building, 405 E 42nd St, New York, NY 10017, USA"
    customer.billing_addresses = address_billing
    customer.coordinates_billing_adresses = getLocationPoint(customer.billing_addresses)
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
        warehouse_coordinates=getLocationPoint("701 D St NW, Washington, DC 20024, USA")
    )
    supplier.save()
    print(f"Created Supplier: {supplier.name}, Warehouse: {supplier.warehouse_addresses}")

    # Update and verify
    
    supplier.warehouse_addresses = "401 Van Ness Ave, San Francisco, CA 94102, USA"
    supplier.warehouse_coordinates = getLocationPoint(supplier.warehouse_addresses)
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

