from bottle import route, run, template, get, post, request, response, app
import json
import redis
from redislite import Redis


#r = redis.Redis(host=rhost, password='', port=rport, decode_responses=True) # db redis a bit more serious

r = Redis("shareingan.db") # db light

# control allow origin or here twitter.com
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = 'https://twitter.com'
    #response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.headers['Content-Type'] = 'application/json'

# get the number of report, 0 for not toxic.
@get('/istoxic/get/<atnickname>')
def istoxic(atnickname):
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    ret = r.get(atnickname)

    print("Get : ",atnickname," -> ",ret)

    if ret != None:
        response.status = 200
        enable_cors()
        reports = json.loads(ret)
        return json.dumps(len(reports))
    else:
        response.status = 200
        enable_cors()
        return json.dumps("0")

@get('/istoxic/get/reports/<atnickname>')
def getreports(atnickname):
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    ret = r.get(atnickname)
    print("Get all reports : ",atnickname," -> ",ret)
    if ret != None:
        response.status = 200
        enable_cors()
        response.headers['Access-Control-Allow-Origin'] = '*'
        return ret
    else:
        response.status = 200
        enable_cors()
        response.headers['Access-Control-Allow-Origin'] = '*'
        return json.dumps([])

@post('/istoxic/report/<atnickname>')
def istoxicset(atnickname):
    print("Received a report for "+atnickname)
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    postslink = r.get(atnickname)
    if postslink != None:
        print("Set : already some values for "+atnickname+", adding one ?")
        response.status = 200
        enable_cors()
        response.headers['Access-Control-Allow-Origin'] = '*'
        linkpost = request.body.read().decode("utf-8")
        arrLink = json.loads(postslink)
        if linkpost in arrLink:
            print("Already in list.")
            return json.dumps("Already in list of reported posts.")
        else:
            arrLink.append(linkpost)
            r.set(atnickname, json.dumps(arrLink))
            return json.dumps("Link to post added (already reported)")
    else:
        print("Set : no value for "+atnickname+", adding one.")
        response.status = 200
        enable_cors()
        response.headers['Access-Control-Allow-Origin'] = '*'
        linkpost = request.body.read().decode("utf-8")
        r.set(atnickname, json.dumps([linkpost]))
        return json.dumps("Reported")
    
@get('/save/a97d9776e68a7f936ed8581a7c245e1c1234a43a')
def saveDB():
    r.save()
run(host='0.0.0.0', port=7776)

