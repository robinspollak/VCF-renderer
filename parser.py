from flask import Flask, url_for, render_template, request,json,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.ext.sqlalchemy import SQLAlchemy

variantData = open("HG00101.chrY.vcf")

def setUpDB():
	listOfData = []
	for line in variantData:
		listOfData.append(line.split('	'))
	IDcounter = 2
	for item in listOfData:
		if item[-1]=='1\n':
			toAddToDatabase = Line(IDcounter,int(item[1]),item[0],item[2],item[3],item[4],int(item[5]),item[7]) #constructor for database
			IDcounter+=1 
			db.session.add(toAddToDatabase)
			db.session.commit()

def formatData(databaseObject):
	return {'Chromosome' : databaseObject.Chromosome,\
	'Base Pair Position' : databaseObject.Position,\
	'Reference Base Pair' : databaseObject.referenceBase,\
	'Variant Base Pair' : databaseObject.actualBase\
	# ,'ID Number' : databaseObject.ID
	}

def formatList(listOfObjects):
	return map(json.dumps,map(formatData,listOfObjects))



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db_user:password@my-db-instance.coekoehxjoxi.us-west-2.rds.amazonaws.com/my_database'
db = SQLAlchemy(app)

class Line(db.Model):
    __tablename__ = 'myDatabase'
    Counter = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.Integer, unique=False)
    Chromosome = db.Column(db.String(10),unique=False)
    ID = db.Column(db.String(50),unique=False)
    referenceBase = db.Column(db.String(50),unique=False)
    actualBase = db.Column(db.String(50),unique=False)
    Quality = db.Column(db.Integer, unique=False)
    Format = db.Column(db.String(300), unique=False)

    def __init__(self, Counter=None, Position=None, Chromosome=None,ID=None,referenceBase=None,actualBase=None,Quality=None,Format=None):
        self.Counter = Counter
        self.Position = Position
        self.Chromosome = Chromosome
        self.ID = ID
        self.referenceBase = referenceBase
        self.actualBase = actualBase
        self.Quality = Quality
        self.Format = Format

    def __repr__(self):
        toreturn = ''
        toreturn+='Counter: %s\n'%(self.Counter)
        toreturn+='Chromosome: %s\n'%(self.Chromosome)
        toreturn+='Base Pair Position: %s\n'%(self.Position)
        toreturn+='ID Number: %s\n'%(self.ID)
        toreturn+='Base Should be: %s\n'%(self.referenceBase)
        toreturn+='Base Actually is: %s\n'%(self.actualBase)
        toreturn+='Quality of Gene: %s\n'%(self.Quality)
        toreturn+='Format: %s\n'%(self.Format)
        return toreturn

db.create_all()
db.session.commit()

if Line.query.first()==None:
	print("im here!")
	setUpDB()

@app.route('/')
def root():
	return render_template('index.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/data')
def serveUp():
	return render_template('data.html',jsonList=formatList(Line.query.all()))

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=80)
	







