from flask import Flask, render_template, request
from forms import CollegeForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "CollegeRecommenderSecretKey"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    form = CollegeForm()

    if request.method == "POST":
        if form.validate_on_submit():
            major = form.major.data
            scores = form.scores.data
            gpa = form.gpa.data
            awards = form.awards.data
            which_test = form.test_scores.data

            return render_template(
                "college_results.html",
                major=major,
                scores=scores,
                gpa=gpa,
                awards=awards,
                which_test=which_test,
            )
        return render_template("home_page.html", form=form)

    return render_template("home_page.html", form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
