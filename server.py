from flask import Flask, request, jsonify
from flask_cors import CORS

from google import genai
import time
import os

def parse_subject_body(s: str) -> tuple[str, str]:
    if "|" in s:
        subject, body = s.split("|", 1)  # split only on first |
        return subject.strip(), body.strip()
    else:
        return "", s.strip()  # fallback: no subject

app = Flask(__name__)
CORS(app)  # ← very important for chrome extension


@app.route('/rewrite', methods=['POST'])
def rewrite_email():
    data = request.get_json()

    style = data.get('style', '')
    body = data.get('body', '')
    subject = data.get('subject', '')
    emailchain = data.get('emailchain', '')

    print("SUBJECT: " + subject)
    print("USER BODY: " + body)
    print("EMAIL CHAIN BODY: " + emailchain)
    

    useAI = False
    parse = """Hook, Line, and Sinker | I’ve officially decided my life is lacking a certain... splash. Since you’re the best at making my world better, I think you should be the one to find me a finned friend. I’m not saying I’m fishing for a gift, but I’d definitely be hooked on you if you brought one home.  """


    

    if useAI:
        client = genai.Client(api_key=os.environ["GENAI_KEY"])
        prompt = f"Write the subject of the email at the start separated by a | the body write it nicer: {body} in a deeply {style} way, no fill boxes like [your name]"
        if emailchain != "no email chain":
            prompt = f"Write the subject of the email at the start separated by a | the body write it nicer: {body} in a deeply {style} way, no fill boxes like [your name], using the following as context: {emailchain}"
        
            


        
        print(prompt)
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents= prompt,
        )
        
        parse = response.text
        print(parse)
       
    else:
        time.sleep(2)
    
    
    


    
    new_subject, new_body = parse_subject_body(parse)

    return jsonify({
        "body": new_body,
        "subject": new_subject
    })



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))





