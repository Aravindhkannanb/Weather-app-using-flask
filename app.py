import requests
from flask import Flask,render_template,request,flash
from flask_mysqldb import MySQL
app=Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="Aravindh"
app.config["MYSQL_PASSWORD"]='12345'
app.config['MYSQL_DB']='weather'
app.config['SECRET_KEY']='12443'
mysql=MySQL(app)
@app.route("/",methods=["POST","GET"])
def home():
    con=mysql.connection.cursor()
    if request.method=="POST":
        city=request.form.get("city")
        con.execute("select city_name from city where city_name=%s",[city])
        res=con.fetchone()
        if(res[0]==city):
            flash("City already exist please try again")
        else:
        
            con.execute("insert into city(city_name)values(%s)",(city,))
            mysql.connection.commit()
        
    con.execute("select city_name from city")
    res=con.fetchall()
    weather_data=[]
    for i in res:
        url="https://api.openweathermap.org/data/2.5/weather?q={}&appid=48bca1e82e35a1604c8df325f1f2cdc5"
        r=requests.get(url.format(i[0])).json()
        weather={
        "city":i[0],
        "temperature":r['main']['temp'],
        "description":r["weather"][0]["description"],
        "icon":r["weather"][0]["icon"]
        }
        weather_data.append(weather)
    return render_template('weather.html',weather_data=weather_data)

if __name__=="__main__":
    app.run(debug=True,port=7000)