// Please install OpenAI SDK first: `npm install openai`(在命令行安装该包，详见readme初始化教程)
//命令行（终端或控制台）中运行代码'npm init -y'以初始化npm项目
import OpenAI from "openai";

const openai = new OpenAI({
        baseURL: 'https://api.deepseek.com',
        apiKey: '<DeepSeek API Key>'
});
//下面这一段如何填写提示词？
async function generateWeeklyReport() {
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "你是一个专业的财经报刊记者，正在编写这周的周刊内容，你的读者偏好阅读相对精炼的文章和有数据支撑的内容，你编写的新闻旨在帮助读者最高效率的获取信息，他们不喜欢听废话。" }],
    model: "deepseek-chat",
  });
    const prompts = [
        '请你总结本周七天内以中国为主，世界其他地区为辅的世界金融市场动态。并分为两个板块1.中国动态和2.世界动态。请你阅读一些已有的财经新闻，并模仿雅虎财经进行写作。你的内容需要包括股市、货币（即外汇市场）、期货、黄金、债券这几个领域的内容。',
        '分点列出本周世界主要五大市场股市行情。',
        '分为板块1.澳门、2.内地及港台、3.国际经济，分别撰写每个板块200字以内的本周主要经济新闻摘要。注意内容不要和已有的内容重复。',
    ];

    const responses = await Promise.all(prompts.map(prompt => openai.createCompletion({
        model: 'text-davinci-002',
        prompt: prompt,
        max_tokens: 800,
    })));

    const report = `
        <h1>City Finance Times Weekly Report</h1>
        <h2>本周主要金融市场动态</h2>
        <p>${responses[0].data.choices[0].text}</p>
        <h2>本周世界股市行情</h2>
        <p>${responses[1].data.choices[0].text}</p>
        <h2>本周经济新闻</h2>
        <p>${responses[2].data.choices[0].text}</p>
        <h2>金融学院周动态</h2>
        <p>编辑内容...</p>
    `;

    return report;

  console.log(completion.choices[0].message.content);
}

generateWeeklyReport();
//以上是新更改的deepseek的api调用，有待debug
