import pandas as pd

"""
Some things to reconsider:
- Admission rate dominates for highly selective schools
    * Admission rate < 15% → Never "Safety"

- Only call a school “Safety” when BOTH are true:
  * Student score > 75th percentile
  * Admission rate > 30%

- Reach classification
* Admission rate < 15%, OR
* Student score < 25th percentile
"""


def classify_score(score: int, p25: int, p75: int, admission_rate: float) -> str:
    """
    Classify a score as 'Reach', 'Target', or 'Safety' based on 25th and 75th percentiles.
    """
    if admission_rate < 0.15:
        return "Reach"

    if score < p25:
        return "Reach"

    if score >= p75 and admission_rate > 0.30:
        return "Safety"

    return "Target"


def passes_gpa_acceptance_filter(df: pd.DataFrame, student_gpa: float) -> pd.DataFrame:
    """Filter dataframe based on student's GPA and institution's admission rate."""
    return df[
        df.apply(lambda row: gpa_acceptance_filter(row.ADM_RATE, student_gpa), axis=1)
    ]


def gpa_acceptance_filter(admission_rate: float, student_gpa: float) -> bool:
    """
    Determine if a student passes the GPA acceptance filter using a continuous model.

    admission_rate: 0.0 (very selective) to 1.0 (everyone admitted)
    """
    # Clamp admission_rate between 0 and 1 for safety
    admission_rate = max(0.0, min(1.0, admission_rate))

    # Continuous GPA threshold from 3.9 (hardest) down to 3.0 (easiest)
    required_gpa = 4.0 - admission_rate

    return student_gpa >= required_gpa


def calculate_sat_totals(df):
    """Add total SAT scores (25th, 50th, 75th percentiles) to the dataframe."""
    df = df.copy()
    df["SAT Total 25th"] = (
        df["SAT Verbal 25th Percentile"] + df["SAT Math 25th Percentile"]
    )
    df["SAT Total 50th"] = (
        df["SAT Verbal 50th Percentile"] + df["SAT Math 50th Percentile"]
    )
    df["SAT Total 75th"] = (
        df["SAT Verbal 75th Percentile"] + df["SAT Math 75th Percentile"]
    )
    return df


def classify_schools(final_admissions_df, sat_score=None, act_score=None):
    """
    Classifies schools into safety, target, or reach based on SAT or ACT score.
    """
    df = final_admissions_df.copy()

    if sat_score is not None:
        df = calculate_sat_totals(df)
        df["Admission Likelihood"] = df.apply(
            lambda row: classify_score(
                sat_score, row["SAT Total 25th"], row["SAT Total 75th"], row["ADM_RATE"]
            ),
            axis=1,
        )
    elif act_score is not None:
        df["Admission Likelihood"] = df.apply(
            lambda row: classify_score(
                act_score,
                row["ACT Composite 25th Percentile"],
                row["ACT Composite 75th Percentile"],
                row["ADM_RATE"],
            ),
            axis=1,
        )
    else:
        raise ValueError("You must provide either a SAT or ACT score.")

    return df.sort_values(
        by="Admission Likelihood",
        key=lambda x: x.map({"Reach": 0, "Target": 1, "Safety": 2}),
    )
