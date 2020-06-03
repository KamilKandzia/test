from sqlalchemy import create_engine, insert, select, update, MetaData, Table
import pandas as pd
import argparse
import hashlib
import time

class ParseError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        return 'Error: {0} '.format(self.message)

engine = create_engine('sqlite:///C:\\Users\\Kamil\\Desktop\\test\\database.db', echo=False)
con = engine.connect()

#META_DATA = MetaData(bind=con, reflect=True)
#todolist = META_DATA.tables['todolist']

message = "CLI for to do list. 'add' and 'update' will return new hash id. Database contain 4 columns (id - as primary key, name, deadline and description"

parser = argparse.ArgumentParser(description=message)
#choose type
parser.add_argument('--type', dest='type', choices=['add', 'update', 'remove', 'list'],
                    help="Choose only one of argument")
#for add, update or remove operation
parser.add_argument('--name', dest='NAME', type=str, nargs='*', help="Name is required for add and optional for update operation")
parser.add_argument('--deadline', dest='DEADLINE', type=int, help="Deadline is optional for update and add")
parser.add_argument('--description', dest='DESCRIPTION', type=str, nargs='*', help="Description is optional for update and add")
parser.add_argument('--task_hash', dest='TASK_HASH', type=str, help="Task_hash is required in update and remove")
#for list operation
parser.add_argument('--all', dest='ALL', action='store_true', help="For list parse")
parser.add_argument('--today', dest='TODAY', action='store_true', help="For list parse")

parser.parse_args()
args = parser.parse_args()

if args.type=='add':

    if not args.NAME:
        raise ParseError('name value must be typed')
    else:
        #concatenate NAME+DEADLINE+DESCRIPTION
        string=str(' '.join(args.NAME))+(str(args.DEADLINE) if args.DEADLINE else '')+(str(' '.join(args.DESCRIPTION)) if args.DESCRIPTION else '')
        #calculate hash
        hash_id=hashlib.md5((string).encode('utf-8')).hexdigest()

        query_insertion = "INSERT INTO todolist (id, name"+ (', deadline' if args.DEADLINE else '')+(', description' if args.DESCRIPTION else '') +") VALUES ('" + str(hash_id) +"','"+ str(' '.join(args.NAME))+("','"+str(args.DEADLINE) if args.DEADLINE else '')+("','"+str(' '.join(args.DESCRIPTION)) if args.DESCRIPTION else '')+"')"

        result1 = con.execute(query_insertion)
        con.close()

        print(hash_id)

elif args.type=='update':
    if not args.TASK_HASH:
        raise ParseError('task hash must be typed')

    else:
        result = con.execute("SELECT * FROM todolist WHERE id="+"'"+str(args.TASK_HASH)+"'")
        df=pd.DataFrame(result.fetchall())

        if df.empty:
            raise ParseError('task hash doesnt exist')
        #print(df)

        df_temp=pd.isna(df)
        
        #in case description cell is empty 
        if df_temp[3].bool():
            string=str(' '.join(args.NAME if args.NAME else df[1]))+str(args.DEADLINE if args.DEADLINE else (df[2]))+str(args.DESCRIPTION if args.DESCRIPTION else (df[3]))
        else:
            string=str(' '.join((args.NAME if args.NAME else df[1])))+str(args.DEADLINE if args.DEADLINE else (df[2]))+str(' '.join(args.DESCRIPTION if args.DESCRIPTION else df[3]))
        #calculate hash
        hash_id=hashlib.md5((string).encode('utf-8')).hexdigest()
        #update arguments
        if args.NAME:
            query_update_name = "UPDATE todolist SET name='"+str(' '.join((args.NAME)))+"' where id="+"'"+str(args.TASK_HASH)+"'"
            result = con.execute(query_update_name)

        if args.DEADLINE:
            query_update_deadline = "UPDATE todolist SET deadline='"+str(args.DEADLINE)+"' where id="+"'"+str(args.TASK_HASH)+"'"
            result = con.execute(query_update_deadline)

        if args.DESCRIPTION:
            query_update_description = "UPDATE todolist SET description='"+str(' '.join((args.DESCRIPTION)))+"' where id="+"'"+str(args.TASK_HASH)+"'"
            result = con.execute(query_update_description)
        
        query_update = "UPDATE todolist SET id='"+str(hash_id)+"' where id="+"'"+str(args.TASK_HASH)+"'"
        result = con.execute(query_update)
        con.close()
        print(hash_id)

elif args.type=='remove':
    if not args.TASK_HASH:
        raise ParseError('task hash must be typed')

    else:
        result = con.execute("SELECT * FROM todolist WHERE id="+"'"+str(args.TASK_HASH)+"'")
        df=pd.DataFrame(result.fetchall())
        if df.empty:
            raise ParseError('task hash doesnt exist')
        else:
            result = con.execute("DELETE FROM todolist WHERE id="+"'"+str(args.TASK_HASH)+"'")
            print("Object deleted")

        con.close()

elif args.type=='list':
    if args.ALL:
        result = con.execute("SELECT * FROM todolist")
        df=pd.DataFrame(result.fetchall())

    elif args.TODAY:
        result = con.execute("SELECT * FROM todolist where deadline="+"'"+str(time.strftime('%d%m%Y'))+"'")
        df=pd.DataFrame(result.fetchall())
    con.close()
    print("Table todolist:\n", df)