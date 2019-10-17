from datetime import datetime

from pony.orm import Required, PrimaryKey

def define_entities(db):
    
    class Metric(db.Entity):
        id = PrimaryKey(str)
        metric_value = Required(float)
        metric_name = Required(str, index=True)
        machine_id = Required(str)
        timestamp = Required(datetime)