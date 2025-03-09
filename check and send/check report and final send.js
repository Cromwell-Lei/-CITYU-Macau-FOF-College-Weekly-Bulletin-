const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'YOUR_EMAIL@gmail.com',
        pass: 'YOUR_EMAIL_PASSWORD',
    },
});

// 定时任务：每周五北京时间早晨六点生成周报内容
cron.schedule('0 6 * * FRI', async () => {
    const report = await generateWeeklyReport();

    // 发送周报到自己的邮箱进行审核
    await transporter.sendMail({
        from: 'YOUR_EMAIL@gmail.com',
        to: 'YOUR_EMAIL@gmail.com',
        subject: 'Weekly Report Review',
        html: report,
    });

    console.log('周报已发送到您的邮箱进行审核');
});

// 审核后发送周报到所有订阅者
async function sendWeeklyReportToSubscribers(report) {
    for (const subscriber of subscribers) {
        await transporter.sendMail({
            from: 'YOUR_EMAIL@gmail.com',
            to: subscriber.email,
            subject: 'City Finance Times Weekly Report',
            html: report,
        });
    }

    console.log('周报已发送到所有订阅者');
}
