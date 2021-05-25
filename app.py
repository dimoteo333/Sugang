from flask import Flask, render_template, request
import psycopg2

connect = psycopg2.connect("dbname=sugang user=postgres password=postgres")
cur = connect.cursor()

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")

if __name__=='__main__':
    app.run()

