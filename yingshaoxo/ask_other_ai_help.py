import http.client
import json

def ask_llama(input_text):
    conn = http.client.HTTPConnection("localhost", 5001)
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({
        "model": 'llama',
        #"stop_sequence": ["User:", "\nUser ", "\nYou: "],
        #"prompt": "User: " + input_text + "\nYou: ",
        "stop_sequence": ["{{[INPUT]}}", "{{[OUTPUT]}}"],
        "prompt": "{{[INPUT]}}" + input_text + "\n" + "{{[OUTPUT]}}",
        "max_context_length": 2048,
        "max_length": 512,
        "stream": False,
        "cache_prompt": True,
    })

    conn.request("POST", "/v1/api/generate", body=payload, headers=headers)
    response = conn.getresponse()

    if response.status == 200:
        data = response.read()
        data = json.loads(data.decode())
        response = data.get("response")
        if response:
            return response.strip()
        else:
            return "error: no response"
    else:
        return "error: HTTP {} request failed".format(response.status)
