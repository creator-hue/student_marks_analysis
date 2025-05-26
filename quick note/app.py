import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask,render_template,request,send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = {'csv'}

#creating a function to check wether the uplaoded file is csv or not

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

##route for the home page where user can uplaod csv file

@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        ##CHECK IF THE USER UPLAODED A FILE
        file = request.files['FILE']

        #if file exist and is a csv
        if file and allowed_file(file.filename):
            # Sexcuring the uplaoded file
            filename = secure_filename(file.filename)
            
            # defining file oath to save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            ## save the uplaoded file to the uplaods folder
            file.save(file_path)

            ##after savin the file process it and return results
            return analyze_file(file_path)
        
        ##if no file uplaoded render home page
    return render_template('home.html')
    

## function to analyze the csv file
def analyze_file(file_path):
    ##load thecsv file intoa pandas dataframe
    df  = pd.read_csv(file_path)

    ## CHEck is NAME and SCOre columns ar present in the file
    if 'Name' not in df.columns or 'Score' not in df.columns:
        return 'csv must contain Name and score columns.' 
    else:
        ##calculate basic statistics from the data using pandas
        total_students = len(df) #total number of students
        avg_score = df['Score'].mean() #average score of all students
        highest_score = df['Score'].max() ##high score
        lowest_score = df['Score'].min() #lowest score

        # Crreate a new figure for plotting charts
        plt.figure(figsize=(10,5))  ##lentgh of 10cm and height of 5cm


        #plot 1: BAr chart for student score
        plt.subplot(1,2,1) ## row and column of first graph
        plt.bar(df['Name'], df['Score'], color = 'blue') ## BAr chart with student names and scores
        plt.xlabel("Student name") # x axis label
        plt.ylabel("score") #y axis label
        plt.title('Student Scores')  ## chart title


        #plot 2: pie chart for grade distribution(failing, average, Execellent)
        plt.subplot(1,2,2) #second plot in 1x2 grid
        grade_distribution= pd.cut(df['Score'], bins = [0,5,70,100], labels =['Fail','Average', 'Excellent'])
        grade_dist_count = grade_distribution.value_counts()  ## count number of students in each category
        plt.pie(grade_dist_count, labels = grade_dist_count.index, autopct = '%1.1f%%', startangle = 90 ) ##pie_chart
        plt.title('Grade Distribution')  #pie chart title


        ##save  thechart as abimage in the static/ folder
        chart_path = os.path.join('static', 'chart.png')
        plt.tight_layout()  #adjust layout for better spacing
        plt.savefig(chart_path) #save the chart to chart.png
        plt.close() ##close the plot to free uo memory

        # REturn the resuts page with data and chart path
        return render_template('results.html',
                            total_students = total_students,
                            avg_score=avg_score,
                            highest_score=highest_score,
                            lowest_score=lowest_score,
                            chart_path= chart_path)


if __name__== '__main__':
    app.run(debug=True)
