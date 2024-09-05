// Import the necessary libraries
const youtubeTranscript = require('youtube-transcript');
const { Configuration, OpenAIApi } = require('openai');

// OpenAI API setup
const configuration = new Configuration({
    apiKey: 'sk-HYcTc0b_nZlNappuK1gcH6GGWafP309D48eH43jK0hT3BlbkFJpIVTFCpmkOMFZ-8F8v54QH21309UgzLuNUzyCO8eAA', // Replace with your actual OpenAI API key
});
const openai = new OpenAIApi(configuration);

// Function to get transcript text only from a YouTube video
async function getTranscriptTextOnly(videoId) {
    try {
        const transcript = await youtubeTranscript.fetchTranscript(videoId);
        const textOnly = transcript.map(entry => entry.text);
        return textOnly;
    } catch (error) {
        console.error(`An error occurred: ${error}`);
        return null;
    }
}

// Function to call the OpenAI API with a prompt
async function getChatGPTResponse(prompt) {
    try {
        const response = await openai.createChatCompletion({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: prompt }],
            max_tokens: 150
        });
        return response.data.choices[0].message.content;
    } catch (error) {
        console.error(`Error: ${error}`);
        return `Error: ${error}`;
    }
}

// Main function
(async () => {
    const videoId = 'YH-KJWHKQ_0'; // Your YouTube video ID
    const transcriptText = await getTranscriptTextOnly(videoId);
    
    if (transcriptText) {
        const transcript = transcriptText.join('\n');
        
        const prompt = `Imagine you are a fact-checker for political debates. Analyze the chunk of text sent within the quotation marks and scan for complete ideas. These statements are from the Joe Biden vs. Donald Trump 2020 Presidential debate. Use your knowledge to determine if each complete idea is true or false. Output the sentence(s) you are checking and either “true” or “false”. Also include who said the statement. If it sounds like an opinion, output “opinion.” If the idea is just a general statement, output “general." \n${transcript}`;
        
        const response = await getChatGPTResponse(prompt);
        console.log(response);
    }
})();
