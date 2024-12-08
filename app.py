from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

# PostgreSQL database URL (replace with your own connection string)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://survey_app_o027_user:fen28ULl82ePmSJuMBE0DpffYYW6ZlRr@dpg-ctakkg0gph6c73epkvhg-a.oregon-postgres.render.com/survey_app_o027'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(255), nullable=False)
    question2 = db.Column(db.String(255), nullable=False)
    question3 = db.Column(db.String(255), nullable=False)

# Initialize database schema
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def survey():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    new_response = Response(
        question1=data['question1'],
        question2=data['question2'],
        question3=data['question3']
    )
    db.session.add(new_response)
    db.session.commit()
    return redirect(url_for('survey'))

@app.route('/admin')
def admin():
    responses = Response.query.all()
    
    # Generate Charts
    df = pd.read_sql_query("SELECT * FROM response", db.session.bind)
    
    pie_chart_path = 'static/pie_chart.png'
    os.makedirs('static', exist_ok=True)  # Ensure the static directory exists
    df['question2'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(6, 6))
    plt.title('Yes/No Responses')
    plt.savefig(pie_chart_path)
    plt.close()

    return render_template('admin.html', data=responses, pie_chart=pie_chart_path)

if __name__ == '__main__':
    app.run(debug=True)
