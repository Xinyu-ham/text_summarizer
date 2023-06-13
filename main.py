from flask import Flask, render_template, request
from summarizer.util import Summarizer 
import os

app = Flask(__name__)
model_path = os.environ.get('MODEL_NAME', 'sentence-transformers_all-mpnet-base-v2')
summ = Summarizer(model_path=model_path)
print('Model loaded')

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template("index.html", output="None", original="")
    else:
        text = request.form['text']
        strength = float(request.form['strength']) /20
        
        summ.fit(text)
        summ.set_strength(strength)
        return render_template("index.html", output=summ.summarize(), original=text)
 
if __name__ == "__main__":
    app.run(debug=True)