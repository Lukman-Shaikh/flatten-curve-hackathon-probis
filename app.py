#!/usr/bin/env python3

"""
Flatten the curve hackathon project by team PROBIS
"""

# Script details
__author__ = ["Team Probis"]
__copyright__ = "Copyright 2020-2021,  © 2020 Team Probis - ACS"
__credits__ = ["Team Probis"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = ["Team Probis"]
__email__ = None
__status__ = "Production"


from flask import Flask
from flask import render_template, url_for, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'fslkfndknfls3423'

client = MongoClient("mongodb+srv://probis:probis%40123@saheli-nj2sw.mongodb.net/test?retryWrites=true&w=majority")
probis_db = client['Probis']
req_coll = probis_db["request"]
volunteer_coll = probis_db["volunteer"]
issue_coll = probis_db["issues"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request-form', methods=['GET', 'POST'])
def request_form():
    temp_list = []
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        postcode = request.form['postcode']
        description = request.form['description']
        state = request.form['state']
        items = request.form.getlist('items')

        req_payload = {'name': name, 'phone': phone, 'postcode': postcode, 'description': description, 'state': state,
                   'items': items}

        for key in req_payload.keys():
            temp_list.append(req_payload[key])
        if '' in temp_list:
            pass
        else:
            req_coll.insert_one(req_payload)
        return render_template('congrats.html')
    return render_template('request.html')

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        postcode = request.form['volunteer-postcode']
        phone = request.form['tel']
        email = request.form['email']
        driver_license = request.form['driver-license']

        volunteer_payload = {'first_name': first_name, 'last_name': last_name, 'postcode': postcode, 'phone': phone,
                   'email': email, 'license': driver_license}

        temp_list = []
        for j in volunteer_coll.find():
            temp_list.append(j.get('email'))

        if email not in temp_list:
            volunteer_coll.insert_one(volunteer_payload)
        else:
            pass

        return redirect('/catalog')
    return render_template('volunteer_registration.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        phone = request.form['tel']
        email = request.form['email']
        report = request.form['report']

        issue_payload = {'first_name': first_name, 'last_name': last_name, 'phone': phone, 'email': email, 'report': report}
        issue_coll.insert_one(issue_payload)
        return render_template('status.html', message="Thank you for filing the report. We will be in contact with you any time soon!")

    return render_template('report.html')

@app.route('/status/<req_id>')
def status(req_id):
    phone = []
    req_cursor = req_coll.find({}, {'phone': 1})
    for document in req_cursor:
        temp = str(document.get("_id"))
        if temp == req_id:
            phone.append(document.get("phone"))
    return render_template('status.html', phone=phone[0], message="Thanks for volunteering with us! We need community heroes like you to get us through these hard times")


@app.route('/catalog')
def catalog():

    taskList = []
    req_list = []
    req_cursor = req_coll.find({})

    for document in req_cursor:
        req_list.append(document)

    for obj in req_list:
        task = {'id': obj['_id'], 'state': obj['state'], 'postcode': obj['postcode'], 'items': obj['items']}

        if len(task.get('items')) > 1:
            task['items'] = " & ".join(task.get('items'))
        else:
            task['items'] = str(task.get('items')[0])

        taskList.append(task)
    return render_template('taskList.html', data={'taskList': taskList})

if __name__ == '__main__':
    app.run(debug=True)

