# Ex2 (Chapter2): To do list
File contains script which implements basic task list **with text interface**. Database contain: **hash id**, **name of task**, **deadline** and **description**.

It is necessary to change path in file (ex2_database.py) and run it.
Next stage is to change path and run via console ex2.py:
*python ex2.py --type [add|update|list|remove]*

In **add** parse, **--name** argument is obligatory (str), but --deadline (in format DDMMYYYY) and --description (str) are optional. Script return hash id (MD5: calculating by concatenate name+deadline+description), if adding to database has been made successfully.

*python ex2.py --type add --name Send a mail --description Post office*

Returned value: eba1a42c2412faacc98f386716d25998

In **update** parse, **--task_hash** is necessary to be types (in database, id is primary key). --name, --deadline, --description are optional argument. Type what you want to change in database, eg.

*python ex2.py --type update --description Car cleaning --deadline 16032020 --task_hash 5ff64bccdd09d2c6a66149191d20d6a0*

In such case, it doesn't effect name value in database. It will change MD5 hash and return updated value.

In **--remove**, it is necessary to type **--task_hash**, eg.

*python ex2.py --type remove --task_hash 5ff64bccdd09d2c6a66149191d20d6a0*

In **--list**, it is obligatory to set **--[all|today]**. 
First returned column is hash id, second name of task, third deadline and forth description. 

*python ex2.py --type list --today*

In case of trouble, there is also --help option.
