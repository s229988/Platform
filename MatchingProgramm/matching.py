import mysql.connector
import re
from gurobipy import *

cnx = mysql.connector.connect(user='root', password='iot17', host='127.0.0.1', database='website')
cursor = cnx.cursor()

# query jobs (orders)
query = ("SELECT id FROM orders WHERE status='pending'")
cursor.execute(query)
jobs = [item[0] for item in cursor.fetchall()]

# query machines
query = ("SELECT id FROM machines")
cursor.execute(query)
machines = [item[0] for item in cursor.fetchall()]

# query processing time
# query = ("SELECT DATEDIFF(end_date, start_date) FROM orders")
query = ("SELECT amount FROM orders WHERE status='pending'")
cursor.execute(query)
processingtimeValues = [item[0] for item in cursor.fetchall()]
processingtime = dict(zip(jobs, processingtimeValues))

# query deadline
query = ("SELECT DATEDIFF(end_date, start_date) FROM orders")
cursor.execute(query)
deadlineValues = [item[0] for item in cursor.fetchall()]
deadline = dict(zip(jobs, deadlineValues))

# query machine capacity
query = ("SELECT capacity FROM machines")
cursor.execute(query)
machinecapacityValues = [item[0] for item in cursor.fetchall()]
machinecapacity = dict(zip(machines, machinecapacityValues))

# query bid (price_offer)
query = ("SELECT price_offer FROM orders WHERE status='pending'")
cursor.execute(query)
bidValues = [item[0] for item in cursor.fetchall()]
bid = dict(zip(jobs, bidValues))

# ==============================================================================

# update Model automatically
model = Model('Matching')
model.Params.UpdateMode = 1

# add binary decision variable
x = model.addVars(((job, machine) for job in jobs
                   for machine in machines), vtype=GRB.BINARY, name="x")

# add variables to model for start and end time
endtime = model.addVars(((job, machine) for job in jobs
                         for machine in machines), vtype=GRB.CONTINUOUS, name="endtime")

starttime = model.addVars(((job, machine) for job in jobs
                           for machine in machines), vtype=GRB.CONTINUOUS, name="starttime")

# Objective max profit
profit = (quicksum(x[job, machine] * bid[job] for job in jobs for machine in machines))

model.setObjective(profit, GRB.MAXIMIZE)

# 2 -> Capacity limit
model.addConstrs(quicksum(x[job, machine] * processingtime[job] for job in jobs)
                 <= machinecapacity[machine] for job in jobs for machine in machines)

# 3 -> each job not scheduled more than one time
model.addConstrs(x.sum(job, '*') <= 1 for job in jobs)

# 4 -> end time = start time + processing time
model.addConstrs(endtime[job, machine] == starttime[job, machine] +
                 x[job, machine] * processingtime[job] for job in jobs for machine in machines)

# 7 -> start time for next job = end time previous job on machine
model.addConstrs(starttime[job + 1, machine] == endtime[job, machine]
                 for job in jobs for machine in machines if job <= (len(jobs)-1))

# Deadline
model.addConstrs(endtime[job, machine] <= deadline[job]
                 for job in jobs for machine in machines)

# Call Gurobi opimization function
model.optimize()

# Create Output
model.printAttr('x')

# writing result to database
# ==============================================================================
# i = 0
#
# result = {}
# resultEdited = []
#
# for job in jobs:
#     for machine in machines:
#         if (x[job, machine].getAttr(GRB.Attr.X) == 1):
#
#             result[i] = x[job, machine].getAttr(GRB.Attr.VarName).replace('[', ',')
#             result[i] = result[i].replace(']', ',')
#             result[i] = result[i].split(',')
#
#             del resultEdited[:]
#
#             resultEdited.append(i+1)
#             resultEdited.append(result[i][2])
#             resultEdited.append(result[i][1])
#             resultEdited.append(0)
#             resultEdited.append(starttime[job, machine].getAttr(GRB.Attr.X))
#             resultEdited.append(endtime[job, machine].getAttr(GRB.Attr.X))
#
#             addResult = ("INSERT INTO matching_result (result_id, machine_id, article_id, status, starttime, endtime) VALUES (%s, %s, %s, %s, %s, %s)")
#             cursor.execute(addResult, resultEdited)
#             cnx.commit()
#             i += 1
#
# cursor.close()
# ==============================================================================


i = 0

result = {}
resultEdited = []

for job in jobs:
    for machine in machines:
        if (x[job, machine].getAttr(GRB.Attr.X) == 1):

            result[i] = x[job, machine].getAttr(GRB.Attr.VarName).replace('[', ',')
            result[i] = result[i].replace(']', ',')
            result[i] = result[i].split(',')

            del resultEdited[:]

            resultEdited.append(i + 1)
            resultEdited.append(result[i][1])
            resultEdited.append(result[i][2])

            addResult = ("INSERT INTO matches (id, order_id, machine_id) VALUES (%s, %s, %s)")
            cursor.execute(addResult, resultEdited)

            changeStatus = 'UPDATE orders SET status="in production" WHERE id="{}"'.format(job)
            cursor.execute(changeStatus)

            cnx.commit()

            i += 1

        else:
            changeStatus = 'UPDATE orders SET status="not matched" WHERE id="{}"'.format(job)
            cursor.execute(changeStatus)

cursor.close()