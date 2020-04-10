# Corgi Flask
Example flask app with SQLite corgis.db

## Features
- This app show of to of methods and ideas about ot to break apart yout big project into smaller resuable building blocks.
- Uses ORM and execution modes of SQLAlchemdy
- Shows you routes with variable

## Just added 4/4/2020
- You can now pass in optional arguements.  for example: ....\ap1\v1.0\pet_training?name=Patterson&grade=B
- A fuction was added to the CorgiData that convers a list of tuples to a list of dictionaries
- Filters are being dymically applied based on optional arguments
- The function that is built by the @app.route decorator can do so much more than you realize.  It can be quite complex and send the data retrievel to a toatally different function. You route function can do all kinds of things depending on your objectives

## Just added 4/10/2020
- Used Class Inheritance to create a new class called CorgiDataPands.  
- This class overwrites functions that were not using Pandas to create a dataframe
- Note the commented and uncommented dependencies.  You can see how with one line of code, all changees are made

[Download the Code](https://github.com/andersjh/corgi_flask.git)
