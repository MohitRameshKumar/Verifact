from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import openai

app = Flask(__name__)

# Your OpenAI API key
openai.api_key = "sk-qZlGEXnebG2pvIsxzUKKRMSyow3Zrm3VsExJOlhmqMT3BlbkFJb07Eqo5TlxQElJbNckhxckUx0i819onFoiCGuNsYUA"

def get_transcript_text_only(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_only = [entry['text'] for entry in transcript]
        return "\n".join(text_only)
    except Exception as e:
        return None

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def index():
    return render_template('index.html')  # Serves your HTML form

@app.route('/process', methods=['POST'])
def process_video_id():
    video_id = request.form.get('video_id')
    
    if not video_id:
        return jsonify({'output': 'No video ID provided'}), 400
    
    transcript_text = get_transcript_text_only(video_id)
    
    if transcript_text is None:
        return jsonify({'output': 'Failed to fetch transcript'}), 500
    
    # ChatGPT prompt
    instruction = ("Imagine you are a fact-checker for political debates. Analyze the chunk of text sent within the quotation marks "
                   "and scan for complete ideas (these can be in one sentence or multiple sentences). These statements are from the "
                   "Joe Biden vs. Donald Trump 2020 Presidential debate. Use your knowledge to determine if each complete idea is true or false. "
                   "Output the sentence(s) you are checking and either 'true' or 'false'. Also include who said the statement. "
                   "If it sounds like an opinion, output 'opinion'. If the idea is just a general statement, output 'general'.")
    
    prompt = f"{instruction}\n'{transcript_text}'"
    
    chatgpt_response = get_chatgpt_response(prompt)
    
    return jsonify({'output': chatgpt_response})

if __name__ == '__main__':
    app.run(debug=True)
