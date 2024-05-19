import json
from openai import OpenAI
from flask import Flask, jsonify, request

app = Flask(__name__)


def json_reader(file_name):
    with open(file_name) as f:
        file_json = json.load(f)
    return file_json


@app.route('/proforientation', methods=['POST'])
def get_prof_orientation():
    client = OpenAI(api_key=config['Authorization'],
                    organization=config['organization_id'],
                    project=config['project_id'])
    text = request.args.get('text')
    ai = AiAssistant(config, client)
    return ai.get_gpt_response(text)


class AiAssistant:
    def __init__(self, config, client: OpenAI):
        self.config = config
        self.client = client

    def get_gpt_response(self, msg):
        result = msg
        print(result)
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[
            {'role': 'system', 'content': config['gpt_system_context']}, {'role': 'user', 'content': msg}])
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


if __name__ == '__main__':
    config = json_reader("config.json")
    app.run(port='9000')
