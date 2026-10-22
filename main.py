import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('images', exist_ok=True)
sns.set_theme(style='whitegrid')

def save(name):
    plt.tight_layout()
    plt.savefig(f'images/{name}.png', dpi=150)
    plt.close()

df = pd.read_csv('data/netflix_titles.csv')
print(df.shape )
print(df.isnull().sum())

for col in ['director', 'cast', 'country']:
    df[col]= df[col].fillna('Unknown')
df = df.dropna(subset=['date_added','rating', 'duration']).copy()

df['date_added'] = pd.to_datetime(df['date_added'].str.strip(),errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()


plt.figure(figsize=(6,4))
sns.countplot(x='type', data= df  )
plt.title('Movies vs TV shows on Netflix')
save('type_counts')

added= df.groupby(['year_added','type']).size().unstack(fill_value=0)
added.plot(kind='line' , marker = 'o', figsize=(9,5))
plt.title('Titles Added to Netflix per Year')
plt.xlabel('Year added')
plt.ylabel('Number of titles')
save('added_per_year')


countries = df['country'].str.split(',').explode().str.strip()
countries = countries[~countries.isin(['Unknown', ''])]
top_countries= countries.value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_countries.values, y=top_countries.index , color='#b20710')
plt.title('Top 10 Countries by Number of Titles')
plt.xlabel('Number of titles')
save('top_countries')

genres = df['listed_in'].str.split(',').explode().str.strip()
top_genres = genres.value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_genres.values , y=top_genres.index, color='#221f1f')
plt.title('Top 10 Genres')
plt.xlabel('Number of titles')
save('top_genres')

movies = df[df['type']=='Movie'].copy()
movies['minutes']= movies['duration'].str.replace(' min', '', regex=False).astype(int)
plt.figure(figsize=(8,5))
sns.histplot(movies['minutes'], bins=30)
plt.title('Movie Duration Distribution')
plt.xlabel('Minutes')
save('movie_duration')

plt.figure(figsize=(9,5))
order= df['rating'].value_counts().index
sns.countplot(x='rating', data= df , order=order)
plt.xticks(rotation =45)
plt.title('Content Ratings')
save('ratings')

print('\n--- INSIGHTS ---')
print('Movie share: %.1f%%' % (100 * (df['type'] == 'Movie').mean()))
print('Peak year for additions:', df['year_added'].value_counts().idxmax())
print('Top country:', top_countries.index[0], top_countries.iloc[0])
print('Top genre:', top_genres.index[0], top_genres.iloc[0])
print('Median movie length: %d min' % movies['minutes'].median())
print('Most common rating:', order[0])