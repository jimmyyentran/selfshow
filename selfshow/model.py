from selfspy import models

class Model:

    def __init__(self, db_name):
        self.session = models.initialize(db_name)()


    def query(self):
        for x in self.session.query(models.Keys).all():
            print(vars(x))




if __name__ == "__main__":
    model = Model('/Users/jimmytran/.selfspy/selfspy.sqlite')
    model.query()
