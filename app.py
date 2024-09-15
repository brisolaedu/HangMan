from flask import Flask, request, render_template, redirect, session
from function import get_word

app = Flask(__name__)
app.secret_key = '$abcdef'

tries = 0
start = 0
word = get_word()
display = list("_" * len(word))
words_try = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Start Page
@app.route("/", methods=["GET", "POST"])
def start():
    global tries
    global display
    global word
    global words_try
    global start

    display = list(display)

    if request.method == "POST":
        input = str(request.form.get('input')) 
        answer = ""

        answer += input.upper()

        if answer not in words_try:
            words_try.append(answer)

        for index in range(len(word)):
            if answer == word[index]:
                display[index] = answer
            elif display[index] == word[index]:
                display[index] = display[index]
            else:
                display[index] = "_"

        pictures = ["nothing", "head", "body", "arm1", "arm2", "leg1", "complete"]
        picture = pictures[tries] 

        display = ''.join(display)

        start = 1

        if display == word:
            tries = 0
            return redirect("/winner")

        elif answer in word:
            return render_template("hangman.html", start=start, words_try=words_try, name=picture, display=display)
        
        else:
            tries += 1
            picture = pictures[tries] 
            
            if picture == "complete":
                return redirect("/lost")
            
            return render_template("hangman.html", start=start, words_try=words_try, name=picture, display=display)



    else:
        return render_template("hangman.html", name="nothing")


# Winner Page
@app.route("/winner", methods=["GET", "POST"])
def winner():
    global word
    global display
    global tries
    global words_try
    global start

    word = get_word()
    display = list("_" * len(word))
    tries = 0
    start = 0
    words_try = []

    if request.method == "POST":
        if "back" in request.form:
            return redirect("/")
    else:
        return render_template("winner.html")
    

# Lost Page
@app.route("/lost", methods=["GET", "POST"])
def lost():
    global word
    global display
    global tries
    global words_try
    global start

    result = word

    word = get_word()
    display = list("_" * len(word))
    tries = 0
    start = 0
    words_try = []

    if request.method == "POST":
        if "back" in request.form:
            return redirect("/")
    else:
        return render_template("lost.html", result=result)
    

if __name__ == "__main__":
    app.run(debug=True)