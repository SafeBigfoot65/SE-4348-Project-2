import threading
import time
import random

# Teller class representing a bank teller thread
class Teller (threading.Thread):
    def __init__(self, teller_id, # Teller ID
                 manager_semaphore, safe_semaphore, # Semaphore for manager access to safe and safe access
                 bank_opening_event, teller_ready_counter, # Counter for ready tellers and bank opening event
                 teller_ready_counter_lock, available_tellers_semaphore, # Semaphore to signal available tellers
                 customer_served_counter, customer_served_counter_lock, # Counter for customers served by this teller
                 TOTAL_CUSTOMERS): #Total number of customers to be served (50 max)
        
        super().__init__()

        self.teller_id = teller_id
        self.current_customer_id = None
        # Either 'deposit' or 'withdraw'
        self.current_transaction = None

        self.manager_semaphore = manager_semaphore
        self.safe_semaphore = safe_semaphore
        self.bank_opening_event = bank_opening_event
        self.teller_ready_counter = teller_ready_counter
        self.teller_ready_counter_lock = teller_ready_counter_lock
        self.available_tellers_semaphore = available_tellers_semaphore
        self.customer_served_counter = customer_served_counter
        self.customer_served_counter_lock = customer_served_counter_lock
        self.TOTAL_CUSTOMERS = TOTAL_CUSTOMERS

        # Customer signals to be assigned to this teller
        self.customer_assigned_semaphore = threading.Semaphore(0)

        # Customer signals after giving their customer ID
        self.customer_id_received_semaphore = threading.Semaphore(0)

        # Customer signals after giving their transaction type
        self.transaction_type_received_semaphore = threading.Semaphore(0)

        # Teller signals after completing the transaction
        self.transaction_complete_semaphore = threading.Semaphore(0)

        # Customer signals after leaving the teller
        self.customer_left_semaphore = threading.Semaphore(0)

        # Output regarding the teller actions on a customer or manager
        def output(self, msg):
            
            if self.current_customer_id is not None:
                print(f"Teller{self.teller_id} [Customer {self.current_customer_id}]: {msg}")
            else:
                print(f"Teller{self.teller_id} [Manager]: {msg}")

        
        def run(self):
            # Main logic for the teller thread

            # Log that the teller is ready
            self.output("is ready for customers.")

            with self.teller_ready_counter_lock:
                self.teller_ready_counter[0] += 1
                count = self.teller_ready_counter[0]

            if count == 3:
                print("All tellers are ready. Bank is now open.")


            # Teller Service Loop

            while True:
                # Check if all customers have been served (all 50 of them)
                with self.customer_served_counter_lock:
                    if self.customer_served_counter[0] == self.TOTAL_CUSTOMERS:
                        break

                # else, serve the next customer
                self.serve_customer()

            # If all customers have been served, log that the teller is closing
            self.output("has served all customers and is closing for the day.")

    # Serve the next customer
    def serve_customer(self):
        # Announce availability
        self.output("is available for the next customer.")

        # add teller to a queue of available tellers
        self.queue_available_teller().put(self)
        # Signal that a teller is available for a customer
        self.available_tellers_semaphore.release()

        # Wait for a customer to be assigned
        self.customer_assigned_semaphore.acquire()

        # ask for customer ID
        self.output("is requesting customer ID.")
        self.customer_id_received_semaphore.acquire()
        self.output(f"received customer ID")

        # ask for transaction type
        self.output("is requesting transaction type.")
        self.teller_ready_for_transaction_semaphore.release()
        
        # Wait for the transaction type to be received
        self.transaction_type_received_semaphore.acquire()
        self.output(f"received transaction type: {self.current_transaction}")

        # Process the transaction
        if self.current_transaction == 'withdraw':
            self.ask_manager_for_withdrawal()

        # go to safe for deposit or after manager approval for withdrawal
        self.go_to_safe()

        # Complete the transaction
        self.output("Transaction complete.")
        self.transaction_complete_semaphore.release()

        # Wait for the customer to leave
        self.customer_left_semaphore.acquire()
        self.output("Customer has left.")

        # Reset current customer info
        self.current_customer_id = None
        self.current_transaction = None

    def ask_manager_for_withdrawal(self):
        # Request manager approval for withdrawal
        self.output("is going to see the manager for withdrawal approval.")

        with self.manager_semaphore:
            self.output("is with the manager for withdrawal approval.")
            time.sleep(random.uniform(0.005, 0.030))  # Random duration between 5ms and 30ms
            self.output("received withdrawal approval from the manager.")

    def go_to_safe(self):
        # Access the safe for deposit or withdrawal
        self.output("is going to the safe.")

        with self.safe_semaphore:
            self.output("is at the safe.")
            time.sleep(random.uniform(0.010, 0.050))  # Random duration between 10ms and 50ms
            self.output(f"finished {self.current_transaction}at the safe.")