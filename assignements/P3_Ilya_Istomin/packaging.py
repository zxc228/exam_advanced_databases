import redis
import threading
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(message)s')

# Connecting to Redis
packaging_queue = redis.Redis(host='localhost', port=6379, db=1)

# Maximum number of threads
MAX_THREADS = 5
semaphore = threading.Semaphore(MAX_THREADS)
active_threads = 0
lock = threading.Lock()  # Synchronization for the thread counter

# Global variable to track if the main thread is waiting
main_thread_waiting = True

def enqueue_purchase(purchase_id):
    """Adds a purchase to the packaging queue"""
    packaging_queue.lpush("packaging_queue", purchase_id)

def get_next_purchase(timeout=10):
    """Gets the next purchase from the packaging queue with blocking."""
    purchase = packaging_queue.blpop("packaging_queue", timeout=timeout)  # Using blpop to handle blocking
    if purchase:
        return purchase[1].decode("utf-8")  # Decode bytes to string
    return None

def packaging(purchase_id, thread_id, sleep_duration=60):
    """Performs the packaging task"""
    logging.info(f"Starting packaging for purchase {purchase_id} in thread {thread_id}")
    time.sleep(sleep_duration)  # Simulate packaging time
    logging.info(f"Finished packaging for purchase {purchase_id} in thread {thread_id}")

class PackagingThread(threading.Thread):
    def __init__(self, main_thread=False):
        super().__init__()
        self.main_thread = main_thread

    def run(self):
        global active_threads
        thread_id = threading.get_ident()

        # Increment active thread counter
        with lock:
            active_threads += 1

        try:
            while True:
                logging.info(f"Thread {thread_id} is waiting for a new task.")

                # Use blpop to wait for a task with timeout
                purchase_id = get_next_purchase(timeout=None if self.main_thread else 10)

                if purchase_id:
                    # Create a new thread for waiting if it's the main thread
                    if self.main_thread:
                        with lock:
                            logging.info(f"Main thread {thread_id} creates a child thread for waiting.")
                            observer_thread = PackagingThread(main_thread=False)
                            observer_thread.start()

                    else:
                        # For child threads, create another child thread if active_threads < MAX_THREADS
                        with lock:
                            if active_threads < MAX_THREADS:
                                logging.info(f"Thread {thread_id} creates another child thread for waiting.")
                                observer_thread = PackagingThread(main_thread=False)
                                observer_thread.start()

                    # Perform the packaging task
                    with semaphore:
                        packaging(purchase_id, thread_id)

                    # If this is a child thread, continue waiting for a new task
                    if not self.main_thread:
                        logging.info(f"Thread {thread_id} completed its task. Waiting for a new task.")
                        continue
                else:
                    # Terminate the child thread if no task is received within timeout
                    if not self.main_thread:
                        logging.info(f"Thread {thread_id} is terminating due to timeout.")
                        break
                    else:
                        # Main thread should never terminate, continue waiting
                        logging.info(f"Main thread {thread_id} is still waiting.")
        finally:
            # Decrement active thread counter
            with lock:
                active_threads -= 1
                logging.info(f"Thread {thread_id} has terminated. Active threads: {active_threads}")

def start_packaging_system():
    """Starts the main thread for the packaging system"""
    main_thread = PackagingThread(main_thread=True)
    main_thread.start()

if __name__ == "__main__":
    # Clear the queue before starting the test
    packaging_queue.delete("packaging_queue")

    # Add test data (8 purchases)
    test_purchases = ["purchase_1", "purchase_2", "purchase_3", "purchase_4", "purchase_5", "purchase_6", "purchase_7", "purchase_8"]
    for purchase in test_purchases:
        enqueue_purchase(purchase)
        logging.info(f"Purchase {purchase} added to the queue.")

    # Start the packaging system
    logging.info("Starting the packaging system...")
    start_packaging_system()