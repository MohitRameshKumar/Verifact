from youtube_transcript_api import YouTubeTranscriptApi
import openai


client = openai
openai.api_key =""




def get_transcript_text_only(video_id):
  try:
      transcript = YouTubeTranscriptApi.get_transcript(video_id)
      text_only = [entry['text'] for entry in transcript]
      return text_only
  except Exception as e:
      print(f"An error occurred: {e}")
      return None




video_id = 'YH-KJWHKQ_0'
transcript_text = get_transcript_text_only(video_id)
transcript = ''




if transcript_text:
  for text in transcript_text:
      transcript += text + "\n"


# Set up your OpenAI API key
 # Replace with your actual API key


# Function to get a response from ChatGPT
def get_chatgpt_response(prompt):
   try:
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=[{"role": "user", "content": prompt}],
           max_tokens=150
       )
       return response['choices'][0]['message']['content']
   except Exception as e:
       return f"Error: {e}"


# Take user input from the terminal
prompt = ("Imagine you are a fact-checker for political debates. Analyze the chunk of text sent within the quotation marks and scan for complete ideas. These statements are from the Joe Biden vs. Donald Trump 2020 Presidential debate. Use your knowledge to determine if each complete idea is true or false. Output the sentence(s) you are checking and either “true” or “false”. Also include who said the statement. If it sounds like an opinion, output “opinion.” If the idea is just a general statement, output “general." + "\n" + transcript)


# Get the ChatGPT response and print it
print(get_chatgpt_response(prompt))