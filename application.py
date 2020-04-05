# dependencies
from CorgiData import CorgiData
from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
cg = CorgiData("sqlite:///corgies.db")

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/pets<br/>"       
        f"/api/v1.0/pets/(name)<br/>"
        f"/api/v1.0/pet_training<br/>"
        f"/api/v1.0/pet_training/(name)<br/>"
    )

@app.route("/api/v1.0/pets")
def get_all_pets():
    return jsonify(cg.get_pet_data())

@app.route("/api/v1.0/pets/<pet_name>")
def get_one_pet(pet_name):
    return jsonify(cg.get_pet_data(pet_name))    

@app.route("/api/v1.0/pet_training")
def get_all_training():
    cur_args = request.args
    if len(cur_args) == 0:
        return jsonify(cg.get_pet_training_data())
    else:
        args_dict = { key: value for key, value in cur_args.items()}
        print("args_dict\n", args_dict)
        return jsonify(cg.get_pet_training_orm(args_dict))


@app.route("/api/v1.0/pet_training/<pet_name>")
def get_one_training(pet_name):
    return jsonify(cg.get_pet_training_data(pet_name))


if __name__ == '__main__':
    app.run(debug=True)