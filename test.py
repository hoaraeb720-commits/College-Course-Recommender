import pandas as pd
df = pd.read_csv("https://waf.cs.illinois.edu/discovery/course-catalog.csv")
df.to_csv("illinois_dataset.csv",index = False)
