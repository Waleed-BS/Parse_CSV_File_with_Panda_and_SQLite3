from flask import *
import models as model
from werkzeug import secure_filename
import csv

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '''''1_1_1`'''
app.config.from_envvar('CUSTOMER2MAP_SETTINGS', silent=True)

from flask_uploads import *

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

title = ''
population = ''
newPopulationExist = False

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # print 'exist ~~~~~~~~~~~~~~~~~~~~~'
            filename = secure_filename(file.filename)

            number_of_services = (int)(request.form['numberofservices'])

            name_of_services = []
            serviceNumber = 1
            for x in xrange(0, number_of_services):
                name_of_services.append(request.form['service' + `serviceNumber`])
                serviceNumber = serviceNumber + 1

            model.readSurvey(filename, newPopulationExist, number_of_services, name_of_services)

            title = request.form['title']
            population = request.form['population']
            print title
            conn = model.connect_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM population")
            table = [dict(serviceName = row[0], annualDollar = row[1], totalClients = row[2], Impact = row[3], percentage = row[4]) for row in curs.fetchall()]
            model.deleteAllDataFromTable()
            return render_template("report.html", title = title, population = population, table = table)
    else:
        # print 'else'
        return render_template("upload.html")
    return render_template("upload.html")
    
@app.route('/report', methods=['GET','POST'])
def report():

    return render_template('report.html', title = title, population = population)

@app.route('/')
def index():
    return render_template('upload.html')


if __name__ =='__main__':
    app.run()
