#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pdfplumber
import email
import regex as re
import pycountry
import mailSum as ms
from geotext import GeoText
import datetime
from mailSum import utilityFunctions



ms = utilityFunctions()

#-----------------------ISOS EMAIL CLASS START-----------------------#

class isosMail(object):


    def isosSeverity(self,text):
   
        if "Notice" in text:
            return 1
        if "Special Advisory" in text:
            return 5
        if "Advisory" in text:
            return 3
        else:
            return "Not Recieved"
       

    def isosAdvice(self,txt):
        start = "WHAT WE ADVISED YOUR PEOPLE"
        end = "ASSISTANCE"
        advice = txt[txt.find(start)+len(start):txt.rfind(end)]
        return advice

    def notravel(self,txt):
        start = "Subject:"
        end = "travellers now"
        sub = txt[txt.find(start)+len(start):txt.rfind(end)]

        sub = re.search(r'\d+', sub).group()

        if(sub == ''):
            sub = 'Not Recieved'

        return sub

    def isosInfo(self,txt):
        start = "Italiano"
        end = "OVERVIEW"
        info = txt[txt.find(start) + len(start):txt.rfind(end)]
        return info

    def isosSub(self,txt):
        start = "travellers now"
        end = "This alert is available to view"
        info = txt[txt.find(start) + len(start):txt.rfind(end)]
        return info

#-----------------------ISOS EMAIL CLASS END-----------------------#

#-----------------------EVERBRIDGE EMAIL CLASS START-----------------------#

class riskMail(object):

    def __init__(self):

        self.l = ["Civil Demonstration","Civil Rioting","General Civil Unrest","Civil Conflict" ]
        self.l2 = ["Earthquake" , "General Natural Disaster" , "Tropical Cyclone" , "Hurricane" , "Tsunami" , "Volcano" , "General Other Security" , "Flood" , "General Other Weather" , "T,nado" , "Winter" ]
        self.l3 = ["Hostage" , "Police" , "Security Activity" , "Robbery" , "Shooting"] 
        self.l4 = ["Bomb Detected" , "Bomb Explosion" , "General Terr,ism" , "Suspicious Activity" , "Suspicious Object" , "Bomb" , "explosive" , "Explosion"]
        self.l5 = ["Disease Outbreak" , "General Health" , "Disease"]
        self.l6 = [ "Chemical Agent" , "Chemical Explosion" , "General Hazmat" , "Fire" , "Non Residential Fire" , "Wildfire" , "Radioactive Agent" , "Avalanche" , "Genral Local Disaster" , "Landslide" , "Subsidence" , "Drinking Water" , "Gas Outage" , "General Utility" , "Infrastructure" , "Power" , "Sewage" , "Telecommunications"]
        self.l7 = ["General War" , "War" , "Conflict"]

    def riskCategory(self,text):
            
        if any(word in text for word in self.l):
            return "Civil Unrest Risk"
        
        elif any(word in text for word in self.l2):
            return "Security Risk"
        
        elif any(word in text for word in self.l3):
            return "Crime Risk"
            
        elif any(word in text for word in self.l4):
            return "Terrorism Risk"
            
        elif any(word in text for word in self.l5):
            return "Medical Risk"
        
        elif any(word in text for word in self.l6):
            return "Infrastructure Risk"
            
        elif any(word in text for word in self.l7):
            return "Political Risk"
       
        else:
            return 'Not Recieved'

    def riskSevere(self,txt):
        start = "Severity:"
        end = "Alert Location:"
        severe = txt[txt.find(start) + len(start):txt.rfind(end)]

        if(severe == 'Minor'):
           
            severe = 1
        
        elif(severe == 'Moderate'):
            
            severe = 2

        elif(severe == 'Severe'):
            
            severe = 4
        
        elif(severe == 'Extreme'):

            severe = 5
      
        else:   

            if 'For more information' in severe:

                severe = re.search(r'\d+', severe).group()

                if int(severe) > 5:
                    severe = 5

        return severe

    def riskDist(self,txt):
        number = re.findall("Distance from alert to nearest asset:(.*)",txt)
        return number

    def riskInfo(self,txt):
        start = "Distance from alert to nearest asset"
        end = "For more information"
        info = txt[txt.find(start) + len(start):txt.rfind(end)]
        info = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', info)

        return info

    def riskSub(self,txt):
        start = "Subject:"
        end = "Urgent:"
        sub = txt[txt.find(start) + len(start):txt.rfind(end)]
        return sub

    def riskCity(self,text):
      
        city = re.findall("Alert Location:(.*)",text)[0]

        return city



#-----------------------EVERBRIDGE EMAIL CLASS END-----------------------#

#-----------------------CORE EMAIL CLASS START-----------------------#

