from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import auth_bp
from app.models.user import User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('所有欄位皆為必填！', 'danger')
            return redirect(url_for('auth.register'))

        if User.get_by_email(email):
            flash('這個 Email 已經被註冊過了！', 'danger')
            return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)
        User.create(username=username, email=email, password_hash=password_hash)
        
        flash('註冊成功！請登入。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_by_email(email)
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email 或密碼錯誤！', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))
