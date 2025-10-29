import threading
import time
import random
import queue


# Customer class representing a bank customer thread
class Customer(threading.Thread):
    def __init__(self, customer_id, # Customer ID
                 bank_opening_event, bank_door_semaphore, # Semaphore for bank door access and bank opening event
                 available_tellers_semaphore, teller_queue, # Semaphore for available tellers and queue of tellers
                 customer_served_counter, customer_served_counter_lock, # Counter for customers served and its lock
                 bank_closing_event, # Event to signal bank closing
                 TOTAL_CUSTOMERS, logger): # Total number of customers to be served
        
        super().__init__()

        self.customer_id = customer_id

        # Random transaction type: either 'deposit' or 'withdraw'
        self.transaction_type = random.choice(['deposit', 'withdraw'])
        self.assigned_bank_teller = None

        self.bank_opening_event = bank_opening_event
        self.bank_door_semaphore = bank_door_semaphore
        self.available_tellers_semaphore = available_tellers_semaphore
        self.teller_queue = teller_queue
        self.customer_served_counter = customer_served_counter
        self.customer_served_counter_lock = customer_served_counter_lock
        self.bank_closing_event = bank_closing_event
        self.TOTAL_CUSTOMERS = TOTAL_CUSTOMERS
        
        # Logger function (callable)
        self.logger = logger

    # Output regarding the customer actions with a teller
    def output(self, msg):
        text = f"Customer {self.customer_id}"
        if self.assigned_bank_teller is not None:
            text += f" [Teller {self.assigned_bank_teller.teller_id}]: {msg}"
        else:
            text += f": {msg}"
        # Use logger
        if hasattr(self, 'logger') and self.logger:
            try:
                self.logger(text)
            except Exception:
                print(text)
        else:
            print(text)

    
    # Main logic for the customer thread
    def run(self):
        # Customer waits 0-100 ms before entering the bank
        time.sleep(random.uniform(0, 0.1))
        
        # Customer's desired transaction type
        self.output(f"wants to {self.transaction_type} money.")

        # Wait for the bank to open
        self.bank_opening_event.wait()

        # Check if bank is already closing
        with self.customer_served_counter_lock:
            if self.customer_served_counter[0] >= self.TOTAL_CUSTOMERS:
                return

        # Enter the bank (only 2 customers can enter at a time)
        self.output("is waiting to enter the bank.")
        with self.bank_door_semaphore:
            self.output("has entered the bank.")

            # Wait for an available teller
            self.output("is waiting for an available teller.")
            self.available_tellers_semaphore.acquire()
            self.output("found an available teller.")

            try:
                # Get an available teller from the queue with timeout
                self.assigned_bank_teller = self.teller_queue.get(timeout=5)
                self.output(f"chooses Teller {self.assigned_bank_teller.teller_id}.")
            except queue.Empty:
                # If we can't get a teller, release the semaphore we acquired
                self.available_tellers_semaphore.release()
                return  # Exit without incrementing served counter

            # Signal teller that customer is assigned
            self.assigned_bank_teller.customer_assigned_semaphore.release()

            # Provide customer ID to teller (Same as giving an introduction to the teller)
            self.assigned_bank_teller.current_customer_id = self.customer_id
            self.output("is providing their customer ID to the teller.")

            try:
                # Signal teller that customer ID is provided
                self.assigned_bank_teller.customer_id_received_semaphore.release()

                # Wait for teller to signal readiness for the transaction type (with timeout)
                if not self.assigned_bank_teller.teller_ready_for_transaction_semaphore.acquire(timeout=5):
                    self.output("Teller not responding - leaving")
                    return

                # Provide the transaction type to the teller
                self.assigned_bank_teller.current_transaction = self.transaction_type
                self.output(f"is telling teller to {self.transaction_type}.")

                # Signal teller that transaction type is provided
                self.assigned_bank_teller.transaction_type_received_semaphore.release()

                # Wait for teller to complete transaction (with timeout)
                if not self.assigned_bank_teller.transaction_complete_semaphore.acquire(timeout=10):
                    self.output("Transaction taking too long - leaving")
                    return

                self.output(f"Transaction completed.")
            except Exception as e:
                self.output(f"Error during transaction: {str(e)}")
                return

            # Customer leaves the teller
            self.output("is leaving the teller.")

            # Signal teller that customer has left (freeing up the teller)
            self.assigned_bank_teller.customer_left_semaphore.release()

        # Customer leaves the bank
        self.output("has left the bank.")

        # Increment the served customer counter
        with self.customer_served_counter_lock:
            self.customer_served_counter[0] += 1
            count = self.customer_served_counter[0]

        # Check if all customers have been served (all 50 of them)
        if count == self.TOTAL_CUSTOMERS:
            self.output("All customers have been served. Bank is closing now.")

            # Signal bank closing event to safely exit
            self.bank_closing_event.set()

