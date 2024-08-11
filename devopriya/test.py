def llm_langhchain(string):
    import requests 
    import json
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type":"application/json"
    }
    
    data = {
        "model" : "llama2-uncensored",
        "prompt": string + " Provide the subject for this.",
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data  = json.loads(response_text)
        actual_response = data["response"]
        print("actual_response : ", actual_response)
        return actual_response
    
    else:
        print("error: ", response.status_code, response.text)
        
string = "this is a test message."       
llm_langhchain(string)