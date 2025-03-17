const { Configuration, OpenAIApi } = require('openai');
const configuration = new Configuration({
    apiKey: 'YOUR_OPENAI_API_KEY',
});
const openai = new OpenAIApi(configuration);

async function generateWeeklyReport() {
    const prompts = [
        '请你总结本周七天内以中国为主，世界其他地区为辅的世界金融市场动态。并分为两个板块1.中国动态和2.世界动态。模仿雅虎财经进行写作。',
        '分点列出本周世界主要五大市场股市行情。',
        '分为板块1.澳门、2.内地及港台、3.国际经济，分别撰写每个板块200字以内的本周主要经济新闻摘要。',
    ];

 try {
        const responses = await Promise.all(prompts.map(async prompt => {
            const response = await openai.createCompletion({
                model: 'text-davinci-002',
                prompt: prompt,
                max_tokens: 500,
            });
            return response.data.choices[0].text.trim(); // 确保去除多余的空格
        }));


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
} catch (error) {
        console.error("Error generating report:", error);
        throw error;
    }
}

