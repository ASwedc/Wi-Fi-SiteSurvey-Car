import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # path of database
    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'beacon.sqlite'))
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # import data base    
    from . import db
    db.init_app(app)
    
    # import web
    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')
    print("import web OK")
    
    # import site survey
    from . import car
    car.Current_app(app)
    app.register_blueprint(car.bp)
    print("import site survey OK")
    
    return app