from flask import Flask, render_template_string, send_from_directory, redirect, request
from json import dumps
import requests


app = Flask(__name__)
clubs = ["cpu"]



def webhook(club, text, url=""):
     data = {
          'userame': club,
          'avatar_url': "http://school.return0927.xyz/img/cpu.banner_top.jpg",
          'tts': False,
          'embeds': [{'color':3447003, 'title': "{club} 동아리지원".format(club=club.upper()), 'description': 'Go', 'fields':[{'name':"Information", 'value':text, 'inline':False}], 'footer':{'text':'Github @return0927'}}],
     }

     return requests.post(url, data=dumps(data), headers={'Content-type':'multipart/form-data'})


@app.route("/club/<path:club>")
@app.route("/club/<path:club>/")
def home(club):
     if club not in clubs: return "Club Not found"

     return redirect("/club/{club}/apply".format(club=club))


@app.route("/club/<path:club>/apply")
def apply(club):
     if club not in clubs: return "Club Not found"

     return render_template_string( open("sources/{club}.apply.html".format(club=club), "r", encoding="UTF-8").read() )


@app.route("/club/<path:club>/submit", methods=["POST"])
def submit(club):
     if club not in clubs: return "Club Not found"
     try:
          ip = request.environ['REMOTE_ADDR']
          form = request.form
          name = form.get("name")
          grade, classroom, number = form.get("grade"), form.get("classroom"), form.get("number")
          phone = form.get("phone")
          email = form.get("email")

          text = """IP {} | Name {} | Basic {}G {}C {}N | Phone {} | Email {} \n""".format(ip, name, grade, classroom, number, phone, email)

          open("{club}.apply.txt".format(club=club), "a", encoding='UTF-8').write(text)
          webhook(club, text)

          return dumps({"message": "성공적으로 등록되었습니다!", "goto": request.url+"/../thanks"})

     except Exception as ex:
          return dumps({"err": True, "message": str(ex)})


@app.route("/club/<path:club>/thanks")
def thanks(club):
     if club not in clubs: return "Club Not found"

     return render_template_string( open("sources/thanks.html", "r", encoding="UTF-8").read(), club=club.upper() )


@app.route("/<path:rsc>/<path:filename>")
def resources(rsc, filename):
     return send_from_directory("sources/{rsc}".format(rsc=rsc), filename)



@app.route("/api/look_up")
def lookup():
     return send_from_directory("./", "cpu.apply.txt")
     #return open("cpu.apply.txt","r",encoding="UTF-8").read().replace("\n","<br/>")

app.run("0.0.0.0", 80, threaded=True, debug=True)
