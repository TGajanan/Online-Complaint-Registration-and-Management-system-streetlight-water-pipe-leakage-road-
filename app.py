from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import ibm_db
import re
import os
import ibm_boto3              #pip install ibm-cos-sdk in terminal
from ibm_botocore.client import Config, ClientError


app = Flask(__name__, template_folder='template')
app.secret_key = 'a'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA .crt;UID=fnc49721;PWD=oI8YaxBwwrliegJ9", '', '')
print("connected")


# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "7w01NqxV1GwsmQd49-X3eGUeePnL1JgZNhzYplxAo29q"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/267baef1483e4e7ea6114e4b9b941b65:bfdc12fb-3d5f-47a1-bc72-4f2cb1b959c3::"
# Create resource
cos = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)


@app.route("/", methods=['POST', 'GET'])
def dashboard():
    return render_template('indexold.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == "POST":
        USERNAME = request.form["username"]
        PASSWORD = request.form["password"]
        sql = "SELECT * FROM USERN WHERE USERNAME=? AND PASSWORD=?"  
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['USERID'] = account['USERID']
            session['USERNAME'] = account['USERNAME']
            msg = "logged in successfully !"
            return redirect(url_for('home'))
        else:
            msg = "Incorrect Email/password"
            return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)


@app.route("/register", methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST':
        USERNAME = request.form["username"]
        EMAIL = request.form["email"]
        PASSWORD = request.form["password"]
        ROLE = 0
        sql = "SELECT* FROM USERN WHERE EMAIL= ? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, EMAIL)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Your signup deatils are already exists in the database Please login"
            return render_template('signup.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', EMAIL):
            msg = "Invalid Email Address!"
        else:
            sql = "SELECT count(*) FROM USERN"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            length = ibm_db.fetch_assoc(stmt)
            print(length)
            insert_sql = "INSERT INTO USERN VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, length['1']+1)
            ibm_db.bind_param(prep_stmt, 2, ROLE)
            ibm_db.bind_param(prep_stmt, 3, USERNAME)
            ibm_db.bind_param(prep_stmt, 4, EMAIL)
            ibm_db.bind_param(prep_stmt, 5, PASSWORD)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully registered !"
            return render_template('login.html', msg=msg)

    return render_template('register.html', msg=msg)


@app.route("/admin_login", methods=['POST', 'GET'])
def admin_login():
    msg = ''
    if request.method == "POST":
        USERNAME = request.form["Username"]
        PASSWORD = request.form["password"]
        sql = "SELECT * FROM USERN WHERE USERNAME=? AND PASSWORD=?"  # from db2 sql table
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['USERID'] = account['USERID']
            session['USERNAME'] = account['USERNAME']
            msg = "logged in successfully !"
            return redirect(url_for('home'))
        else:
            msg = "Incorrect Email/password"
            return render_template('admin_login.html', msg=msg)
    return render_template('admin_login.html', msg=msg)


@app.route("/admin_register", methods=['POST', 'GET'])
def admin_register():
    msg = ''
    if request.method == 'POST':
        USERNAME = request.form["Username"]
        EMAIL = request.form["Email"]
        PASSWORD = request.form["password"]
        ROLE = request.form['role']
        secret_key = request.form["secret"]
        sql = "SELECT* FROM USERN WHERE USERNAME= ? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            secret_key == "12345"
            msg = "Your signup deatils are already exists in the database Please login"
            return render_template('signup.html')
        else:
            secret_key == "12345"
            sql = "SELECT count(*) FROM USERN"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            length = ibm_db.fetch_assoc(stmt)
            print(length)
            insert_sql = "INSERT INTO USERN VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, length['1']+1)
            ibm_db.bind_param(prep_stmt, 2, ROLE)
            ibm_db.bind_param(prep_stmt, 3, USERNAME)
            ibm_db.bind_param(prep_stmt, 4, EMAIL)
            ibm_db.bind_param(prep_stmt, 5, PASSWORD)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully registered !"
            return render_template('admin_login.html', msg=msg)

    return render_template('admin_register.html', msg=msg)


@app.route("/agent_login", methods=['POST', 'GET'])
def agent_login():
    msg = ''
    if request.method == "POST":
        USERNAME = request.form["Username"]
        PASSWORD = request.form["password"]
        sql = "SELECT * FROM USERN WHERE USERNAME=? AND PASSWORD=?"  # from db2 sql table
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['USERID'] = account['USERID']
            session['USERNAME'] = account['USERNAME']
            msg = "logged in successfully !"
            return redirect(url_for('home'))
        else:
            msg = "Incorrect Email/password"
            return render_template('agent_login.html', msg=msg)
    return render_template('agent_login.html', msg=msg)

@app.route("/agent_register", methods=['POST', 'GET'])
def agent_register():
    msg = ''
    if request.method == 'POST':
        USERNAME = request.form["Username"]
        EMAIL = request.form["Email"]
        PASSWORD = request.form["password"]
        ROLE = request.form['role']
        secret_key = request.form["secret"]
        sql = "SELECT* FROM USERN WHERE USERNAME= ? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            secret_key == "12345"
            msg = "Your signup deatils are already exists in the database Please login"
            return render_template('signup.html')
        else:
            secret_key == "12345"
            sql = "SELECT count(*) FROM USERN"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.execute(stmt)
            length = ibm_db.fetch_assoc(stmt)
            print(length)
            insert_sql = "INSERT INTO USERN VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, length['1']+1)
            ibm_db.bind_param(prep_stmt, 2, ROLE)
            ibm_db.bind_param(prep_stmt, 3, USERNAME)
            ibm_db.bind_param(prep_stmt, 4, EMAIL)
            ibm_db.bind_param(prep_stmt, 5, PASSWORD)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully registered !"
            return render_template('admin_login.html', msg=msg)

    return render_template('agent_register.html', msg=msg)        

@app.route('/home', methods=['POST', 'GET'])
def home():
    sql = "SELECT * FROM USERN WHERE USERID=" + str(session['USERID'])
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    User = ibm_db.fetch_tuple(stmt)
    print(User)
    print('data fetched')
    if User[1] == '0':
        if request.method == "POST":
            f = request.files['image']
            TITLE = request.form.get("title")
            DESCRIPTION = request.form.get("description")
            LAT = request.form.get("lat")
            LONG = request.form.get("lon")
            IMAGE_ID= '0'
            if(LAT == "" and LONG == ""):
                return render_template('homeuser.html', data=0)
            else:
                sql = "SELECT * FROM USERN WHERE USERID = " + str(session['USERID'])
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.execute(stmt)
                data = ibm_db.fetch_assoc(stmt)
                print(data)
                sql = "INSERT INTO TICKETS VALUES (?,?,NULL,?,?,NULL,?,?,?)"
                stmt1 = ibm_db.prepare(conn, sql)
                # print('stmt1')
                ibm_db.bind_param(stmt1, 1, data["USERID"])
                ibm_db.bind_param(stmt1, 2, data["USERNAME"])
                ibm_db.bind_param(stmt1, 3, TITLE)
                ibm_db.bind_param(stmt1, 4, DESCRIPTION)
                ibm_db.bind_param(stmt1, 5, LAT)
                ibm_db.bind_param(stmt1, 6, LONG)
                ibm_db.bind_param(stmt1, 7, IMAGE_ID)
                ibm_db.execute(stmt1)

                sql = 'SELECT * FROM TICKETS'
                stmt2 = ibm_db.prepare(conn, sql)
                ibm_db.execute(stmt2)
                data = ibm_db.fetch_assoc(stmt2)
                print(data)
                print("Latest USERID:", data)
                # data1 = str(data['USERID'])
                os.mkdir('userupload') 
                basepath=os.path.dirname(__file__) #getting the current path i.e where app.py is present
                #print("current path",basepath)
                filepath=os.path.join(basepath,'userupload','.jpg') #from anywhere in the system we can give image but we want that image later  to process so we are saving it to uploads folder for reusing
                #print("upload folder is",filepath)
                f.save(filepath)
                cos.upload_file(Filename= filepath, Bucket='complaints', Key= TITLE +'.jpg')
                # image.save(os.path.join("static/images", filename))
                print('data sent tô Object storage')
                return render_template("homeuser.html",data=True)

        return render_template("homeuser.html",user=User)

    elif User[1] =='Admin':
        select_sql = "SELECT * FROM TICKETS"
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(stmt)
            if not data:
                break 
            else:
                data['USERID'] = str(data['USERID'])
                data['IMAGE_ID'] = str(data['IMAGE_ID'])
                rows.append(data)
        print('rows: ', rows)
        sql="SELECT * FROM USERN WHERE ROLE='Electrician' or ROLE='Road-Contractor' or ROLE='Plumber' "
        stmt=ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        data1 = ibm_db.fetch_tuple(stmt)
        list=[]
        print(data1)
        while data1!= False:
            list.append(data1)
            data1 = ibm_db.fetch_tuple(stmt)
        print(list)
        return render_template('admin_newhome.html', rows=rows, user=User,user1=list )

    elif User[1] == 'Electrician': 
        select_sql = "SELECT * FROM TICKETS WHERE ASSIGNED='Electrician'"
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(stmt)
            if not data:
                break 
            else:
                data['USERID'] = str(data['USERID'])
                data['IMAGE_ID'] = str(data['IMAGE_ID'])
                rows.append(data)
        print('rows: ', rows)
        return render_template('admin_newhome.html', rows=rows, user=User)

    elif User[1] == 'Road-Contractor': 
        select_sql = "SELECT * FROM TICKETS WHERE ASSIGNED='Road-Contractor'"
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(stmt)
            if not data:
                break 
            else:
                data['USERID'] = str(data['USERID'])
                data['IMAGE_ID'] = str(data['IMAGE_ID'])
                rows.append(data)
        print('rows: ', rows)
        return render_template('admin_newhome.html', rows=rows, user=User)

    elif User[1] == 'Plumber': 
        select_sql = "SELECT * FROM TICKETS WHERE ASSIGNED='Plumber'"
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(stmt)
            if not data:
                break 
            else:
                data['USERID'] = str(data['USERID'])
                data['IMAGE_ID'] = str(data['IMAGE_ID'])
                rows.append(data)
        print('rows: ', rows)
        return render_template('admin_newhome.html', rows=rows, user=User)

    return render_template("homeuser.html",user=User)

@app.route('/delete_issue/<string:USERID>', methods = ['POST'])
def delete_issue(USERID):
    
    sql= "DELETE FROM TICKETS WHERE USERID=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, USERID)
    ibm_db.execute(stmt)
    print('item deleted')
    return redirect(url_for('home',data=1 ))


@app.route('/home/<string:USERID>', methods = ['POST'])
def update_status(USERID):

    if request.method == "POST":
        ASSIGNED = request.form.get('Agent')
        sql= "UPDATE TICKETS SET ASSIGNED=? WHERE USERID=" +str(USERID)
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, ASSIGNED)
        ibm_db.execute(stmt)
        print('update_status')

        update_sql="UPDATE TICKETS SET PROGRESS='assigned to agent' WHERE USERID=" +str(USERID)
        stmt=ibm_db.prepare(conn, update_sql)
        ibm_db.execute(stmt)
        return redirect(url_for('home', data=True))
    
