#  from selfspy import models
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from IPython import embed
import time

class Model:

    def __init__(self, db_name):
        Base = automap_base()
        engine = create_engine('sqlite:///%s' % db_name)
        Base.prepare(engine, reflect=True)
        self.Keys = Base.classes.get('keys')
        self.session = Session(engine)

    def query_keys(self):
        keystrokes = self.session.query(self.Keys).all()
        plot = []
        for key in keystrokes:
            plot.append(dict(x=time.mktime(key.started.timetuple()), y=key.nrkeys))
            plot.append(dict(x=time.mktime(key.created_at.timetuple()), y=key.nrkeys))
        return plot

if __name__ == "__main__":
    model = Model('/Users/jimmytran/.selfspy/selfspy.sqlite')
    model.query_keys()
