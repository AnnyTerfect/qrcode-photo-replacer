import requests
import json
import pickle
import re
import base64
from flask import Flask
from flask import request
from flask import Response

def log(msg):
	print(msg)
	with open('log.txt', 'a') as wf:
		wf.write(msg)

app = Flask(__name__)

def print_request(request):
	method = request.method
	url = request.url
	headers = {h[0]: h[1] for h in request.headers}
	data = request.data
	json = request.json if headers.get('Content-Type', '') == 'application/json' else dict(request.form)
	log(('#' * 40) + ' Request ' + ('#' * 40) + '\n')
	log('method = {}\nurl = {}\nheaders = {}\ndata = {}\njson = {}\n'.format(method, url, headers, data, json))
	log('#' * 89 + '\n')
 
def print_response(res):
	log(('#' * 40) + ' Response ' + ('#' * 40) + '\n')
	log('url = {}\nheaders = {}\ncontent = {}\n'.format(res.url, res.headers, res.content[: 100]))
	log('#' * 89 + '\n')

@app.route('/photo', methods=['GET'])
def get_photo():
	response = Response()
	response.status_code = 200
	response.headers['Content-Type'] = 'image/jpeg'
	with open('photo.jpg', 'rb') as rf:
		response.set_data(rf.read())
	return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'HEAD'])
def handler(path):
	# Print request
	print_request(request)

	# Parse and modify request
	https = True
	headers = {h[0]: h[1] for h in request.headers}
	url = request.url
	url = url.replace('http:', 'https:') if https else url
	url = re.sub('(?<=https:\/\/).*?(?=\/)', '219.219.115.212', url)
	headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 9; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15'

	# Handle */api/photo directly
	if url.split('/')[-2: ] == ['api', 'photo']:
		response = Response()
		response.status_code = 200
		response.headers['Content-Type'] = 'application/json'
		response.set_data(json.dumps({"headerurl": '/photo'}))
		return response

	kwargs = {
		'method': request.method,
		'url': url,
		'headers': headers,
		'verify': False,
		'allow_redirects': False
	}
	if headers.get('Content-Type', '') == 'application/json' and request.json:
		kwargs['json'] = request.json
	elif request.form:
		kwargs['json'] = request.form
	
	if request.data:
		kwargs['data'] = request.data

	res = requests.request(**kwargs)
	print_response(res)
	response = Response(res) 
	response.status_code = res.status_code
	for key, value in res.headers.items():
		if key.lower() not in ('connection', 'content-encoding', 'transfer-encoding'):
			response.headers[key] = value
	for k, v in res.cookies.items():
		response.set_cookie(k, v)

	return response

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
