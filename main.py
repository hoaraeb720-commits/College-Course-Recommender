from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "GET":
        return render_template("home_page.html")

    if request.method == "POST":
        major = request.form.get("major")  # drop-down of valid majors
        scores = request.form.get("scores")  # 400-1600
        gpa = request.form.get("gpa")  # 0-4.0
        awards = request.form.get("awards")  # optional
        which_test = request.form.get("test_scores")
        
        return render_template(
            "college_results.html",
            major=major,
            scores=scores,
            gpa=gpa,
            awards=awards,
            which_test=which_test
        )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
