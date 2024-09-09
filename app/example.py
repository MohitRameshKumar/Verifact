from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Example Python function to process the video ID
def process_video_id(video_id):
    # Replace this with your actual Python code logic
    return f"Processed video with ID: {video_id}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    video_id = request.form['video_id']
    result = process_video_id(video_id)  # Pass the video ID to your Python function
    return jsonify({'output': result})

if __name__ == '__main__':
    app.run(debug=True)
