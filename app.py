# importing Flask and other modules
from flask import Flask, request, render_template,url_for,flash,session
import commons, constants
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from distutils.util import strtobool
import MySQLdb.cursors
import re

# from sqlalchemy import text
# import dao

# Flask constructor
app = Flask(__name__)

app.config['MYSQL_HOST'] = constants.HOST
app.config['MYSQL_USER'] = constants.USERNAME
app.config['MYSQL_PASSWORD'] = constants.PASSWORD
app.config['MYSQL_DB'] = constants.DB_NAME
app.secret_key='SECRET KEY'
mysql = MySQL(app)

#our code


#login-signup


@app.route('/', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('form.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user  VALUES(NULL, %s,%s,%s)', (userName, email, password,))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('signup.html', mesage = mesage)







@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='POST':
        #fetch data
        userDetails=request.form
        PostName=userDetails['PostName']
        FullName=userDetails['FullName']
        DOB=userDetails['DOB']
        Age=userDetails['Age']
        Email=userDetails['Email']
        Mobile_Number=userDetails['Mobile_Number']
        fpref=userDetails['fpref']
        spref=userDetails['spref']
        tpref=userDetails['tpref']
        qual=userDetails['qual']
        deg=userDetails['deg']
        deg1=userDetails['deg1']
        speci=userDetails['speci']
        speci1=userDetails['speci1']
        speci2=userDetails['speci2']
        speci3=userDetails['speci3']
        Percentage=userDetails['Percentage']
        desg=userDetails['desg']
        other=userDetails['other']
        qexperience=userDetails['qexperience']
        skills=userDetails['skills']
        expertise=userDetails['expertise']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO candidates(PostName,FullName,DOB,Age,Email,Mobile_Number,Preferences,Qualification,Degree,Specialisation,Percentage,Designation,QualifyingExperience,Skills,other_expertise)VALUES(%s,%s,%s,%s,%s,%s,concat(%s,%s,%s),%s,concat(%s,%s),concat(%s,%s,%s,%s),%s,concat(%s,%s),%s,%s,%s)',(PostName,FullName,DOB,Age,Email,Mobile_Number,fpref,spref,tpref,qual,deg,deg1,speci,speci1,speci2,speci3,Percentage,desg,other,qexperience,skills,expertise, ))
        mysql.connection.commit()
        cur.close()
        return 'successfully submitted!!!'
    return render_template('form.html')


@app.route("/index/admin/view")
def view():
    cur=mysql.connection.cursor()
    resultvalue=cur.execute("SELECT * FROM candidates")
    if resultvalue>0:
        userDetails=cur.fetchall()
        return render_template('adminview.html',userDetails=userDetails)

@app.route("/admin")
def admin():
    cur=mysql.connection.cursor()
    cur1=mysql.connection.cursor()
    cur2=mysql.connection.cursor()
    cur3=mysql.connection.cursor()
    cur4=mysql.connection.cursor()
    cur1.execute("SELECT  count(*) FROM candidates")
    cur2.execute("SELECT  count(*) FROM candidates where status='approved'")
    cur3.execute("SELECT  count(*) FROM candidates where status='pending'")
    cur4.execute("SELECT  count(*) FROM candidates where status='not approved'")
    allapplicants=cur1.fetchone()
    approvedapplicants=cur2.fetchone()
    pendingapplicants=cur3.fetchone()
    notapprovedapplicants=cur4.fetchone()
    
    resultvalue=cur.execute("SELECT * FROM candidates order by ApplicantID DESC limit 8")
   
    if resultvalue>0 :
        userDetails=cur.fetchall()
      
        

    
        return render_template('admin.html',userDetails=userDetails,allapplicants=allapplicants,approvedapplicants=approvedapplicants,pendingapplicants=pendingapplicants,notapprovedapplicants=notapprovedapplicants)


@app.route('//admin/approval')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM candidates")
    userDetails=cur.fetchall()
    cur.close()

    return render_template('formapproval.html', userDetails=userDetails)
    
    
 


@app.route('/admin/approval/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM candidates WHERE ApplicantID=%s", [id_data])
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route("/admin/approval/edit/<string:id>",methods=['GET','POST'])
def editUser(id):
    cur=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        sql="update candidates set status=%s where ApplicantID=%s"
        cur.execute(sql,[name,id])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("Index"))
        cur=mysql.connection.cursor()
    sql="select * from candidates where ApplicantID=%s"
    cur.execute(sql,[id])
    res=cur.fetchone()
    return render_template('edituser.html',datas=res)


@app.route('/admin/logout')
def logingout():
    return redirect('/')





# A decorator used to tell the application
# which URL is associated function
@app.route('/admin/filter', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        post_name = request.form.get("Post_Name")
        print(post_name)
        age = request.form.get("Age")
        preferences = request.form.get("Preferences")
        min_degree = request.form.get("Min_Degree")
        max_degree = request.form.get("Max_Degree")
        specialisation = request.form.getlist("Specialisation")
        percentage = request.form.getlist("Percentage")
        designation = request.form.getlist("Designation")
        print(designation[0])
        #print(designation[1])
        #responsibilities = request.form.get("Responsibilities")
        total_experience = request.form.getlist("Total_Experience")
        print("experience...")
        skills = request.form.get("Skills")
        skills_exp = request.form.get("Experience_in_Skill")
        
        #print(skills_exp[0])
        cursor = mysql.connection.cursor()
        #fetch_skill_range_query = "select * from skillExp"
        #cursor.execute(fetch_skill_range_query)
        #skill_range_data = cursor.fetchall()
        #print(skill_range_data)
        # get constraints
        query = commons.get_applicant_ids_query_as_per_skill(skills)
        exp_applicant_ids = []
        if len(query) > 0:
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            applicant_ids =[]
            for row in result:
                applicant_ids.append(row[0])
            exp_query = commons.filter_applicant_ids_as_per_skill_exp(skills_exp)
            print(exp_query)
            if len(exp_query) > 5:
                cursor.execute(exp_query)
                result = cursor.fetchall()
                for row in result:
                    exp_applicant_ids.append(row[0])
        common_applicant_ids = set(applicant_ids) 
        if len(exp_applicant_ids) > 0:
            common_applicant_ids = set(applicant_ids).intersection(set(exp_applicant_ids))
        #print(common_applicant_ids)
        query1 = commons.get_filter_query(post_name, age, preferences, min_degree, max_degree, specialisation,
                                         percentage, designation,  total_experience) #responsibilities,
        print(query1)
        cursor.execute(query1)
        result = cursor.fetchall()
        if len(result) == 0:
           result_html_code = '<html><h1 align=center>No records found. Please reduce the constraints</h1></html>'
        #write under else
        else:
            selected_applicant_ids = []
            for row in result:
                selected_applicant_ids.append(row[0])
            common_applicant_ids = set(common_applicant_ids).intersection(set(selected_applicant_ids))
            print(common_applicant_ids)
            field_map = {1: 'Applicant_Id', 3: 'Post_Name', 4: 'Full_Name', 6: 'Age', 9: 'Preferences', 10: 'Qualification',
                         11: 'Degree',
                         13: 'Percentage', 14: 'Designation', 15: 'Qual_Experience',
                         16: 'Skills_with_exp(months)'}  # 43: 'Responsibilities',
            result_html_code = '<html>'
            if len(common_applicant_ids) == 0:
                print("No records found. Please reduce the constraints")
                result_html_code = result_html_code + '<h1 align=center>No records found. Please reduce the constraints</h1>'
            else:
                result_html_code = result_html_code + '<h1 align=center>Filtered Records</h1><table border=2><tr><th>S.No.</th>'
                for key in field_map:
                    result_html_code = result_html_code + '<th>' + field_map[key] + '</th>'
                result_html_code = result_html_code + '</tr>'
                result_html_code = result_html_code + '<tr>'
                #final_query = "Select * from cdacdatabase.candidates where "
                final_query = "Select * from recruit.candidates where "
                for applicant_id in common_applicant_ids:
                    final_query = final_query + "ApplicantId = "+str(applicant_id)+" or "
                final_query = final_query[:final_query.rfind("or")] + ";"
                print(final_query)
                cursor.execute(final_query)
                result = cursor.fetchall()
                print(result)
                count = 0
                for row in result:
                    count = count + 1
                    result_html_code = result_html_code + '<td>' + str(count) + '</td>'
                    for key in field_map.keys():
                        if key == 16:
                            skill_with_exp = str(row[key-1]).replace(" -",":")
                            result_html_code = result_html_code + '<td>' + skill_with_exp + '</td>'
                        else:
                            result_html_code = result_html_code + '<td>' + str(row[key - 1]) + '</td>'
                    result_html_code = result_html_code + '</tr><tr>'
                ind = result_html_code.rfind('<tr>')
                result_html_code = result_html_code[:ind]
            result_html_code = result_html_code + '</table></html>'
            show_result(result_html_code)
            cursor.close()
        #ELSE ENDS
        return render_template("table.html", tables=[result_html_code], titles=[''])
    return render_template("guestFacultyfilter.html")




@app.route('/table', methods=["GET", "POST"])
def show_result(result_html_code):
    return render_template("table.html", tables=[result_html_code], titles=[''])


if __name__ == '__main__':
    app.run(debug=True)