@app.route('/viewcomplaints')
def viewcomplaints():
    global form1
    form1="https://form.jotform.com/223611887326460"
    
    sql = "SELECT * FROM TICKETS WHERE USERID=" +str(session['USERID'])
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    row = []
    while True:
        data = ibm_db.fetch_assoc(stmt)
        if not data:
            break
        else:
            data['USERID'] = str(data['USERID'])
            row.append(data)
    print('rows: ', row)
    return render_template("viewcompalints.html", rows=row, form=form1)
    

@app.route('/tickect_update/<string:USERID>', methods = ['POST'])
def tickect_update(USERID):

    if request.method == "POST":
        PROGRESS = request.form.get('Progress')
        f = request.files['image']
        IMAGE_ID = request.form.get("imageid")

        select_sql = "SELECT * FROM TICKETS"
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        lat=data['LAT']
        long=data['LONG']

        sql= "UPDATE TICKETS SET PROGRESS=?,IMAGE_ID=? WHERE USERID=" +str(USERID)
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, PROGRESS)
        ibm_db.bind_param(stmt, 2, IMAGE_ID)
        ibm_db.execute(stmt)
        os.mkdir('agentupload')
        basepath=os.path.dirname(__file__) #getting the current path i.e where app.py is present
        #print("current path",basepath)
        filepath=os.path.join(basepath,'agentupload','.jpg') #from anywhere in the system we can give image but we want that image later  to process so we are saving it to uploads folder for reusing
        #print("upload folder is",filepath)
        f.save(filepath)
        cos.upload_file(Filename= filepath, Bucket='complaints', Key= IMAGE_ID +'.jpg')
        # image.save(os.path.join("static/images", filename))
        print('data sent tô Object storage')
        return redirect(url_for('home', data=2, lat=lat, long=long))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('USERID', None)
    return render_template('indexold.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)




