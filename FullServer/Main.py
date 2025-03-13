from flask import Flask, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime
import secrets
import os
from flask_cors import CORS
import os

# 从环境变量中获取公网 IP 或域名
PUBLIC_IP = os.getenv('PUBLIC_IP', '#')

app = Flask(__name__)
CORS(app)  # 全局启用 CORS

# QQ 邮箱 SMTP 配置
SMTP_SERVER = '#' #smtp地址
SMTP_PORT = 465  # 使用 SSL 加密
EMAIL_ADDRESS = '#'  #  邮箱地址
EMAIL_PASSWORD = '#'  # 授权码

# 保存令牌和用户数据的文件
TOKEN_FILE = 'tokens.json'
USER_FILE = 'users.json'

# 生成验证令牌
def generate_token():
    return secrets.token_urlsafe(16)

# 保存令牌和用户数据
def save_token(email, token):
    try:
        # 如果文件不存在，创建一个空字典
        if not os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        # 读取现有数据
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            tokens = json.load(f)

        # 添加新令牌
        tokens[token] = email

        # 保存数据
        with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, ensure_ascii=False, indent=4)

        return True, "令牌保存成功！"
    except Exception as e:
        return False, f"令牌保存失败: {str(e)}"

# 保存用户数据
def save_user(email, name, grade, department, remarks, verified=False):
    try:
        # 如果文件不存在，创建一个空字典
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        # 读取现有数据
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)

        # 添加或更新用户数据
        users[email] = {
            'name': name,
            'grade': grade,
            'department': department,
            'remarks': remarks,
            'verified': verified
        }

        # 保存数据
        with open(USER_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

        return True, "用户数据保存成功！"
    except Exception as e:
        return False, f"用户数据保存失败: {str(e)}"

# 发送邮件
def send_email(to_email, subject, body):
    try:
        # 创建邮件对象
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject

        # 连接 SMTP 服务器
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:  # 使用 SSL 加密
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # 登录邮箱
            server.sendmail(EMAIL_ADDRESS, [to_email], msg.as_string())  # 发送邮件

        return True, "邮件发送成功！"
    except Exception as e:
        return False, f"邮件发送失败: {str(e)}"

# 验证令牌
def verify_token(token):
    try:
        # 读取令牌数据
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            tokens = json.load(f)

        # 查找令牌对应的邮箱
        if token in tokens:
            email = tokens[token]
            del tokens[token]  # 删除已使用的令牌
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                json.dump(tokens, f, ensure_ascii=False, indent=4)
            return True, email
        else:
            return False, "无效的令牌。"
    except Exception as e:
        return False, f"令牌验证失败: {str(e)}"

# 定义根路径路由，返回 index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 提供静态图片资源的路由
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# 处理表单提交的路由
@app.route('/submit', methods=['POST'])
def submit_form():
    # 获取表单数据
    form_data = {
        'name': request.form.get('name'),
        'grade': request.form.get('grade'),
        'department': request.form.get('department'),
        'email': request.form.get('email'),
        'remarks': request.form.get('remarks')
    }

    # 生成验证令牌
    token = generate_token()

    # 保存令牌和用户数据
    save_success, save_message = save_token(form_data['email'], token)
    if not save_success:
        return jsonify({"status": "error", "message": save_message}), 500

    # 保存用户数据（初始状态为未验证）
    save_user_success, save_user_message = save_user(
        form_data['email'],
        form_data['name'],
        form_data['grade'],
        form_data['department'],
        form_data['remarks'],
        verified=False
    )
    if not save_user_success:
        return jsonify({"status": "error", "message": save_user_message}), 500

    # 发送验证邮件
    verification_url = f"http://{PUBLIC_IP}:5000/verify?token={token}"
    email_success, email_message = send_email(
        form_data['email'],
        "请验证您的邮箱",
        f"请点击以下链接验证您的邮箱：\n{verification_url}"
    )
    if email_success:
        return jsonify({"status": "success", "message": "验证邮件已发送，请检查您的邮箱。"})
    else:
        return jsonify({"status": "error", "message": email_message}), 500

# 验证邮箱的路由
@app.route('/verify')
def verify_email():
    token = request.args.get('token')
    if not token:
        return "缺少令牌参数。"

    # 验证令牌
    verify_success, verify_message = verify_token(token)
    if verify_success:
        # 更新用户验证状态
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if verify_message in users:
            users[verify_message]['verified'] = True
            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4)

        # 发送确认订阅邮件
        email_success, email_message = send_email(
            verify_message,
            "订阅确认",
            "您已成功订阅《City Finance Times》。感谢您的订阅！"
        )
        if email_success:
            return "邮箱已验证成功，并已发送确认订阅邮件！"
        else:
            return f"邮箱已验证成功，但确认订阅邮件发送失败: {email_message}"  # 添加 else 分支
    else:
        return verify_message  # 返回验证失败信息

# 获取用户验证状态的路由
@app.route('/check-verification', methods=['POST'])
def check_verification():
    email = request.json.get('email')
    if not email:
        return jsonify({"status": "error", "message": "缺少邮箱参数。"}), 400

    try:
        # 读取用户数据
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)

        # 检查邮箱验证状态
        if email in users and users[email]['verified']:
            return jsonify({"status": "success", "verified": True})
        else:
            return jsonify({"status": "success", "verified": False})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)