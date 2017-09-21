from flask import request


func = request.environ.get('werkzeug.server.shutdown')
if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
func()
