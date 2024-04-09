from flask import Flask,render_template,request,flash
import pymongo

server=pymongo.MongoClient("mongodb://localhost:27017")

db=server['Payroll_management']

app=Flask(__name__)
app.secret_key = "abc"

@app.route("/")

def index():
    return render_template("index.html")

#User SignUp info Collection

user_info=db['user_info']

@app.route('/signup.html',methods=["GET","POST"])

def signup():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        cpassword=request.form['cpassword']
        if password==cpassword:
            data={"username":username,"password":password}
            user_info.insert_one(data)
        else:
            flash("PassWords Don't match")
        
    return render_template("signup.html")

#Employee Collection

emp=db['Employee']

@app.route("/existing.html",methods=['GET','POST'])

def employees():
    if request.method == 'POST':
        name=request.form['name']
        id=request.form['id']
        contact=request.form['contact']
        DOJ=request.form['DOJ']
        Address=request.form['address'] 
        dept=request.form['department']
        salary=request.form['salary']
        d_id = dept_db.find_one({'name':dept})

        data={'id':id,"name":name,'salary':salary,"DOJ":DOJ,'contact':contact,"address":Address,"dept_id":d_id['id']}
        emp.insert_one(data)

    data=dept_db.find({},{"name":1})
    return render_template("existing.html",data=data)


@app.route("/dropdown_login.html",methods=["GET","POST"])

def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        data=user_info.find_one({"username":username})
        if data['password'] == password:
            return render_template("adminpage.html")

    return render_template("dropdown_login.html")

#Department collection

dept_db=db['Department']
@app.route("/dept.html",methods=['GET','POST'])

def dept():
    
    if request.method == 'POST':
       name=request.form['name']
       id=request.form['id'] 
       Manager=request.form['Manager']  

       data={"id":id,"name":name,"Manager":Manager}

       dept_db.insert_one(data)
       
    return render_template("dept.html")


@app.route("/adminpage.html")

def admin():
    return render_template("adminpage.html")

@app.route("/emp_show.html")

def emshow():
    data=emp.find()
    return render_template("emp_show.html",data=data)

@app.route("/dept_show.html")

def dept_show():
    data=dept_db.find({},{})
    return render_template("dept_show.html",data=data)

@app.route('/update_emp.html',methods=['GET','POST'])

def emp_updt():
    if request.method == 'POST':
        key=request.form['id']
        value=request.form['attr']
        updated = request.form['val']
        data2=emp.find_one({'id':key})

        if data2['id'] != 'None':
            emp.update_one({"id":key},{"$set":{value:updated}})
            flash("Employee Data Updated")

            
    return render_template("update_emp.html")

@app.route('/update_dept.html',methods=['GET','POST'])

def dept_updt():
    if request.method == 'POST':
        key=request.form['id']
        value=request.form['attr']
        updated = request.form['val']
        d=dept_db.find_one({'id':key})

        if d['id'] != 'None':
            dept_db.update_one({"id":key},{"$set":{value:updated}})
            

    return render_template("update_dept.html")

@app.route('/remove_emp.html',methods=['GET','POST'])
def emp_remove():
    if request.method == 'POST':

        key=request.form['id']
        data=emp.find_one({'id':key})

        if data['id'] != 'None':
            emp.delete_one({"id":key})
            
        
    return render_template("remove_emp.html")

@app.route('/remove_dept.html',methods=['GET','POST'])

def r_dept():
    if request.method == 'POST':

        key=request.form['id']
        d=dept_db.find_one({'id':key})

        if d['id'] != 'None':
            dept_db.delete_one({"id":key})
            
        
    return render_template("remove_dept.html")


payr=db['payroll']

@app.route("/payroll.html",methods=['GET','POST'])

def payroll():

    if request.method == 'POST':
        id=request.form['e_id']
        dept=request.form['department']
        Wdays=request.form['PresentDays']
        bonus=request.form['Bonus']
        tax=request.form['Taxes']
        data={'e_id':id,"dept_name":dept,"PresentDays":Wdays,"Bonus":bonus,'Taxes':tax}
        payr.insert_one(data)

        name=get_employee_name(id)
        salary=get_employee_salary(id)
        x = 30 - int(Wdays)
        wage = 50*x
        tax_deduct = (int(tax)*int(salary))/100
        earn = int(salary) + int(bonus)
        deduct = int(wage) + int(tax_deduct)
        gross=int(salary)
        net=gross + int(bonus) - (wage + tax_deduct)
        return render_template("payslip.html",name=name,dept=dept,id=id,bonus=bonus,wage=wage,tax_deduct=tax_deduct,salary=salary,gross=gross,net=net,earn=earn,deduct=deduct)

    data=dept_db.find()
    e_id = emp.find()
    return render_template("payroll.html",data=data,e_id=e_id)

@app.route("/payslip.html",methods=['GET','POST'])

def payslip():

    coll1=emp.find()
    coll2=dept_db.find()
    return render_template("payslip.html",coll1=coll1,coll2=coll2)

def get_employee_name(employee_id):
    result = emp.find_one({'id': employee_id})
    if result:
        return result['name']
    else:
        return 'Employee not found'
    
def get_employee_salary(employee_id):
    result = emp.find_one({'id': employee_id})
    if result:
        return result['salary']
    else:
        return 'Employee not found'   
app.run(debug=True)
