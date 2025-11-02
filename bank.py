import threading
import queue
from teller import Teller
from customer import Customer
import log_writer

def main():

    # Constraints on tellers and customers
    MAX_TELLERS = 3
    MAX_CUSTOMERS_IN_BANK = 50

    # For Tellers only:

    manager_semaphore = threading.Semaphore(1)  # Semaphore for manager access to the safe
    safe_semaphore = threading.Semaphore(2)     # Semaphore for safe access (only 2 at a time)

    # For Bank Opening Sequence:
    bank_opening_event = threading.Event()      # Event to signal bank opening

    # Counter for tellers ready
    teller_ready_counter = [0]
    teller_ready_counter_lock = threading.Lock()

    # For Customers and Tellers:

        # Semaphore for customers to wait for a freed teller
    available_tellers_semaphore = threading.Semaphore(0)
        # Queue to hold available tellers objects (buffer size = number of tellers)
    ready_teller_queue = queue.Queue(maxsize=MAX_TELLERS)

    # For Customers:
        # Semaphore for bank door access (max 2 customers inside at a time)
    bank_door_semaphore = threading.Semaphore(2)

    # Counter for customers served
    customer_served_counter = [0]
    customer_served_counter_lock = threading.Lock()

    # Event to signal bank closing (waits on the last customer to be served)
    bank_closing_event = threading.Event()


    # Initialize logger (will be cleared when bank opens by the tellers)
    log_writer.init('log.txt')

    # Now, we create instances of Tellers
    tellers = []

    for i in range(MAX_TELLERS):
        teller = Teller(teller_id=i,
                        manager_semaphore=manager_semaphore,
                        safe_semaphore=safe_semaphore,
                        bank_opening_event=bank_opening_event,
                        teller_ready_counter=teller_ready_counter,
                        teller_ready_counter_lock=teller_ready_counter_lock,
                        available_tellers_semaphore=available_tellers_semaphore,
                        teller_queue=ready_teller_queue,
                        num_tellers=MAX_TELLERS,
                        logger=log_writer.log,
                        logger_clear=log_writer.clear,
                        customer_served_counter=customer_served_counter,
                        customer_served_counter_lock=customer_served_counter_lock,
                        TOTAL_CUSTOMERS=MAX_CUSTOMERS_IN_BANK
                        )
        tellers.append(teller)

    # Create instances of Customers
    customers = []

    for i in range(MAX_CUSTOMERS_IN_BANK):
        customer = Customer(customer_id=i,
                            bank_opening_event=bank_opening_event,
                            bank_door_semaphore=bank_door_semaphore,
                            available_tellers_semaphore=available_tellers_semaphore,
                            teller_queue=ready_teller_queue,
                            customer_served_counter=customer_served_counter,
                            customer_served_counter_lock=customer_served_counter_lock,
                            bank_closing_event=bank_closing_event,
                            logger=log_writer.log,
                            TOTAL_CUSTOMERS=MAX_CUSTOMERS_IN_BANK
                            )
        customers.append(customer)


    # Start all teller threads
    for teller in tellers:
        teller.start()

    # Start all customer threads
    for customer in customers:
        customer.start()

    # Wait for all customer threads to finish (last customer is served)
    log_writer.log("\nWaiting for customers to finish...")
    print("\nWaiting for customers to finish...")
    bank_closing_event.wait()

    log_writer.log("\nBank is now closing. All customers have been served.")
    print("\nBank is now closing. All customers have been served.")

    # Wake up any idle tellers who are stuck waiting (so they can exit cleanly)
    log_writer.log("Waking up any idle tellers...")
    print("Waking up any idle tellers...")
    for _ in range(MAX_TELLERS):
        try:
            # Check if a teller is actually waiting on the semaphore
            if not available_tellers_semaphore.acquire(blocking=False):
                # No tellers were waiting, so we can stop!!!
                break

            # If we acquired, a teller is waiting. Retrieve the teller from the queue.
            teller = ready_teller_queue.get(block=False)
            
            # Send the "wake up" signal. This releases the teller
            teller.customer_assigned_semaphore.release()

        except queue.Empty:
            log_writer.log("Cleanup loop found an empty queue, stopping.")
            print("Cleanup loop found an empty queue, stopping.")
            break


    log_writer.log("Waiting for tellers to finish...")
    print("Waiting for tellers to finish...")
    
    # now join without timeouts.
    for teller in tellers:
        teller.join()

    log_writer.log("Waiting for remaining customers to exit...")
    print("Waiting for remaining customers to exit...")
    for customer in customers:
        customer.join()

    # Final log message (bank is closed once all tellers and customers have exited)
    log_writer.log("Bank closed.")
    print("Bank closed.")

    # Close the log file
    log_writer.close()

if __name__ == "__main__":
    main()