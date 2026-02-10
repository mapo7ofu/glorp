

from flask import Flask, render_template
import csv

app = Flask(__name__)
data = []
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

@app.route('/')

def index():
	return render_template('index.html', data=data, fieldnames=fieldnames, shown_types=shown_types)

@app.route('/clicked/<code>')

def itemclicked(code):
	return render_template('iteminfo.html', code=code)

app.run(host="0.0.0.0", port=5000)
