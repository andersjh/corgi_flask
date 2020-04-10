# dependencies
from CorgiData import CorgiData
import pandas as pd
from sqlalchemy.orm import Session

class CorgiDataPandas(CorgiData):

    def __init__(self, connect_string):
        super().__init__(connect_string)

    #ORM approach
    def get_pet_data(self, name=""):
        session = Session(self.engine)
        if name == "":
            results = session.query(self.Pets)
        else:
            results = session.query(self.Pets).filter(self.Pets.name == name)
            
        pet_df = pd.read_sql(results.statement, session.connection())
        session.close()  
        return pet_df.to_dict(orient="records")  


    # use ORM to dynamically create query from query parms
    def get_pet_training_orm(self, parm_dict):
        session = Session(self.engine)

        results = session.query(self.PetTraining)
        for k, v in parm_dict.items():
            if k == 'name':
                results = results.filter_by(name = v)
            elif k == 'grade':
                v = v.upper()
                results = results.filter_by(grade = v) 
            elif k == 'task':
                results = results.filter_by(task = v )    

        training_df = pd.read_sql(results.statement, session.connection())
        session.close()
        return training_df.to_dict(orient="records")
            

    

if __name__ == '__main__':
    corgies = CorgiDataPandas("sqlite:///corgies.db")
    print(corgies.get_pet_data())
    # print('*' * 15, "Patterson Only")
    # print(corgies.get_pet_data("Patterson"))
    # print('*' * 15)
    # print(corgies.get_pet_training_data())
    # print('*' * 15, "Patterson Only")
    # print(corgies.get_pet_training_data('PATTERSON'))


        