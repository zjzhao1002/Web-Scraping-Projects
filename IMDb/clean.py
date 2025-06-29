import pandas as pd

df = pd.read_csv('imdb.csv', header=None)

df.columns = ["title", "year", "duration", "restriction", "rating", "votes"]

df[['ranking', 'title']] = df['title'].str.split(' ', n=1, expand=True)
df['ranking'] = df['ranking'].str.replace('.', '')

df['duration'] = df['duration'].apply(lambda x: "0h "+x if 'h' not in x else x)
df['duration'] = df['duration'].apply(lambda x: x+" 0m" if 'm' not in x else x)
df[['hour', 'minute']] = df['duration'].str.split('h', expand=True)

df['hour'] = df['hour'].str.replace('m', '')
df['hour'] = df['hour'].astype(int)
df['minute'] = df['minute'].str.replace('m', '')
df['minute'] = df['minute'].str.strip()
df['minute'] = df['minute'].astype(int)
df['duration (in Min)'] = df['hour'] * 60 + df['minute']
df = df.drop(columns=['duration', 'hour', 'minute'])

df["votes"] = df["votes"].str.replace(')', '')
df["votes"] = df["votes"].str.replace('(', '')
df['votes (in M)'] = df['votes'].apply(lambda x: x.replace('M','') if 'M' in x else '0')
df['votes (in M)'] = df['votes (in M)'].astype(float)
df['votes (in K)'] = df['votes'].apply(lambda x: x.replace('K','') if 'K' in x else '0')
df['votes (in K)'] = df['votes (in K)'].astype(float)
df['votes (in M)'] = df['votes (in M)'] + df['votes (in K)']/1000.0
df = df.drop(columns=['votes', 'votes (in K)'])

df = df[['ranking', 'title', 'year', 'duration (in Min)', 'restriction', 'rating', 'votes (in M)']]
print(df.head())

df.to_csv("imdb_clean.csv", index=False)