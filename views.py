from flask import *
import models as model
from werkzeug import secure_filename
import csv

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '''''1_1_1`'''
app.config.from_envvar('CUSTOMER2MAP_SETTINGS', silent=True)

# configuration
# UPLOAD_FOLDER = '/upload'

# DEBUG = True
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'



# sess = Session()

# photos = UploadSet('photos', IMAGES)
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST' and 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         rec = Photo(filename=filename, user=g.user.id)
#         rec.store()
#         flash("Photo saved.")
#         return redirect(url_for('show', id=rec.id))
#     return render_template('upload.html')
#
# @app.route('/photo/<id>')
# def show(id):
#     photo = Photo.load(id)
#     if photo is None:
#         abort(404)
#     url = photos.url(photo.filename)
#     return render_template('show.html', url=url, photo=photo)

from flask_uploads import *

# UPLOAD_FOLDER = '/upload'
ALLOWED_EXTENSIONS = set(['csv'])
# pp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            # print population
            # foo = request.form['name']
            # print foo
            # path = os.path.dirname(os.path.abspath(__file__)) + "/csvfiles/"+foo
            # print path
            # if not os.path.exists(path):
            #     print " not exist ~~~~~~~~~~~~~~~~"
            #     os.makedirs(path)
            # app.config["UPLOAD_FOLDER"] = path

            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print file
            # return redirect(url_for('report'))
            return render_template("report.html", title = title, population = population, table = table)
    else:
        # print 'else'
        return render_template("upload.html")
    return render_template("upload.html")
        # with open('./uploads/upload.csv.csv', 'rb') as csvfile:
        #     rows = csv.reader(csvfile, delimiter=',', quotechar='"')
        #     for row in rows:
        #         name = row[0]
        #         address = row[1]
        #         additionaldata = row[2]
        #         err,lat,lng = geodecode(address)
        #     if err == False:
        #         db.execute('insert into entries (name,address,lat,lng,additionaldata) values (?,?,?,?,?)',
        #         (name,address,lat,lng,additionaldata))
        #         db.commit()


@app.route('/report', methods=['GET','POST'])
def report():

    return render_template('report.html', title = title, population = population)

@app.route('/')
def index():
    return render_template('upload.html')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# gives the file name and extension in flask
# request.files['upload'].filename
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# todo:
#   - click on generate button calls
#   - click on

# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#
#         print "/uploader ~~~~~~~~~~~~~~"
#
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         model.read(f)
#         return 'file uploaded successfully'
    # return render_template('upload.html')




# @app.route('/report')
# def report():
#     # if not session.get('received_file'):
#     return render_template('home.html')



if __name__ =='__main__':
    app.run()
