# SE-4348-Project-2

- 2nd Project of this Class

- Name: Tobenna Nwosu
- Class & Section: SE 4348.504

- IDE: VS Code
- Programming Language: Python 3.11

## Files



- `bank.py` — Main program.

  - Creates semaphores, events, and counters.
  - Instantiates and starts `Teller` (3 of them) and `Customer` (50 of them) threads.
  - Initializes the logging system (`log_writer.py`) and clears `log.txt` when the bank opens.
  - Waits for the bank simulation to finish and closes the log.

- `teller.py` — `Teller` thread class.

  - Represents a teller that waits for customers, requests manager approval for withdrawals,
    and accesses a shared safe (limited concurrent access).
  - Uses semaphores to interact with a customer.
  - Sends all output via the logger.

- `customer.py` — `Customer` thread class.

  - Represents a customer who waits for the bank to open, enters (only 2 customers are allowed),
    selects an available teller, and performs either a deposit or withdrawal.
  - Sends all output via the logger.

- `log_writer.py` — file logger.

  - `init(path)` opens the log file.
  - `log(msg)` appends a line to txt file.
  - `clear()` clears file, when the bank opens an existing `log.txt`.
  - `close()` closes the log file.



## Instructions

- It's pretty easy! If you are using VS Code, you can simply just click on the ▶ Icon to run it.
    - If not, make your to the directory containing `bank.py`. Then in the terminal, simply enter `python bank.py`, and you should be good to go. 
- Only a few outputs appear in the terminal, while the majority are in a new or existing `log.txt`.
    - I'll provide my own `log.txt` as a sample!

