def clean_column_names(df):
    df.columns = df.columns.str.strip()
    return df


def merge_dataframes(admissions_df, institutions_df):
    return (
        admissions_df[
            [
                "UNITID",
                # SAT scores
                "SATVR25",
                "SATVR50",
                "SATVR75",
                "SATMT25",
                "SATMT50",
                "SATMT75",
                # ACT Composite
                "ACTCM25",
                "ACTCM50",
                "ACTCM75",
                # ACT English
                "ACTEN25",
                "ACTEN50",
                "ACTEN75",
                # ACT Math
                "ACTMT25",
                "ACTMT50",
                "ACTMT75",
                "ADMSSN",
                "APPLCN",
            ]
        ]
        .merge(
            institutions_df[
                [
                    "UNITID",
                    "INSTNM",
                    "IALIAS",
                    "ADDR",
                    "CITY",
                    "STABBR",
                    "ZIP",
                    "WEBADDR",
                    "ADMINURL",
                    "FAIDURL",
                    "APPLURL",
                ]
            ],
            on="UNITID",
            how="left",
        )
        .rename(
            columns={
                "UNITID": "Institution ID",
                "INSTNM": "Institution Name",
                "ADDR": "Address",
                "CITY": "City",
                "STABBR": "State",
                "ZIP": "ZIP Code",
                "WEBADDR": "college_url",
                "ADMINURL": "admission_url",
                "FAIDURL": "financial_aid_url",
                "APPLURL": "application_url",
                # SAT scores
                "SATVR25": "SAT Verbal 25th Percentile",
                "SATVR50": "SAT Verbal 50th Percentile",
                "SATVR75": "SAT Verbal 75th Percentile",
                "SATMT25": "SAT Math 25th Percentile",
                "SATMT50": "SAT Math 50th Percentile",
                "SATMT75": "SAT Math 75th Percentile",
                # ACT Composite
                "ACTCM25": "ACT Composite 25th Percentile",
                "ACTCM50": "ACT Composite 50th Percentile",
                "ACTCM75": "ACT Composite 75th Percentile",
                # ACT English
                "ACTEN25": "ACT English 25th Percentile",
                "ACTEN50": "ACT English 50th Percentile",
                "ACTEN75": "ACT English 75th Percentile",
                # ACT Math
                "ACTMT25": "ACT Math 25th Percentile",
                "ACTMT50": "ACT Math 50th Percentile",
                "ACTMT75": "ACT Math 75th Percentile",
            }
        )
        .dropna()
    )


def calculate_admission_rate(final_admissions_df):
    return final_admissions_df.assign(ADM_RATE=lambda df: df.ADMSSN / df.APPLCN)
