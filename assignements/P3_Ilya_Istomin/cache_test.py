import redis
from ODM import ModelCursor
import json

# Redis settings for the cache (db=0)
cache_db = redis.Redis(host='localhost', port=6379, db=0)

# Initialize cache for models in ODM
from ODM import Model
Model.initialize_cache(cache_db)

# Initialize models and save them in a dictionary
definitions_path = "./models_product.yml"
mongodb_uri = "mongodb://localhost:27017/"
db_name = "db1"
models = ModelCursor.initApp(definitions_path=definitions_path, mongodb_uri=mongodb_uri, db_name=db_name)

# Retrieve models
Customer = models.get('Customer')
Product = models.get('Product')
Purchase = models.get('Purchase')
Supplier = models.get('Supplier')

def setup_test_data():
    """Creates test data for all models."""
    print("\nSetting up test data...")
    
    # Clear Redis cache before setting up data
    cache_db.flushdb()
    
    # Create test customers
    test_customers = [
        Customer(name="Test Customer 1", billing_addresses=["Test Address 1"], coordinates_billing_adresses=[], registration_date="2024-01-01"),
        Customer(name="Test Customer 2", billing_addresses=["Test Address 2"], coordinates_billing_adresses=[], registration_date="2024-01-02"),
    ]
    for customer in test_customers:
        customer.save()

    # Create test products
    test_products = [
        Product(name="Test Product 1", supplier_product_code="TP1", price_without_vat=100, price_with_vat=121),
        Product(name="Test Product 2", supplier_product_code="TP2", price_without_vat=50, price_with_vat=60.5),
    ]
    for product in test_products:
        product.save()

    # Create test suppliers
    test_suppliers = [
        Supplier(name="Test Supplier 1"),
        Supplier(name="Test Supplier 2"),
    ]
    for supplier in test_suppliers:
        supplier.save()

    # Create test purchases
    test_purchases = [
        Purchase(products=["Test Product 1"], customer="Test Customer 1", purchase_price=110, purchase_date="2024-01-10"),
        Purchase(products=["Test Product 2"], customer="Test Customer 2", purchase_price=60, purchase_date="2024-01-11"),
    ]
    for purchase in test_purchases:
        purchase.save()

def cleanup_test_data():
    """Removes all test data."""
    print("\nCleaning up test data...")
    
    # Delete only test data from database
    Customer.db.delete_many({"name": {"$regex": "^Test"}})
    Product.db.delete_many({"name": {"$regex": "^Test"}})
    Supplier.db.delete_many({"name": {"$regex": "^Test"}})
    Purchase.db.delete_many({"purchase_date": {"$regex": "^2024-01"}})

    # Clear Redis cache
    cache_db.flushdb()

def test_cache_behavior():
    """Runs tests for cache behavior across all models."""
    print("\nRunning cache behavior tests...")

    # Test Customer model
    print("\nTesting Customer model:")
    customers = Customer.find({"name": {"$regex": "^Test Customer"}})
    print(f"Number of customers retrieved: {len(customers)}")
    assert len(customers) == 2, "Expected 2 customers"

    # Generate cache key the same way it is generated in the find method
    filter_key = {"name": {"$regex": "^Test Customer"}}
    cache_key = f"find:{json.dumps(filter_key, sort_keys=True)}"
    assert cache_db.exists(cache_key), "Customer query should be cached"

    # Update a customer and invalidate cache
    customer = customers[0]
    customer_instance = Customer(**customer)
    customer_instance.registration_date = "2024-02-01"
    customer_instance.save()
    assert not cache_db.exists(cache_key), "Customer cache should be invalidated after update"

    # Test Product model
    print("\nTesting Product model:")
    products = Product.find({"name": {"$regex": "^Test Product"}})
    print(f"Number of products retrieved: {len(products)}")
    assert len(products) == 2, "Expected 2 products"

    cache_key = f"find:{json.dumps({'name': {'$regex': '^Test Product'}}, sort_keys=True)}"
    assert cache_db.exists(cache_key), "Product query should be cached"

    # Delete a product and check cache invalidation
    product = products[0]
    product_instance = Product(**product)
    product_instance.delete()
    assert not cache_db.exists(cache_key), "Product cache should be invalidated after delete"

    # Test Purchase model
    print("\nTesting Purchase model:")
    purchases = Purchase.find({"purchase_date": {"$regex": "^2024-01"}})
    print(f"Number of purchases retrieved: {len(purchases)}")
    assert len(purchases) == 2, "Expected 2 purchases"

    cache_key = f"find:{json.dumps({'purchase_date': {'$regex': '^2024-01'}}, sort_keys=True)}"
    assert cache_db.exists(cache_key), "Purchase query should be cached"

    # Delete a purchase and check cache invalidation
    purchase = purchases[0]
    purchase_instance = Purchase(**purchase)
    purchase_instance.delete()
    assert not cache_db.exists(cache_key), "Purchase cache should be invalidated after delete"

    # Test Supplier model
    print("\nTesting Supplier model:")
    suppliers = Supplier.find({"name": {"$regex": "^Test Supplier"}})
    print(f"Number of suppliers retrieved: {len(suppliers)}")
    assert len(suppliers) == 2, "Expected 2 suppliers"

    cache_key = f"find:{json.dumps({'name': {'$regex': '^Test Supplier'}}, sort_keys=True)}"
    assert cache_db.exists(cache_key), "Supplier query should be cached"

    # Delete a supplier and check cache invalidation
    supplier = suppliers[0]
    supplier_instance = Supplier(**supplier)
    supplier_instance.delete()
    assert not cache_db.exists(cache_key), "Supplier cache should be invalidated after delete"

