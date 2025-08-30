from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/')

def home():
    return render_template("Home.html")
@app.route("/welcome")
def welcome():
     return render_template("Welcome.html")
@app.route("/GETPOST",methods=['GET','POST'])
def getpost():
    if request.method =='POST':
      name=request.form['name']
      return  f'Hello,{name}!'
    return render_template("GETPOST.html")
if __name__== "__main__":
  app.run(debug=True)