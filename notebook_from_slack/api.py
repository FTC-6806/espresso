from notebook_from_slack import app

@app.route('/bot_endpoint')
def bot_endpoint():
	"""The endpoint that Slack will hit with specific messages for us.
	The endpoint just feeds to a db
	"""

	return 'Hello World!'