from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from config import MYSQL_CONFIG
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

@app.route('/')
def survey():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO responses (question1, question2, question3) 
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (data['question1'], data['question2'], data['question3']))
    conn.commit()
    conn.close()
    return redirect(url_for('survey'))

@app.route('/admin')
def admin():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM responses", conn)
    conn.close()
    
    # Generate Charts
    pie_chart_path = 'static/pie_chart.png'
    df['question2'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(6, 6))
    plt.title('Yes/No Responses')
    plt.savefig(pie_chart_path)
    plt.close()

    return render_template('admin.html', data=df.to_dict(orient='records'), pie_chart=pie_chart_path)

if __name__ == '__main__':
    app.run(debug=True)