def test_intersecting_queries():
    """Test cache behavior with intersecting queries."""
    print("\nTesting intersecting queries...")

    # Step 1: Create test data
    customer_1 = Customer(name="Test1", billing_addresses=["Address1"], coordinates_billing_adresses=[], registration_date="2024-01-01")
    customer_2 = Customer(name="Test2", billing_addresses=["Address2"], coordinates_billing_adresses=[], registration_date="2024-01-02")
    customer_3 = Customer(name="Test3", billing_addresses=["Address3"], coordinates_billing_adresses=[], registration_date="2024-01-03")
    customer_4 = Customer(name="Test4", billing_addresses=["Address4"], coordinates_billing_adresses=[], registration_date="2024-01-04")
    
    for customer in [customer_1, customer_2, customer_3, customer_4]:
        customer.save()

    # Step 2: Query and cache two groups
    query_1 = {"name": {"$in": ["Test1", "Test2"]}}
    query_2 = {"name": {"$in": ["Test3", "Test4"]}}

    customers_group_1 = Customer.find(query_1)
    customers_group_2 = Customer.find(query_2)

    # Generate cache keys
    cache_key_1 = f"find:{json.dumps(query_1, sort_keys=True)}"
    cache_key_2 = f"find:{json.dumps(query_2, sort_keys=True)}"

    # Ensure both queries are cached
    assert cache_db.exists(cache_key_1), "Query 1 should be cached"
    assert cache_db.exists(cache_key_2), "Query 2 should be cached"

    # Step 3: Update Test4 and invalidate its cache
    customer_to_update = customers_group_2[1]  # This should be Test4
    customer_instance = Customer(**customer_to_update)
    customer_instance.registration_date = "2024-05-01"
    customer_instance.save()

    # Step 4: Verify cache state
    assert cache_db.exists(cache_key_1), "Query 1 should still be cached"
    assert not cache_db.exists(cache_key_2), "Query 2 should have been invalidated"

    print("Intersecting queries test passed successfully.")

def test_complex_cache_behavior():
    """Test complex cache interactions with multiple intersecting queries."""
    print("\nTesting complex cache behavior...")

    # Step 1: Create test data
    customer_1 = Customer(name="Test1", billing_addresses=["Address1"], coordinates_billing_adresses=[], registration_date="2024-01-01")
    customer_2 = Customer(name="Test2", billing_addresses=["Address2"], coordinates_billing_adresses=[], registration_date="2024-01-02")
    customer_3 = Customer(name="Test3", billing_addresses=["Address3"], coordinates_billing_adresses=[], registration_date="2024-01-03")
    customer_4 = Customer(name="Test4", billing_addresses=["Address4"], coordinates_billing_adresses=[], registration_date="2024-01-04")
    
    for customer in [customer_1, customer_2, customer_3, customer_4]:
        customer.save()

    # Step 2: Query two overlapping groups
    query_all = {"name": {"$in": ["Test1", "Test2", "Test3", "Test4"]}}
    query_subset = {"name": {"$in": ["Test2", "Test3"]}}

    customers_all = Customer.find(query_all)
    customers_subset = Customer.find(query_subset)

    # Generate cache keys
    cache_key_all = f"find:{json.dumps(query_all, sort_keys=True)}"
    cache_key_subset = f"find:{json.dumps(query_subset, sort_keys=True)}"

    # Ensure both queries are cached
    assert cache_db.exists(cache_key_all), "Query covering all customers should be cached"
    assert cache_db.exists(cache_key_subset), "Subset query should be cached"

    # Step 3: Modify Test2 and check invalidation
    customer_to_update = customers_subset[0]  # This should be Test2
    customer_instance = Customer(**customer_to_update)
    customer_instance.registration_date = "2024-05-01"
    customer_instance.save()

    # Check cache state
    assert not cache_db.exists(cache_key_all), "Query covering all customers should have been invalidated"
    assert not cache_db.exists(cache_key_subset), "Subset query should have been invalidated"

    # Step 4: Add a new customer and check cache
    new_customer = Customer(name="Test5", billing_addresses=["Address5"], coordinates_billing_adresses=[], registration_date="2024-06-01")
    new_customer.save()

    # Re-query and cache
    customers_all = Customer.find(query_all)
    cache_key_all = f"find:{json.dumps(query_all, sort_keys=True)}"
    assert cache_db.exists(cache_key_all), "Query covering all customers should be cached after re-query"

    # Step 5: Delete Test4 and verify cache invalidation
    customer_to_delete = customers_subset[1]  # This should be Test3
    customer_instance = Customer(**customer_to_delete)
    customer_instance.delete()

    # Verify cache state after deletion
    assert not cache_db.exists(cache_key_all), "Query covering all customers should have been invalidated after deletion"
    print("Complex cache behavior test passed successfully.")

if __name__ == "__main__":
    try:
        setup_test_data()
        test_cache_behavior()
        test_intersecting_queries()
        test_complex_cache_behavior()
    finally:
        cleanup_test_data()