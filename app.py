from flask import Flask,render_template,session,redirect,url_for,request
import mysql.connector


# from ai_engine import ai_response
from ai_engine import classify_message, generate_ai
import random
import time


app=Flask(__name__)
app.secret_key = "supersecretkey123"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="lokesh@1976",
        database="mental_health_db",
        auth_plugin="mysql_native_password",
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci"
    )

@app.route('/',methods=['POST','GET'])
def register():
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
            (name, email, password))
            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('login'))
        return render_template('index.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')

        # Generate OTP
        otp = random.randint(1000, 9999)

        
        session['otp'] = otp
        session['otp_expiry'] = time.time() + 120  
        session['email'] = email

        print("Generated OTP:", otp)  

        return redirect('/otp')

    return render_template('forgot_password.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        user_otp = request.form.get('otp')

        if time.time() > session.get('otp_expiry', 0):
            return "OTP expired. Please try again."

        if str(session.get('otp')) == str(user_otp):
            return redirect('/reset')

        return "Invalid OTP. Try again."

    return render_template('otp.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        new_password = request.form.get('password')
        email = session.get('reset_email')   # stored earlier

        if not email:
            return "Session expired. Try again."

        # Use your get_db() function
        conn = get_db()
        cur = conn.cursor()

        query = "UPDATE users SET password=%s WHERE email=%s"
        cur.execute(query, (new_password, email))

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('reset_password.html')

@app.route('/about')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/meditate')
def meditate():
    return render_template("meditation.html")

@app.route('/well')
def well():
    return render_template("mental_wellness.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email == "admin@gmail.com" and password == "123456":
            session['admin'] = True
            return redirect('/admin')

        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect('/chat')
    return render_template('login.html')

messages = []

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect('/')

    uid = session['user_id']

    if request.method == 'POST':
        user_msg = request.form.get('message')

        if user_msg:
            mode = classify_message(user_msg)
            ai_reply = generate_ai(user_msg, mode)

            
            messages.append({"sender": "user", "text": user_msg})
            messages.append({"sender": "bot", "text": ai_reply})

            
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO history (user_id, user_message, ai_reply) VALUES (%s, %s, %s)",
                (uid, user_msg, ai_reply)
            )
            conn.commit()
            cur.close()
            conn.close()

        return redirect('/chat')

    
    return render_template('chat.html', messages=messages)



@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT id, user_message, ai_reply, created_at 
        FROM history 
        WHERE user_id = %s 
        ORDER BY created_at DESC
    """, (session['user_id'],))

    history = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('history.html', history=history)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM history WHERE id = %s AND user_id = %s",
                (id, session['user_id']))

    conn.commit()

    cur.close()
    conn.close()

    return redirect('/history')

@app.route('/admin')
def admin_page():
    if 'admin' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, email from users ORDER BY id ASC")
    users = cur.fetchall()
    total_users = len(users)
    
    # cur.execute("SELECT id, user_id, user_message,created_at from history ORDER BY id ASC")
    cur.execute("""
        SELECT 
            users.id AS user_id,
            users.name,
            users.email,
            history.user_message,
            history.ai_reply,
            history.created_at
        FROM users
        LEFT JOIN history 
        ON users.id = history.user_id
        ORDER BY history.created_at DESC
    """)
    history = cur.fetchall()
    
    cur.execute("SELECT COUNT(*) AS total_chats FROM history")
    total_chats = cur.fetchone()['total_chats']

    cur.execute("SELECT COUNT(*) AS todays_chats FROM history WHERE DATE(created_at) = CURDATE()")
    todays_chats = cur.fetchone()['todays_chats']
    cur.close()
    conn.close()

    return render_template('admin.html', users=users,total_users=total_users,total_chats=total_chats,todays_chats=todays_chats,history=history)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    # Delete user from DB
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/admin')



# @app.route('/view_user/<int:user_id>', methods=['POST'])
# def view_user(user_id):
#     conn = get_db()
#     cur = conn.cursor(dictionary=True)

#     cur.execute("""
#         SELECT users.name, history.user_id, history.user_message, history.created_at
#         FROM history
#         JOIN users ON history.user_id = users.id
#         WHERE users.id = %s
#         ORDER BY history.id DESC
#     """, (user_id,))

#     user_chats = cur.fetchall()
#     cur.close()
#     conn.close()

#     return render_template("user_chat.html", user_chats=user_chats)

@app.route('/user_history/<int:user_id>')
def user_history(user_id):
    cur = mysql.connection.cursor(dictionary=True)

    # Fetch user
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    # Fetch user chat history
    cur.execute("SELECT * FROM history WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    user_chats = cur.fetchall()

    return render_template("user_history.html", user=user, user_chats=user_chats)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)