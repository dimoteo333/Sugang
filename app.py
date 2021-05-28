from flask import Flask, render_template, url_for, request, redirect
import psycopg2

connect = psycopg2.connect("dbname=sugang user=postgres password=postgres")
cur = connect.cursor()

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/enter', methods=['GET', 'POST'])
def enter():
    return render_template("apply.html", student_id=student_id)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    course_id = request.form["course_id"]
    sec_id = request.form["sec_id"]
    send = request.form["send"]
    cur.execute("SELECT * from section where course_id='{}' and sec_id='{}'".format(course_id, sec_id))
    class_avilable = cur.fetchall()
    if class_avilable:
        cur.execute("SELECT * from takes where ID='{}' and course_id='{}' and sec_id='{}'".format(student_id, course_id, sec_id))
        take_class = cur.fetchall()
        if send == "수강신청":
            if take_class:
                return "이미 신청된 과목입니다."
            else:
                cur.execute("insert into takes values ('{}', '{}', '{}', 'Spring', 2021)".format(student_id, course_id, sec_id))
                cur.execute("update student set tot_cred = tot_cred + 3 where ID='{}'".format(student_id))
                connect.commit()
                return "{} 과목 {} 분반 수강신청이 완료되었습니다.".format(course_id, sec_id)
    else:
        return "존재하지 않는 과목번호입니다."

@app.route('/login', methods=['GET', 'POST'])
def login():
    cur.execute("SELECT tot_cred from student where ID='{}'".format(student_id))
    tot_credit = cur.fetchall()
    cur.execute("SELECT course_id, sec_id, semester, year from takes natural join student where ID='{}'".format(student_id))
    course_take = cur.fetchall()
    cur.execute("SELECT * from section")
    result = cur.fetchall()
    return render_template("login.html", sections=result, student_id=student_id, tot_credit=tot_credit[0][0], course_take=course_take)


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
                global student_id
                student_id = id
                return redirect(url_for('login'))
            else:
                return "잘못된 비밀번호입니다."
        else:
            return "유저가 확인되지 않습니다."
    elif send == "회원가입":
        if result:
            return "학번 '{}' 가 이미 존재합니다.".format(id)
        else:
            cur.execute("INSERT INTO student VALUES ('{}', '{}', '컴퓨터학과', 0, '{}')".format(id, id, password))
            connect.commit()
            return "학번 '{}' 이 회원가입 되었습니다.".format(id)


if __name__=='__main__':
    app.run()

