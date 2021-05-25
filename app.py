from flask import Flask, render_template, request
import psycopg2

connect = psycopg2.connect("dbname=sugang user=postgres password=postgres")
cur = connect.cursor()

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/register', methods=['POST'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]

    cur.execute("SELECT password FROM student where ID='{}'".format(id))
    result = cur.fetchall()
    if send == "로그인":
        if result:
            if password == result[0][0]:
                return render_template("login.html")
            else:
                return "잘못된 비밀번호"
        else:
            return "No Users Found"
    elif send == "회원가입":
        if result:
            return "학번 '{}' 가 이미 존재합니다.".format(id)
        else:
            cur.execute("INSERT INTO student VALUES ('{}', '{}', '컴퓨터학과', 0, '{}')".format(id, id, password))
            connect.commit()
            return "학번 '{}' 이 회원가입 되었습니다.".format(id)


if __name__=='__main__':
    app.run()

