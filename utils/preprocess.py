import pandas as pd


def clean_duration_and_rating(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and extracts numeric duration, handles cases where duration is in the rating, and categorizes duration.
    Args:
        df (pd.DataFrame): Input DataFrame.
    Returns:
        pd.DataFrame: DataFrame with cleaned duration and rating columns, and duration label.
    """
    df['duration_cleaned'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['duration_like_rating'] = df['rating'].str.contains(r'(min|Season)', na=False)
    df.loc[df['duration_like_rating'], 'duration_cleaned'] = (
    df.loc[df['duration_like_rating'], 'rating']
        .str.extract(r'(\d+)')
        .squeeze()
        .astype(float)
    )
    df.loc[df['rating'].str.contains(r'(min|Season)', na=False), 'rating'] = "Unrated"
    
    df.drop(columns=['duration_like_rating'], inplace=True)
    df.drop(columns=['duration'], inplace=True)


    return df

def impute_missing_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputes missing values in 'duration_cleaned' using mean for movies and median for TV shows.
    Args:
        df (pd.DataFrame): Input DataFrame.
    Returns:
        pd.DataFrame: DataFrame with imputed 'duration_cleaned'.
    """
    movies = df[df['type'] == 'Movie']
    movie_mean = round(movies['duration_cleaned'].mean(), 2)
    df.loc[
        (df['type'] == 'Movie') & (df['duration_cleaned'].isna()),
        'duration_cleaned'
    ] = movie_mean

    tv_shows = df[df['type'] == 'TV Show']
    tv_median = round(tv_shows['duration_cleaned'].median(), 2)
    df.loc[
        (df['type'] == 'TV Show') & (df['duration_cleaned'].isna()),
        'duration_cleaned'
    ] = tv_median

    return df

def categorize_duration(row):
    """
    Categorizes the duration of a row based on its type and cleaned duration.
    Args:
        row (pd.Series): A row from the DataFrame.
    Returns:
        str: Duration category label.
    """
    if row['type'] == 'Movie':
        if row['duration_cleaned'] < 60:
            return "very short movie"
        elif row['duration_cleaned'] < 120:
            return "short movie"
        else:
            return "long movie"
    elif row['type'] == 'TV Show':
        if row['duration_cleaned'] == 1:
          return "one season show"
        elif row['duration_cleaned'] > 1:
          return "multi-season show"
    return "unknown"


def create_embedding_input(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a single text column 'embedding_input' by concatenating relevant fields for embedding generation.
    Args:
        df (pd.DataFrame): Input DataFrame.
    Returns:
        pd.DataFrame: DataFrame with new 'embedding_input' column.
    """
    df['embedding_input'] = (
        df['title'] + '. ' +
        df['description'] + '. ' +
        df['listed_in'] + '. ' +
        df['cast'] + '. ' +
        df['director'] + '. ' +
        df['country'] + '. ' +
        df['type'] + '. ' +
        df['release_year'].astype(str) + '. ' +
        df['rating'] + '. ' +
        df['duration_cleaned'].astype(str) + '. ' +
        df['duration_label']
    )
    return df

def preprocess_netflix_data(file_path: str) -> pd.DataFrame:
    """
    Runs the full preprocessing pipeline on the Netflix data CSV file.
    Args:
        file_path (str): Path to the CSV file.
    Returns:
        pd.DataFrame: Fully preprocessed DataFrame ready for downstream tasks.
    """
    df = pd.read_csv(file_path)
    df.set_index('show_id', inplace=True)

    # Fill missing text fields
    for col in ["director", "cast", "country"]:
        df[col] = df[col].fillna("Unknown").astype(str)

    # Parse and extract date info
    df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
    df['year_added'] = df['date_added'].dt.year.fillna(0).astype(int)
    df['month_added'] = df['date_added'].dt.month.fillna(0).astype(int)

    # Clean and encode duration and rating
    df = clean_duration_and_rating(df)
    df = impute_missing_duration(df)
    
    df['duration_label'] = df.apply(categorize_duration, axis=1)
    
    df['rating'] = df['rating'].fillna('Unrated')
    df['rating'] = df['rating'].str.strip().str.upper()

    df = create_embedding_input(df)

    return df