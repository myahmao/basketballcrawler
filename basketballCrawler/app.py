from flask import Flask, render_template, request, json, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pprint import pprint
from sets import Set

import sys
sys.path.append("..")
import inspect
import os, re
from flask import request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename


import logging

logger = logging.getLogger(__name__)


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tar'])
dbName = '' 

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "super secret key"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#CmdList = {'show system internal vpcm info peer-link':['show system internal vpcm info peer-link'],
#           'show system internal vpcm info vpc':['show system internal vpcm info vpc'],
#           'show system internal vpcm info global':['show system internal vpcm info global']
#           }




# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/search/', methods=['GET', 'POST'])
def search():
    print request.method

    techstr = ''
    if request.method == 'POST':
        global dbName
        dbname = request.form['sessionID2']
        dbName = dbname
        #print 88,'dbName', dbname

        bugID = request.form['sessionID1']
        print 'bugID', bugID

        moduleList = request.form.getlist('component')
        print 94, moduleList

        binaryTs = []
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        #print 99, file
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            binTs= app.config['UPLOAD_FOLDER']+ filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            binaryTs.append(binTs)
            #return redirect(url_for('upload_file',
            #                        filename=filename))
        '''
            call iparser 
        '''
        print binaryTs
        #moduleList = ['vpc','eth_port_channel', 'ethpm']
        treeList = None
        work_dir_list, active_sup_num = iparser.iparser(binaryTs,moduleList, treeList)
        print "work_dir_list"
        print work_dir_list
        
        print "active_sup_num"
        print active_sup_num
        sessionId = None

        if str(bugID).startswith("CSC"):
            carrier = Carrier(str(bugID))
        else:
            carrier = Carrier(sessionId)
        for work_dir in work_dir_list:
            matched = re.search(r'switch\d', work_dir)
            switchID = matched.group(0)
            carrier.dumpLog(str(work_dir), switchID, active_sup_num)
     
        #global dbName 
        dbName = carrier.sessionID
        print "dbName = " + dbName

        '''delete parsed logs'''
	os.system("rm -rf iparser_*") 

    #global dbName

    frame = inspect.currentframe()
    # __FILE__
    fileName  =  frame.f_code.co_filename
    # __LINE__
    fileNo = frame.f_lineno
    print frame.f_lineno, 'dbName', dbName

    tech_supp = []

    #global dbName
    if dbName == '':
        dbName = 'T10341'

    if dbName != '':
        client = MongoClient('localhost',27017)
        db = client['nba_player']
        collection = db['Player']
        data = collection.find()
        for item in data:
            if item !=None:
                tech_supp = item['logList']
        for i in range(len(tech_supp)):
            techstr += tech_supp[i]
        
        print 'techstr', techstr

    return render_template('search.html', techstr=techstr, dbname=dbName)

@app.route('/result/', methods=['GET', 'POST'])
def result():

    _name = request.form['searchKeyword']
    _name = _name.title()
    print _name

    radio_value = request.form['radio']
    print 146, radio_value

    '''client = MongoClient('34.212.20.96:27017')
    db = client['nba_player']
    collection = client['Player']
    '''
    client = MongoClient('localhost', 27017)
    coll_name = 'Player'
    db = client['nba_player']
    #db.authenticate(user[1], user[2])
    collection = db[coll_name]
  
    datadict = {}

    result_temp = ''
    datadict[_name] = ''
   	#data = collection.find({'$text':{'$search': _name}}, {'_id':0})
    
    if radio_value == 'player':
        data = collection.find_one({'name': _name}, {'_id':0})


        if data is not None:

            for item in data:
                    #pprint(item)
                    
                    if item == 'positions':
                        result_temp += str(item) + ':'
                        for value in data[item]:
                            result_temp += str(value) + ','
                        result_temp += '\n'
                    else :
                        result_temp += str(item) + ' : ' + str(data[item])+'\n'
        else:
            result_temp = 'Not found!'

    if radio_value == 'team':
        cursor = collection.find({'team': _name}, {'_id':0})

        #result_temp = ' has following players:\n'

        for data in cursor:
            #print 218, data
            result_temp += 'Jersey ' + str(data['jersey'])+ ': '+str(data['name'])+'\n'
        if result_temp =='':
            result_temp = 'Not found!'
    col = 'Player'

    datadict[_name]= result_temp
    print 196,datadict

    #if len(datadict[col]) == 0 :
    #    del datadict[col]
                
        
    #pprint(datadict[col])
    #pprint (datadict)
    #print 256, 'send coll is ', colls
    return render_template('result.html', data=datadict, colls=col)


@app.route('/health/', methods=['GET', 'POST'])
def health():
    print request.method


    reportStr=''
    resultStr = ''
    global dbName
    if resultList is None or len(resultList) == 0:
        print "No results are found"
        return
    pass_seqno = 0
    total_seqno = 0
    hasbeenhit = False
    failedRules = ''
    for result in resultList:
        total_seqno += 1
        if result.hit:
            
            #print 276, result.contextList
            deviceID = result.contextList[0]['Device-id']
            matched = re.search(r"vdc(\d+)", deviceID)
            vdcNumber = matched.group(1)
            #resultStr += "===================================================\n"
            resultStr += str(total_seqno) + '. '+ result.ruleName +': HIT\n'
            failedRules += result.ruleName +'\n'
            #resultStr += "VDC: " + vdcNumber + '\n' 
            resultStr += "Description: " + result.description + '\n\n'
            for entry in result.contextList:
                hasbeenhit = True
                display = Displayer('DETAIL', entry)
                resultStr += display.JSON_print() +'\n\n'
        else :
            pass_seqno += 1
            #resultStr += '===================================================\n'
            resultStr += str(total_seqno) + '. ' +result.ruleName + ': PASS\n'
            resultStr += "Description: " + result.description + '\n\n'
    reportStr  = 'SUMMARY: \n===================================================\n'
    reportStr += 'Passed rules  : ' +str(pass_seqno) + '\nFailed rules    : ' + str(total_seqno-pass_seqno) \
                 + '\nTotal rules      : ' + str(total_seqno) + '\nHealth Score : ' + str(float(pass_seqno)/total_seqno*100)[:4] + '\n\n' \
                 + 'Failed Rules: \n===================================================\n' + failedRules + '\n'
    reportStr += 'DETAIL: \n===================================================\n' + resultStr
    if not hasbeenhit:
        print "All rules are not been hit on selected VDCs."
    print reportStr


    return render_template('health.html', data='reportStr')

@app.route('/correct/', methods=['GET', 'POST'])
def correct():
    print request.method

    datadict = {}
    #datadict[_name] = ''
    datadict['Text']= "Do you know who clay comes is of course and though he he is with the Golden State Warriors I laxity Stephen curry Kevin Durant and so forth there's really gave lebron James a real headache I cannot wait to see their meet at next NBA championship game."
    col = 'Player'
    return render_template("correct.html",data = datadict, colls=col)
# Route that will process the AJAX request, sum up two
# integer numbers (defaulted to zero) and return the
# result as a proper JSON response (Content-Type, etc.)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #print request.method
    return render_template('search.html')
    

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

