restify = require 'restify'
mongojs = require 'mongojs'
_ = require 'lodash'


db = mongojs 'gnats'
issues = db.collection 'issues'
items_per_page = 40

server = restify.createServer()

server.use restify.queryParser()
# server.use restify.jsonp()

server.get '/', (req, res, next) ->
	  res.send
		    status: 1

server.get '/team/:name', (req, res, next) ->
    # not implemented
    res.send
        status: 1

server.get '/:name', (req, res, next) ->
    uid = req.params.name.replace '.json', ''

    options =
      _id: 0
      audit_trail: 0
      
    issues.find {responsible: uid}, options, (err, doc) ->
        res.send doc


server.get '/search.json', (req, res, next) ->
    # not implemented
    t = req.params.term.trim()
    if not t
        res.send []

    term = new RegExp t
    options = _id: 0
    query = "$or": [{uid: term}, {preferred_name: term}, {cube: term}, {extension: term}, {mobile: term}, {phone: term}]

    employees.find query, options, (err, docs) ->
        res.send docs


server.listen 6090, ->
    console.log 'ready on %s', server.url