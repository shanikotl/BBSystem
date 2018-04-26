# BBSystem


Simulate a production line of Bucket Brigade (BB), when workers work in a line, and can't bypass each other.
Items arrive by a stochasic process (each item has it's own lambda rate).

Items -
Item is divided into tasks per station (Q1, Q2,...), and amount of units per task.
for example, Q1 can be "adding a pocket", and number of working units is 3.
It means that in the first station, worker will need to add 3 pockets to the item.

workers -
each worker had the capacity for each kind of task.
for example - for the first worker it takes 4 hours to accomplish 1 pocket,
while for the second worker it will take 2 house.

You can run the code by running the file run_process.py
The function init_production_line in system_dynamics.py defines the initial state of the system.
In CONFIG file you can find the items and workers functions.


