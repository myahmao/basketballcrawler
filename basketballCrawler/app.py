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

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import sys
import requests, urllib

import logging

logger = logging.getLogger(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tar'])
dbName = '' 

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "super secret key"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('little.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

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
    print 143, _name
    _name = _name.title()

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


    #dlist=[]
    data = collection.distinct('team')
    #for item in data:
    #    if item is not u' ':
    #        dlist.append(str(item))
    #print sorted(data)[1:]
    team_list = sorted(data)[1:]

    players = sorted(collection.distinct('name'))

   	#data = collection.find({'$text':{'$search': _name}}, {'_id':0})
    
    if radio_value == 'player':
        data = collection.find_one({'name': _name}, {'_id':0})


        if data is not None:

            for item in data:
                    #pprint(item)
                    if item == 'overview_url':
                        link = str(data[item])
                    if item == 'positions':
                        result_temp += str(item) + ':'
                        for value in data[item]:
                            result_temp += str(value) + ','
                        result_temp += '\n'
                    else:
                        result_temp += str(item) + ' : ' + str(data[item])+'\n'
            col = 'Player'

            datadict[_name]= result_temp
            return render_template('result.html', data=datadict, colls=col, link=link)

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

    if radio_value == 'all':
        _name = _name.lower()
        _name1 = correction(_name)
        print _name1.title()

        if _name1 != _name:
            result_temp += 'Do you mean '+_name1 + ':\n'

        for player in players:
            if _name1.title() == player.title():
                data = collection.find_one({'name': player.title()}, {'_id':0})


                if data is not None:

                    for item in data:
                            #pprint(item)
                            if item == 'overview_url':
                                link = str(data[item])
                            if item == 'positions':
                                result_temp += str(item).title() + ':'
                                for value in data[item]:
                                    result_temp += str(value) + ','
                                result_temp += '\n'
                            else:
                                result_temp += str(item).title() + ' : ' + str(data[item])+'\n'
                    col = 'Player'


                    url = link
                    html = urllib.urlopen(url).read()
                    soup = BeautifulSoup(html, 'html5lib')

                    body_text = soup.findAll('body')
                    response = HtmlResponse(url=url, body=str(body_text[0]))

                    name = response.xpath('//*[@itemprop="relatedTo"]/text()').extract()
                    if len(name) is not 0:
                        result_temp += 'Relative: '
                        for item in name:
                            print str(item)
                            result_temp += str(item)+ ', '
                        result_temp += '\n'
                    date=response.xpath('//*[@id="top_news"]/div/strong/text()').extract()
                    if len(date) != 0:
                        result_temp += '\nLatest News: ' +response.xpath('//*[@id="top_news"]/div/strong/text()').extract()[0] \
                            +','+response.xpath('//*[@id="top_news"]/div/text()').extract()[0]+'\n'

                    datadict[player]= result_temp
                    return render_template('result.html', data=datadict, colls=col, link=link)

                #else:
                    #result_temp = 'Not found!'

        for item in team_list:
            if _name1.title() in item.title():
                result_temp += item + ' has following players\n';
                cursor = collection.find({'team': item}, {'_id':0})

            #result_temp = ' has following players:\n'

                for data in cursor:
                    #print 218, data
                    result_temp += 'Jersey ' + str(data['jersey'])+ ': '+str(data['name'])+'\n'
                if result_temp =='':
                    result_temp = 'Not found!'

                print item
                break

        cursor = collection.find({'$text':{'$search': _name1}}, {'_id':0})

        #result_temp = ' has following players:\n'

        for data in cursor:
            #print 200, data
            if 'team' in data:
                result_temp += str(data['team'])+ ': '+str(data['name'])+'\n'
            else:
                result_temp += str(data['name'])+'\n'
        if result_temp =='':
            result_temp = 'Not found!'

    if radio_value == 'list':
        if _name == 'Name' or _name == 'Team' or _name=='Player' :
            if _name == 'Player':
                _name = 'Name'
            data =collection.distinct(_name.lower())
            #print 216, data
            dlist = []
            for item in data:
                if item != ' ':
                    dlist.append(str(item))
            dlist = sorted(dlist)
            for item in dlist:
                result_temp += item + '\n'
        else:
            result_temp = 'Not Found!'

    col = 'Player'

    datadict[_name]= result_temp
    #print 224,datadict

    #if len(datadict[col]) == 0 :
    #    del datadict[col]
                

    return render_template('result.html', data=datadict, colls=col)



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
        debug=True,
        threaded=True
    )

