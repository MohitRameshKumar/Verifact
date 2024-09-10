from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import openai

app = Flask(__name__)

# Your OpenAI API key
openai.api_key = ""

def get_transcript_text_only(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_only = [entry['text'] for entry in transcript]
        return "\n".join(text_only)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in OpenAI request: {e}")
        return f"Error: {e}"

@app.route('/')
def index():
    return render_template('index.html')  # Serves your HTML form

@app.route('/process', methods=['POST'])
def process_video_id():
    video_id = request.form["video_id"] 


    
    if not video_id:
        return jsonify({'output': 'No video ID provided'}), 400
    
    print(f"Received video ID: {video_id}")
    
    transcript_text = get_transcript_text_only(video_id)
    
    if transcript_text is None:
        return jsonify({'output': f'Failed to fetch transcript for video ID: {video_id}'}), 500
    
    # ChatGPT prompt
    instruction = ("Imagine you are a fact-checker for political debates. Analyze the transcript sent between the quotation marks '' and look for sentences with complete ideas. Using your knowledge, check if the complete idea is true, false, an opinion, or a general statement. Give me the output in the form of 'Speaker: Sentences that form the complete idea (if it is true, false, general, or opinion)'. This transcript is from the 2020 presidential debate from biden and trump.")
    
    prompt = f"{instruction}\n'{transcript_text}'"
    
    chatgpt_response = get_chatgpt_response(prompt)
    
    return jsonify({'output': chatgpt_response})

if __name__ == '__main__':
    app.run(debug=True)
