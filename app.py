from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
# yaml.load(input, Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        state = userDetails['state']
        dist = userDetails['dist']
        mandal=userDetails['mandal']
        village=userDetails['village']
        msg=userDetails['msg']
        x=len(state)
        y=len(dist)
        z=len(mandal)
        a=len(village)
        b=len(msg)
        if x>0 and y>0 and z>0 and a>0 and b>0:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(state, dist,mandal,village,msg) VALUES(%s, %s,%s,%s,%s)",(state, dist,mandal,village,msg))
            mysql.connection.commit(),
            cur.close()
        else:
            return render_template("alert.html")
        return render_template('thanks.html')
        # return "<h1>Your Complaint has been sended to our Office We will Solve that issue As soon as possible</h1>"
    return render_template('FirstOne.html')
@app.route('/users',methods=['POST','GET'])
def users():
    if request.method=='POST':
        userIDDetails=request.form
        userid=userIDDetails['userid']
        password=userIDDetails['password']
        if userid=='uday' and password=='9941245026':
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT * FROM users")
            if resultValue > 0:
                userDetails = cur.fetchall()
            return render_template('users.html',userDetails=userDetails)
        else:
            return render_template("wrong.html")
    return render_template('valid.html')
if __name__ == '__main__':
    app.run(debug=True)
