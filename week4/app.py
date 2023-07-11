from flask import Flask
from flask import render_template
from flask import request 
import matplotlib.pyplot as plt

Student_data=open('data.csv','r')
n=Student_data.readline().strip('\n').split(',')
D=[]
l=[]
for j in range(len(n)):
  n[j]=n[j].strip(" ")
s=Student_data.readlines()
for line in s:
  l.append(line.strip('\n').split(","))
for elem in l:
  d={}
  for k in range(len(elem)):
    for i in range(len(n)):
      if i==k and i!=2:
        d[n[i]]=elem[k].strip(" ")
        break
      elif i==k and i==2:
        d[n[i]]=int(elem[k].strip(" "))
        break
  D.append(d)
sid1=[]
cid1=[]
for elem in D:
  for elems in elem:
    if elems=='Student id':
      sid1.append(elem[elems])
    if elems=='Course id':
      cid1.append(elem[elems])
sid=list(set(sid1))
cid=list(set(cid1))
Student_data.close()

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
      value1=request.form.get("ID")
      value2=request.form["id_value"]
      if (value1 is None) or value2=='':
        return render_template("wrong_data.html")  
      if value1=='student_id'and value2 in sid:
        return render_template("student_data.html",D=D,value2=value2)
      elif value1=='course_id' and value2 in cid:
        s=[]
        for i in D:
            if i["Course id"]==value2:
                s.append(i["Marks"])
            plt.hist(s)
            plt.xlabel("Marks")
            plt.ylabel("Frequency")
            plt.savefig(f"static/img.png")
            plt.clf()
        return render_template("course_data.html",D=D,value2=value2)
      else:
        return render_template("wrong_data.html")


if __name__=='__main__':
    app.debug=True
    app.run()

