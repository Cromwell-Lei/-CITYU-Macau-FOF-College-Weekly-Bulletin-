# 澳门城市大学金融学院周刊-《City Finance Times》
![示例图片](https://github.com/Cromwell-Lei/-CITYU-Macau-FOF-College-Weekly-Bulletin-/blob/main/bulletin%20title/学院周刊title-1.png)
澳门城市大学金融学院周刊-《City Finance Times》<br>
这是一个为澳门城市大学金融学院开发的周刊系统，旨在为读者提供最高效的市场信息获取渠道。能够每周生成周刊报道市场主要动态和相关新闻，以及学院内部的活动预告和其他相关栏目。本刊数据严谨，语言精炼。读者可以通过填写表单订阅，订阅后，每周五将通过邮件寄送本周周刊给读者。相关内容正在持续开发中。<br>
任何问题联系：1049888453macau@gmail.com<br>
[City Finance Times]:The Weekly Report of the Faculty of Finance, City University of Macau
This is a weekly report system developed for the Faculty of Finance of City University of Macau. It can generate a weekly report every week, covering the main market dynamics and related news, as well as activity previews and other relevant sections within the faculty. Readers can subscribe by filling out a form. After subscribing, the weekly report of the current week will be sent to readers via email every Friday. Relevant content is still under continuous development. <br>
For any questions, please contact: 1049888453macau@gmail.com<br>
# 预览
![示例图片](https://raw.githubusercontent.com/Cromwell-Lei/-CITYU-Macau-FOF-College-Weekly-Bulletin-/refs/heads/main/preview.png)
# 部署
文件[openai make content]和[deepseek make]两者选择一个安装部署，不可同时存在，后者代码有待改进<br>
**以下是本项目的部署方法，将按照步骤顺序展开描述**

## 克隆本项目到本地或服务器
```bash
//命令指示符运行
git clone https://github.com/Cromwell-Lei/-CITYU-Macau-FOF-College-Weekly-Bulletin-.git
```
## 部署前先在环境中初始化npm项目
```bash
//命令指示符运行
// 更改当前工作目录，将下面的路径更换为项目地址即可
cd "C:/Program Files/My Project"
//初始化npm项目，创建package.json文件
npm init -y
```
## 安装依赖项
```bash
//安装openai package
npm install openai
```

# 希望的改进方向
1.将生成的内容填入html中<br>
2.优化提示词，以更好的输出高质量内容<br>
3.新增学院活动预告板块<br>
4.demo设计：做一个demo版本的周刊。功能上，可以自行在html页面中输入想要获取信息的时间段，输入订阅邮箱。演示订阅、确认订阅功能和周刊生成和发送邮箱功能
<br>
