from flask import Flask, render_template, request, session
from flask_session import Session
import csv, os, math, uuid

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'ieatdirt123!'
Session(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/configuration')
def loadconfiguration():
	return render_template('configuration.html', fieldnames=[], category='', waitingforfile = True)

@app.route('/file', methods = ['POST'])
def file():
	file = request.files.get('file')
	filename = f'{uuid.uuid4().hex}.csv'
	file.save(os.path.join(app.root_path, filename))
	codedict = {}
	with open (filename, 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for dictionary in csv_reader:
			codedict[list(dictionary.values())[0]] = dictionary
	fieldnames = list(list(codedict.values())[0].keys())
	showntypes = fieldnames[:2]
	session['showntypes'] = showntypes
	session['fieldnames'] = fieldnames
	session['codedict'] = codedict
	os.remove(filename)

	return render_template('configuration.html', fieldnames=fieldnames, category=fieldnames[0], waitingforfile=False)

@app.route('/category')
def changecategory():
	category = request.args['category']
	fieldnames = session.get('fieldnames')
	return render_template('configuration.html', fieldnames=fieldnames, category=category)

@app.route('/search/<category>')
def loadtable(category):
	search = request.args['search']
	fieldnames = session.get('fieldnames')
	codedict = session.get('codedict')
	showndicts = []
	showntypes = session.get('showntypes')
	if category != fieldnames[0]:
		showntypes = [fieldnames[0], category]
		session['showntypes'] = showntypes
	for dictionary in list(codedict.values()):
		if search.lower() in dictionary[category].lower():
			showndicts.append(dictionary)
	totalpages = math.ceil(len(showndicts)/10)
	if totalpages <= 1:
		lastpage = True
	else:
		lastpage = False
	showndicts = showndicts[:10]
	if len(showndicts) == 0:
		page = -1
	else:
		page = 0

	highlights = []
	highlight = []
	if search != '':
		for dictionary in showndicts:
			highlight = []

			start = 0
			index = dictionary[category].lower().find(search.lower())
			while index >= 0:
				highlight.append(index)
				start =  index + len(search)
				index = dictionary[category].lower().find(search.lower(), start)

			highlights.append(highlight)

	return render_template('itemtable.html', highlights=highlights, search=search, showndicts=showndicts, fieldnames=fieldnames, showntypes=showntypes, page=page, totalpages=totalpages, category=category, lastpage=lastpage)

@app.route('/removeinfo')
def removeinfo():
	return render_template('noinfo.html')

@app.route('/item/<code>')
def showextrainfo(code):
	codedict = session.get('codedict')
	return render_template('iteminfo.html', dictionary=codedict[code], code=code)

@app.route('/page/<page>/<category>')
def changepage(page, category):
	search = request.args['search']
	fieldnames = session.get('fieldnames')
	codedict = session.get('codedict')
	page = int(page)
	showndicts = []
	showntypes = session.get('showntypes')
	if category != fieldnames[0]:
		showntypes = [fieldnames[0], category]
		session['showntypes'] = showntypes
	for dictionary in list(codedict.values()):
		if search.lower() in dictionary[category].lower():
			showndicts.append(dictionary)
	totalpages = math.ceil(len(showndicts)/10)
	if page + 1 == totalpages:
		lastpage = True
	else:
		lastpage = False
	showndicts = showndicts[page * 10: page * 10 + 10]

	highlight = []
	highlights = []
	if search != '':
                for dictionary in showndicts:
                        highlight = []

                        start = 0
                        index = dictionary[category].lower().find(search.lower())
                        while index >= 0:
                                highlight.append(index)
                                start =  index + len(search)
                                index = dictionary[category].lower().find(search.lower(), start)

                        highlights.append(highlight)


	return render_template('itemtable.html', highlights=highlights, search=search, showndicts=showndicts, fieldnames=fieldnames, showntypes=showntypes, page=page, totalpages=totalpages, category=category, lastpage=lastpage)

app.run(host="0.0.0.0", port=5000)