class coreMail(object):

    def coreInfo(self,txt):
        start = "Incident date:"
        end = 'CATEGORIES'
        string = txt[txt.find(start)+len(start):txt.rfind(end)]
        string = string.replace("VIEWONMAP"," ")
        string = string.replace("Location Precision: Street / Neighbourhood"," ")
        string = string.replace("\n"," ")
        string = re.sub(" +"," ",string)

        start1 = "2021"
        end1 = ''
        string = string[string.find(start1)+len(start1):string.rfind(end1)]
        
        return string


    def coreSeverity(self,text):
        if "ONE" in text:
            return 1
        if "TWO" in text:
            return 2
        if "THREE" in text:
            return 3
        if "FOUR" in text:
            return 4
        if "FIVE" in text:
            return 5
        else:
            return "Not Recieved"

    def coreCategory(self,text):
        if "WAR" in text:
            return "War Risk"
        if "CRIME" in text:
            return "Crime Risk"
        if "UNREST" in text:
            return "Civil Unrest Risk"
        if "TERRORISM" in text:
            return "Terrorism Risk"
        if "WAR,CRIME" in text:
            return "War,Crime Risk"
        if "UNREST,WAR" in text:
            return "Unrest,War Risk"
        if "UNREST,TERRORISM" in text:
            return "Unrest,Terrorism Risk"
        if "WAR,TERRORISM" in text:
            return "War,Terroism Risk"
        else:
            return "Not Recieved"

    def coreSubject(self,text):
        sub = re.findall("Subject:(.*)",text)
        return sub


    
    def coreDist(self,text):
       
        dist = ""

        if 'This incident occurred approximately' in text:
        
            dist = re.findall("This incident occurred approximately (.*)",text)[0]
            
            if dist:

                dist = re.search(r'\d+', dist).group()

                if(dist == ''):
                    dist = 'Not Recieved'

        return dist

#-----------------------CORE EMAIL CLASS END-----------------------#

class emailParserUtility(object):

    def city(self,text):
        places = GeoText(text)
        cities = list(places.cities)
        return cities

    def changeDate(self,t):

        t = (t.replace(',', ' '))
        date = datetime.datetime.strptime(t, '%A %B %d %Y').strftime('%Y-%m-%d')
        return date



    def date(self,txt):
        start = "Sent on:"
        end = "To:"
        data = txt[txt.find(start) + len(start):txt.rfind(end)]
        sep = '2021'
        stripped = data.split(sep, 1)[0]
        
        txt =  (stripped+'2021')

        txt = txt.lstrip()

        dateNew = self.changeDate(txt)

        return dateNew

    def emailNew(self,text):
        ls = re.findall('\S+@\S+', text)
        return ls

    def emailParser(self,loc):
        all_text =""
        with pdfplumber.open(loc) as pdf:
            for pdf_page in pdf.pages:
                single_page_text = pdf_page.extract_text()
                if single_page_text:
                    all_text = all_text + '\n' + single_page_text
            return (all_text) 

    def countryName(self,text):
        for country in pycountry.countries:
            if country.name in text:
                return country.name


   
obj = emailParserUtility()

   
class mainFuncUtlity(object):

    def __init__(self):
        
        self.UserLS = []
        self.NameLS = []
        self.FileName = []
        self.mainTextLS = []
        self.body = []
        self.Subject = []
        self.advice = "Not Recieved"
        self.info = "Not Recieved"
        self.distance = "Not Recieved"
        self.traveller = "Not Recieved"
        self.severity = "Not Recieved"
        self.prediction = "Not Recieved"
        self.Subject  = "Not Recieved"
        self.city = "Not Recieved"
    



    def mainFunc(self,path):
     
        #cName = countryName(path)
        
        cName = obj.countryName(obj.emailParser(path))
        
        txt = obj.emailParser(path)
        
        emailDf = obj.emailNew(txt)[0]
        
        dateDf = (obj.date(txt))
        
        cityName = obj.city(txt)
        
        msg = email.message_from_string(obj.emailParser(path))
        
        listMail = (ms.listToString(obj.emailNew(txt))) 
        user = listMail[listMail.find("@")+1:].split()[0]
        user = user.split('.')[0]

        print(user)


        if (user == 'internationalsos'):

            isosObj = isosMail()

            self.advice = isosObj.isosAdvice(txt)

            self.info   = isosObj.isosInfo(txt)

            self.traveller = isosObj.notravel(txt)

            self.subject = isosObj.isosSub(txt)

            self.severity = isosObj.isosSeverity(txt)

            
        if (user == 'controlrisks'):

            cObj = coreMail()

            self.severity = cObj.coreSeverity(txt)

            self.prediction = cObj.coreCategory(txt)

            self.info = cObj.coreInfo(txt)

            self.subject = cObj.coreSubject(txt)

            self.distance = cObj.coreDist(txt)


        if (user == 'everbridge'):

            riskObj = riskMail()

            self.severity = riskObj.riskSevere(txt)

            self.distance  = riskObj.riskDist(txt)

            self.subject = riskObj.riskSub(txt)

            self.prediction = riskObj.riskCategory(txt)

            self.info = riskObj.riskInfo(txt)

            self.city = riskObj.riskCity(txt)


        if (user == 'riskadvisory'):
              pass
        
        
        if msg.is_multipart():
            for payload in msg.get_payload():
                    self.body.append(payload.get_payload())
                    res = payload.get_payload()
        else:
            self.body.append(msg.get_payload())
            res = msg.get_payload()
            
        msg = msg['Subject']
        

        if(type(msg)==None.__class__):
            msg = ""
        
        mainText = res + msg

        print(msg)
        
        #results

        self.UserLS.append(user)
        self.FileName.append(path)
        self.NameLS.append(cName)
        self.mainTextLS.append(mainText)
       # self.summary = ms.mailSummary(res)


        return self.body, cName,user,dateDf,self.city,self.mainTextLS,self.traveller,self.info,self.advice,self.severity,self.distance,self.subject,self.prediction
   

        


