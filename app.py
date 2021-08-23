# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 00:47:33 2021

@author: Kushagra
"""


from model import modelFunction
import os
from sqlalchemy import and_,or_
from eyDatabase import Mail_db
from flask import Flask, flash, request, redirect, render_template,session,make_response
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy
from flask_weasyprint import HTML, render_pdf
from flask_cors import cross_origin
import warnings
from EmailPareser import mainFuncUtlity
from mailSum import utilityFunctions
import eyDatabase as eyDb
warnings.filterwarnings("ignore")

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.secret_key = "abc123"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/ey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b3x2mzn3vgxhrr12:kk1wi098ezdx4bdb@tvcpw8tpu4jvgnnq.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/pwjh6mzn4jk2lehc'


#-------------Creating Objects------------#
db = SQLAlchemy(app)

ms = utilityFunctions()

md = modelFunction()

ep = mainFuncUtlity()

#------------------------Defining Global Variables------------------

visualCommandTuple = ""
riskAdvisoryTuple  = ""
sosTuple       = ""
controlRiskTuple   = "" 
sosRisk = ""
eventNameDb   = ""
countryNameDb = ""

#----------------- APP ROUTE START ------------------#

boolIsOpened = False

@app.route('/', methods=['GET'])
def index():
    
    return render_template('new.html')

@app.route('/about', methods=['GET'])
def about():
    
    return render_template('about.html')

@app.route('/dash', methods=['GET'])
def dash():
    
    return render_template('dashboard.html')


@app.route('/info', methods=['GET'])
def info():
    
    return render_template('info.html',countryList = allCountry,eventList = allEvent)

@app.route('/pdfDown', methods=['GET'])
def pdfDown():
    


    rendered = render_template('report.html', visual_command = visualCommandTuple,risk_advisory = riskAdvisoryTuple,isos = sosTuple,control_risks = controlRiskTuple,eventName = eventNameDb,countryName = countryNameDb )

    
    return render_pdf(HTML(string=rendered))


#-----------------APP ROUTE END------------------#




 #----QUERY START----#

allCountryTuple =  Mail_db.query.with_entities(Mail_db.Country).distinct().all()

allCountry = [item[0] for item in allCountryTuple]


alleventTuple =  Mail_db.query.with_entities(Mail_db.Prediction).distinct().all()

allEvent = [item1[0] for item1 in alleventTuple]




 #----QUERY END----#




ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


fileList = []

textList = []

dateList = []

predList = []

cNameList = []

adviceList = []

infoList = []

travellerList = []

cityList = []

userList = []

summaryList = []

severityList = []

distanceList = []

subjectList = []

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                fileList.append(file_path)
        flash('File(s) successfully uploaded')

        count = 1
            
    
        for i in range(len(fileList)):
            
        
            body, cName,user,date,city,mainText,traveller,info,advice,severity,distance,subject,prediction = ep.mainFunc(fileList[i])       
                
            textList.append(ms.listToString(mainText))

            print("Uploaded", count,"/",len(fileList))

           

            if(user == 'controlrisks'):

                print(prediction)

                predList.append(prediction)

            elif(user == 'everbridge'):

                print(prediction)

                predList.append(prediction)

            else:  
                        
                pred = md.modelFunction(textList[i])

                if (pred == 'Infrastructre Risk'):

                    pred = 'Infrastructre Risk'        

                predList.append(pred)
            
                predList.append(predList[i])
                
            cNameList.append(ms.remove(cName))
            
            #cityList.append(cityName)
            
            dateList.append(date)

            severityList.append(severity)

            cityList.append(city)

            distanceList.append(distance)
            
            userList.append(user)

            travellerList.append(traveller)

            adviceList.append(advice)

            infoList.append(info)

            subjectList.append(subject)
                                               
            
            entry = Mail_db(City = cityList[i],Prediction = predList[i],Subject = subjectList[i],Severity = severityList[i],Distance = distanceList[i],Advice = adviceList[i],Info = infoList[i],Travellers = travellerList[i],Country = cNameList[i],Company = userList[i],Date = dateList[i])
            db.session.add(entry)
            db.session.commit()
            
            count = count + 1
   
        fileList.clear()
        textList.clear()
        predList.clear()
        cNameList.clear()
        cityList.clear()
        distanceList.clear()
        severityList.clear()
        userList.clear()
        travellerList.clear()
        adviceList.clear()
        subjectList.clear()
        infoList.clear()
        
        #vendorName = control_risk
           
        flash('Now you can visit the Information hub')
        
        
        return render_template("new.html", enable = True)
        
                #return render_template("info.html", visual_command = summaryVisual,control_risk = summaryControl,risk_advisory = #summaryRisk,travel_tracker = summaryTravel)
        
        
    return None

@app.route('/bengal1', methods=['GET', 'POST'])
@cross_origin()
def bengal1():

    
    
    updateEvent = True


   # global countryNameDb,eventNameDb ,dateDb
    

    countryNameDb = 'India' 
    eventNameDb = 'Political War Risk'
    
            
        #Visual Command
        
        #global visualCommand

    dateDb = ""

    if dateDb:
    
        visualCommandTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'everbridge'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb))
        
    else:
                visualCommandTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'everbridge'),(Mail_db.Prediction == eventNameDb),(Mail_db.Event == 'Bengal1')).all()
                                                                            
        #Control Risk        
    
    global  controlRiskTuple

    if dateDb:
    
        controlRiskTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'controlrisks'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()       
    
    else:
            controlRiskTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'controlrisks'),(Mail_db.Prediction == eventNameDb)).all()
    

    
    #isos
    global sosRisk

    if dateDb:
    
        sosTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'internationalsos'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()
    
    else:
        sosTuple =  Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'internationalsos'),(Mail_db.Prediction == eventNameDb)).all()
    
    
    #risk advisory
    
    global riskAdvisory

    if dateDb:
    
        riskAdvisoryTuple =Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'riskadvisory'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()
    
        
    else:

        riskAdvisoryTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'riskadvisory'),(Mail_db.Prediction == eventNameDb)).all()
    

            
    boolCheckEmpty = False
    
    if(sosRisk == "No information has been recieved" and riskAdvisory == "No information has been recieved" and controlRisk == "No information has been recieved" and visualCommand == "No information has been recieved"):
        boolCheckEmpty = True



        #Render

    if(countryNameDb == 'India' and eventNameDb == 'Political War Risk'):

        updateEvent = True

    boolIsOpened = True
      
    return render_template("info.html",update_event = updateEvent, visual_command = visualCommandTuple,risk_advisory = riskAdvisoryTuple,isos = sosTuple,control_risks = controlRiskTuple, countryList = allCountry,eventList = allEvent,checkEmpty = boolCheckEmpty,isOpened = boolIsOpened, eventName = eventNameDb,countryName = countryNameDb)
    

@app.route('/bengal2', methods=['GET', 'POST'])
@cross_origin()
def bengal2():

    
    updateEvent = True


   # global countryNameDb,eventNameDb ,dateDb
    

    countryNameDb = 'India' 
    eventNameDb = 'Political War Risk'
    
            
        #Visual Command
        
    global visualCommandTuple

    dateDb = ""

    if dateDb:
    
        visualCommandTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'everbridge'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb))
        
    else:
                visualCommandTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'everbridge'),(Mail_db.Prediction == eventNameDb),(Mail_db.Event == 'Bengal2')).all()
                                                                            
        #Control Risk        
    
    global  controlRiskTuple

    if dateDb:
    
        controlRiskTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'controlrisks'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()       
    
    else:
            controlRiskTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'controlrisks'),(Mail_db.Prediction == eventNameDb)).all()
    

    
    #isos
    global sosTuple

    if dateDb:
    
        sosTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'internationalsos'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()
    
    else:
        sosTuple =  Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'internationalsos'),(Mail_db.Prediction == eventNameDb)).all()
    
    
    #risk advisory
    
    global riskAdvisoryTuple

    if dateDb:
    
        riskAdvisoryTuple =Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'riskadvisory'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()
    
        
    else:

        riskAdvisoryTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'riskadvisory'),(Mail_db.Prediction == eventNameDb)).all()
    

            
    boolCheckEmpty = False
    
    if(sosRisk == "No information has been recieved" and riskAdvisory == "No information has been recieved" and controlRisk == "No information has been recieved" and visualCommand == "No information has been recieved"):
        boolCheckEmpty = True



        #Render

    if(countryNameDb == 'India' and eventNameDb == 'Political War Risk'):

        updateEvent = True

    boolIsOpened = True
      
    return render_template("info.html",update_event = updateEvent, visual_command = visualCommandTuple,risk_advisory = riskAdvisoryTuple,isos = sosTuple,control_risks = controlRiskTuple, countryList = allCountry,eventList = allEvent,checkEmpty = boolCheckEmpty,isOpened = boolIsOpened, eventName = eventNameDb,countryName = countryNameDb)
    

#--------SELECT BUTTON------------------------------#
@app.route('/goButton', methods=['GET', 'POST'])
@cross_origin()
def goButton():
    
    updateEvent = False


    global countryNameDb,eventNameDb ,dateDb
    

    if request.method=="POST":
        countryNameDb = str(request.form["countryOption"])
        eventNameDb   = str(request.form["eventOption"])
        
        dateDb = str(request.form['trip-start'])  #optional

        print(dateDb)

        if eventNameDb == 'Political':
            eventNameDb = eventNameDb + ' War Risk'
        else:  
            eventNameDb = eventNameDb + ' Risk'
    
            
        #Visual Command
        
        global visualCommandTuple

        if dateDb:
        
            visualCommandTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'everbridge'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb))
            
        else:

                  visualCommandTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'everbridge'),(Mail_db.Prediction == eventNameDb)).all()
                                                                                
         #Control Risk        
        
        global  controlRiskTuple

        if dateDb:
        
            controlRiskTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'controlrisks'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()       
        
        else:
             controlRiskTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'controlrisks'),(Mail_db.Prediction == eventNameDb)).all()
        

        
        #isos
        global sosTuple

        if dateDb:
        
            sosTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'internationalsos'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()
        
        else:
            sosTuple =  Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'internationalsos'),(Mail_db.Prediction == eventNameDb)).all()
        
        
        #risk advisory
        
        global riskAdvisoryTuple

        if dateDb:
        
            riskAdvisoryTuple =Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'riskadvisory'),(Mail_db.Prediction == eventNameDb),(Mail_db.Date == dateDb)).all()
        
           
        else:

            riskAdvisoryTuple = Mail_db.query.filter(and_(Mail_db.Country == countryNameDb),(Mail_db.Company == 'riskadvisory'),(Mail_db.Prediction == eventNameDb)).all()
        

                
        boolCheckEmpty = False

        #check all empty

        if not riskAdvisoryTuple and not visualCommandTuple and not sosTuple and not controlRiskTuple:
            boolCheckEmpty = True


        if not riskAdvisoryTuple:

            riskAdvisoryTuple = "No information has been recieved"
        
        if not visualCommandTuple:
            
            visualCommandTuple = "No information has been recieved"

        if not sosTuple:

            sosTuple = "No information has been recieved"

        if not controlRiskTuple:

            controlRiskTuple = "No information has been recieved"
        
   
            #boolCheckEmpty = True

            #Render

    if(countryNameDb == 'India' and eventNameDb == 'Political War Risk'):

        updateEvent = True


    
    boolIsOpened = True
      
    return render_template("info.html",update_event = updateEvent, visual_command = visualCommandTuple,risk_advisory = riskAdvisoryTuple,isos = sosTuple,control_risks = controlRiskTuple, countryList = allCountry,eventList = allEvent,checkEmpty = boolCheckEmpty,isOpened = boolIsOpened, eventName = eventNameDb,countryName = countryNameDb)
    


# disable caching

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

#Error Handle   
@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('error.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
        

if __name__ == '__main__':
   app.run(debug = False)



