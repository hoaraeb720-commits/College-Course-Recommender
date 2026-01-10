from flask import Flask, render_template, request
import pandas as pd

import src.extract as extract
import src.transform as transform
import src.recommender as recommender
from src.forms import CollegeForm


YEAR = 2023


def get_final_data():
    admissions_df = extract.get_ipeds_admissions(YEAR)
    institutions_df = extract.get_institutions(YEAR)

    admissions_df = transform.clean_column_names(df=admissions_df)
    institutions_df = transform.clean_column_names(df=institutions_df)

    final_admissions_df = transform.merge_dataframes(admissions_df, institutions_df)
    final_admissions_df = transform.calculate_admission_rate(final_admissions_df)
    return final_admissions_df


final_admissions_df = get_final_data()
final_admissions_df.to_csv("final_admissions_data.csv", index=False)

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
            gpa_df = recommender.passes_gpa_acceptance_filter(
                df=final_admissions_df, student_gpa=gpa
            )
            if which_test == "sat":
                college_rec_df = recommender.classify_schools(
                    final_admissions_df=gpa_df, sat_score=scores
                )
            else:
                college_rec_df = recommender.classify_schools(
                    final_admissions_df=gpa_df, act_score=scores
                )
            target: pd.DataFrame = college_rec_df.query(
                "`Admission Likelihood` == 'Target'"
            )
            reach: pd.DataFrame = college_rec_df.query(
                "`Admission Likelihood` == 'Reach'"
            )
            safety: pd.DataFrame = college_rec_df.query(
                "`Admission Likelihood` == 'Safety'"
            )
            target_college_information = target.to_records()
            reach_college_information = reach.to_records()
            safety_college_information = safety.to_records()

            return render_template(
                "college_results.html",
                target=target,
                major=major,
                scores=scores,
                gpa=gpa,
                awards=awards,
                which_test=which_test,
                target_college_information=target_college_information,
                reach_college_information=reach_college_information,
                safety_college_information=safety_college_information,
            )
        return render_template("home_page.html", form=form)

    return render_template("home_page.html", form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
