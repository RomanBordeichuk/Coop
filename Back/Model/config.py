import os
import sys

rmq_user = 'guest'
rmq_password = 'guest'
rmq_host = 'localhost'
rmq_port = 5672
rmq_queue = 'cars'

# getting db path
a = sys.path[0]
b = a.replace('Back/Model', '')
db = os.path.join(b, 'Front/db.db')