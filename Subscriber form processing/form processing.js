// 1先安装所需的包：express, body-parser, fs, nodemailer, node-cron
// npm install express body-parser fs nodemailer node-cron

const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const nodemailer = require('nodemailer');
const cron = require('node-cron');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

let subscribers = [];

// 从文件加载订阅者列表（如果文件存在）
if (fs.existsSync('subscribers.json')) {
    subscribers = JSON.parse(fs.readFileSync('subscribers.json'));
}

// 处理表单提交
app.post('/subscribe', (req, res) => {
    const { name, grade, department, email, remarks } = req.body;
    const subscriber = { name, grade, department, email, remarks };
    subscribers.push(subscriber);
    fs.writeFileSync('subscribers.json', JSON.stringify(subscribers, null, 2));
    res.send('订阅成功！');
});

// 启动服务器
app.listen(3000, () => {
    console.log('服务器正在运行在 http://localhost:3000');
});
