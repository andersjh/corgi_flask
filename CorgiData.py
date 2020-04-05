# dependencies
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, join, outerjoin
from sqlalchemy import Table, MetaData, func

class CorgiData():

    def __init__(self, connect_string):
        self.engine = create_engine(connect_string)
        # self.conn = self.engine.connect()
        self.connect_string = connect_string
        # self.inspector = inspect(self.engine)
        # self.tables = self.inspector.get_table_names()
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        # self.Grades = self.Base.classes['grades']
        self.Pets = self.Base.classes['pets']
        self.meta = MetaData()
        self.PetTraining = Table('pet_training', self.meta, autoload_with=self.engine)
        # self.Training = self.Base.classes['training']
        # self.session = Session(self.engine)

    def display_db_info(self):
        inspector = inspect(self.engine)
        tables = self.inspector.get_table_names()
        for table in self.tables:
            print("\n")
            print('-' * 12)
            print(f"table '{table}' has the following columns:")
            print('-' * 12)
            for column in self.inspector.get_columns(table):
                print(f"name: {column['name']}   column type: {column['type']}")


    
    # idea base from: https://riptutorial.com/sqlalchemy/example/6614/converting-a-query-result-to-dict
    def object_as_dict(self, obj):
        """
        This function takes in a Class instance and converts it to a dictionary
        """
        obj_count = 1
        try:
            obj_count = len(obj)
        except:
            pass
        if  obj_count == 1:
            base_dict = {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
            return base_dict
        else:
            cur_obj = obj[0]
            base_dict = {c.key: getattr(cur_obj, c.key) for c in inspect(cur_obj).mapper.column_attrs}
            for i in range(1, obj_count):
                cur_obj = obj[i]
                cur_dict = {c.key: getattr(cur_obj, c.key) for c in inspect(cur_obj).mapper.column_attrs}
                base_dict = {**base_dict, **cur_dict} 
            return base_dict                 

    # From Jeff LOL
    def query_to_list_of_dicts(self, cur_query):
        """
        From a query object return a list of dictionaries
        """
        return [self.object_as_dict(row) for row in cur_query]

    # list of tuples converted to list of dictionaries
    def list_tuple_to_list_dict(self, cols, rows):
        """
        Take a list of tuples and return a list of dicts
        """
        dict_rows = []
        for row in rows:
            dict_rows.append({ cols[i]: row[i] for i in range(len(cols))})
        return dict_rows    

    
    
    #ORM approach
    def get_pet_data(self, name=""):
        session = Session(self.engine)
        if name == "":
            results = session.query(self.Pets)
        else:
            results = session.query(self.Pets).filter(self.Pets.name == name)
            
        session.close()
        return self.query_to_list_of_dicts(results)    

    

    # sql engine approach
    def get_pet_training_data(self, name=""):
        if name == "":
            sql = "select * from pet_training"
        else:
            cur_name = name.lower()
            sql = f"select * from pet_training where lower(name) = '{cur_name}'"  

        conn = self.engine.connect()
        training_df = pd.read_sql(sql, conn) 
        conn.close()
        return training_df.to_dict(orient='records')  

    # use ORM to dynamically create query from query parms
    def get_pet_training_orm(self, parm_dict):
        session = Session(self.engine)
        table_columns = [c.name for c in self.PetTraining.columns]

        results = session.query(self.PetTraining)
        for k, v in parm_dict.items():
            if k == 'name':
                results = results.filter_by(name = v)
            elif k == 'grade':
                v = v.upper()
                results = results.filter_by(grade = v) 
            elif k == 'task':
                results = results.filter_by(task = v )    

        results = results.all()
        results = self.list_tuple_to_list_dict(table_columns, results)
        session.close()
        return results
           

if __name__ == '__main__':
    corgies = CorgiData("sqlite:///corgies.db")
    print(corgies.get_pet_data())
    print('*' * 15, "Patterson Only")
    print(corgies.get_pet_data("Patterson"))
    print('*' * 15)
    print(corgies.get_pet_training_data())
    print('*' * 15, "Patterson Only")
    print(corgies.get_pet_training_data('PATTERSON'))


        