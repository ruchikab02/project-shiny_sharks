# from crypt import methods
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
from peewee import *
# import requests
from playhouse.shortcuts import model_to_dict


load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"), 
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"), 
    port=3306)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb
        
mydb.connect()
mydb.create_tables([TimelinePost])

name = "Name"
experience_list = ["Experience 1", "Experience 2", "Experience 3"]
education_list = ["Education 1"]
hobby_list = ["Hobby 1", "Hobby 2", "Hobby 3", "Hobby 4"]


# Example for one person
# name = "Lauren Ciha"
# experience_list = ["Schloss Visual Reasoning Lab", "People and Robots Lab", "MLH Fellowship!"]
# education_list = ["University of Wisconsin-Madison"]
# hobby_list = ["reading", "journaling", "running"]

#Lauren
laurenExperience = ["Schloss Visual Reasoning Lab", "People and Robots Lab", "MLH Fellowship"]
laurenEducation = ["University of Wisconson-Madison"]
laurenHobbies = ["reading", "journaling", "running"]

#Ruchika
ruchikaExperience =["Fellow", "MLH Production Engineering Fellowship","Undergraduate Research Assistant,IUC","Math Tutor, Juni Learning"]
ruchikaEducation = ["University of Illinois at Urbana Champaign"]
ruchikaHobbies = ["drumming", "embroidery", "video games"]

#Sasha
sashaExperience = ["Fellow, MLH PE Fellowship", "Video Editor, McMaster Silhouette", "Make-Up Artist, Sephora"]
sashaEducation = ["McMaster University", "OCAD U"]
sashaHobbies = ["Photography", "Games", "Reading"]

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('homePage.html', title="Index Page", url=os.getenv("URL"))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homePage.html', title="Index Page", url=os.getenv("URL"))

@app.route('/sasha', methods=['GET', 'POST'])
def sasha():
    return render_template('sasha.html', title="Sasha Page", experience_list=sashaExperience, education_list=sashaEducation, hobby_list = sashaHobbies,url=os.getenv("URL"))

@app.route('/lauren', methods= ['POST', 'GET'])
def lauren():
    return render_template('lauren.html', title="Lauren",experience_list=laurenExperience, education_list=laurenEducation, hobby_list = laurenHobbies, url=os.getenv("URL"))

@app.route('/ruchika', methods= ['POST', 'GET'])
def ruchika():
    return render_template('ruchika.html', title="Ruchika Page", experience_list=ruchikaExperience, education_list=ruchikaEducation, hobby_list = ruchikaHobbies, url=os.getenv("URL"))

@app.route('/sample')
def template_test():
    return render_template('sample_page.html', name = name, experience_list=experience_list, education_list=education_list, hobby_list = hobby_list, url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():

    test_name = request.form.get('name')
    if test_name is None or test_name == "":
        return "Invalid name", 400
    else:
        name = request.form['name']

    test_email =  request.form.get('email')
    if "@" not in test_email or test_email is None:
        return "Invalid email", 400
    else:
        email = request.form['email']

    test_content = request.form.get('content')
    if test_content == "" or test_content is None:
        return "Invalid content", 400
    else:
        content =  request.form['content']       
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)
    
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    if request.method == 'POST':
        post_time_line_post()

    data = get_time_line_post()
    return render_template('timeline.html', title="Timeline", data=data)

if __name__ == '__main__':
    app.run(debug=True)
