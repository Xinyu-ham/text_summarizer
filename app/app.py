from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template("index.html", output="None", original="")
    else:
        text = request.form['text']
        return render_template("index.html", output=text.split('.')[0], original=text)

if __name__ == "__main__":
    app.run(debug=True)