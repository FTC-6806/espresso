from notebook_from_slack import app

@app.route('/bot_endpoint')
def bot_endpoint():
	return 'Hello World!'

@app.route('/logs')
def logs():
	return 'not implemented'