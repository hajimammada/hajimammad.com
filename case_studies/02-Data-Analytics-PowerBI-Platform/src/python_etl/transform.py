import pandas as pd
import numpy as np
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Transforms raw customer feedback data into a structured format 
    suitable for Power BI and statistical modeling in R.
    """
    
    def __init__(self, raw_data_path: str):
        self.raw_data_path = raw_data_path
        self.df = None

    def load_data(self) -> None:
        """Loads data with memory optimization."""
        dtypes = {
            'customer_id': 'int32',
            'product_id': 'category',
            'rating': 'float32',
            'feedback_text': 'string'
        }
        try:
            self.df = pd.read_csv(self.raw_data_path, dtype=dtypes, parse_dates=['timestamp'])
            logger.info(f"Loaded {len(self.df)} records.")
        except FileNotFoundError:
            logger.error(f"Data file not found at {self.raw_data_path}")
            raise

    def clean_data(self) -> None:
        """Handles missing values and outliers."""
        initial_len = len(self.df)
        
        # Drop rows missing critical analytical fields
        self.df.dropna(subset=['product_id', 'rating'], inplace=True)
        
        # Impute missing feedback text with a placeholder
        self.df['feedback_text'] = self.df['feedback_text'].fillna("NO_COMMENT")
        
        # Cap ratings to logical boundaries (0 to 5)
        self.df['rating'] = np.clip(self.df['rating'], 0, 5)
        
        logger.info(f"Data cleaning dropped {initial_len - len(self.df)} invalid records.")

    def engineer_features(self) -> None:
        """Derives new features for trend analysis."""
        # Extract time-series components
        self.df['year_month'] = self.df['timestamp'].dt.to_period('M')
        self.df['day_of_week'] = self.df['timestamp'].dt.day_name()
        
        # Basic text length feature (proxy for feedback detail)
        self.df['feedback_length'] = self.df['feedback_text'].str.len()
        
        # Simulate a basic sentiment score based on rating (in production, this would call an NLP model)
        conditions = [
            (self.df['rating'] >= 4),
            (self.df['rating'] == 3),
            (self.df['rating'] <= 2)
        ]
        choices = ['Positive', 'Neutral', 'Negative']
        self.df['sentiment_category'] = np.select(conditions, choices, default='Unknown')

    def export_processed_data(self, output_path: str) -> None:
        """Exports the cleaned dataset to a Parquet file for high-performance reading."""
        self.df.to_parquet(output_path, engine='pyarrow', index=False)
        logger.info(f"Exported processed data to {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Orchestration logic
    # transformer = DataTransformer('../data/raw/customer_feedback.csv')
    # transformer.load_data()
    # transformer.clean_data()
    # transformer.engineer_features()
    # transformer.export_processed_data('../data/processed/feedback_cleaned.parquet')
