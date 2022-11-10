# point_tracker
Flask API that lets you add points and delete them in a client-customizable order.

### Quickstart
 1. Clone git repository
 2. Setup the python environment
	 - Install python3
	- `python -m venv env` to create a new environment (called 'env' here)
	- `source env/bin/activate` to enter the virtual environment
	- `pip install -r requirements.txt` to install the needed requirements
3.  Run the server by running app.py (set debug flag to True in the last line to auto-reload code changes)

### API routes
#### 1. Add transactions
	POST /transactions
	JSON data:  { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
#### 2. Spend points
	POST /expense
	JSON data:  { "points": 5000 }
#### 3. Return payer balances
	GET /balance

### A Note On Efficiency
The transactions are kept in a heap, which allows for efficient removal when we make the spend call. We keep a master-heap for this purpose and payer-specific heaps for negative transactions (to take away oldest transactions belonging to a specific payer)

Both those heaps use lazy deletion so that removal (diiferent from pop) is more efficient as well
	 
