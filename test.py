from flask import Flask, render_template, request
import csv

app = Flask(__name__)
data = []
codedict = {}
shown_types = ['naam', 'code']

with open('art.csv', 'r') as csv_file:
	csv_reader = csv.DictReader(csv_file)

	with open('art_new.csv', 'w') as new_file:
		fieldnames = list(next(csv_reader).keys())
		csv_writer = csv.DictWriter(new_file, delimiter='\t', fieldnames=fieldnames)

		csv_writer.writeheader()

		for line in csv_reader:
			csv_writer.writerow(line)

with open('art_new.csv', 'r') as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter='\t')

	for dictionary in csv_reader:
		data.append(dictionary)
		codedict[dictionary['code']] = dictionary

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/configuration')
def loadconfiguration():
	return render_template('configuration.html', fieldnames=fieldnames, category=fieldnames[0])

@app.route('/category/<category>')
def changecategory(category):
	print('category')
	print(category)
	return render_template('configuration.html', fieldnames=fieldnames, category=category)

@app.route('/search/<category>')
def loadtable(category):
	search = request.args['search']
	print('search', search)
	showndicts = []
	for dictionary in data:
		if search.lower() in dictionary[category].lower():
			showndicts.append(dictionary)
	if len(showndicts) <= 10:
		lastpage = True
	else:
		lastpage = False
	showndicts = showndicts[:10]
	return render_template('itemtable.html', search=search, showndicts=showndicts, fieldnames=fieldnames, shown_types=shown_types, page=0, category=category, lastpage=lastpage)


@app.route('/item/<code>')
def showextrainfo(code):
    return render_template('iteminfo.html', dictionary=codedict[code], code=code)

@app.route('/page/<page>/<category>')
def changepage(page, category):
	search = request.args['search']
	page = int(page)
	showndicts = []
	for dictionary in data:
		if search.lower() in dictionary[category].lower():
			showndicts.append(dictionary)
	if len(showndicts) <= page * 10 + 10:
		lastpage = True
	else:
		lastpage = False
	showndicts = showndicts[page * 10: page * 10 + 10]
	return render_template('itemtable.html', search=search, showndicts=showndicts, fieldnames=fieldnames, shown_types=shown_types, page=page, category=category, lastpage=lastpage)

app.run(host="0.0.0.0", port=5000)
