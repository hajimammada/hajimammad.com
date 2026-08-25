import pytest
import pandas as pd
import numpy as np
from src.python_etl.transform import DataTransformer

@pytest.fixture
def sample_data(tmp_path):
    """Creates a temporary CSV file with sample data for testing."""
    df = pd.DataFrame({
        'customer_id': [1, 2, 3, 4],
        'product_id': ['P1', 'P2', None, 'P1'],
        'rating': [5.0, -1.0, 4.0, 3.0], # Includes an out-of-bounds rating
        'feedback_text': ["Great!", None, "Good", "Okay"],
        'timestamp': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04'])
    })
    file_path = tmp_path / "test_data.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)

def test_data_cleaning(sample_data):
    transformer = DataTransformer(sample_data)
    transformer.load_data()
    transformer.clean_data()
    
    # Assert missing product_id row was dropped
    assert len(transformer.df) == 3
    
    # Assert out-of-bounds rating (-1.0) was clipped to 0
    assert transformer.df.loc[transformer.df['customer_id'] == 2, 'rating'].values[0] == 0.0
    
    # Assert missing feedback was imputed
    assert transformer.df.loc[transformer.df['customer_id'] == 2, 'feedback_text'].values[0] == "NO_COMMENT"

def test_feature_engineering(sample_data):
    transformer = DataTransformer(sample_data)
    transformer.load_data()
    transformer.clean_data()
    transformer.engineer_features()
    
    # Check if sentiment categories are correctly assigned
    sentiments = transformer.df['sentiment_category'].tolist()
    assert sentiments == ['Positive', 'Negative', 'Neutral'] # Ratings 5.0, 0.0 (clipped), 3.0
    
    # Check if date components were extracted
    assert 'year_month' in transformer.df.columns
    assert 'day_of_week' in transformer.df.columns
