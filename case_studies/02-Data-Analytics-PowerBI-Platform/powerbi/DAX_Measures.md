# Advanced DAX Measures Reference

This document catalogs the custom Data Analysis Expressions (DAX) used in the Power BI dashboard to calculate complex KPIs for customer feedback and sales performance.

## 1. Rolling 3-Month Average Rating
Calculates a smoothing moving average to identify macro trends without getting bogged down by daily volatility.

```dax
Rolling_3M_Avg_Rating = 
CALCULATE(
    AVERAGE(Feedback[Rating]),
    DATESINPERIOD(
        'DateTable'[Date], 
        MAX('DateTable'[Date]), 
        -3, 
        MONTH
    )
)
```

## 2. Dynamic Year-Over-Year (YoY) Sentiment Growth
Measures the percentage increase or decrease in 'Positive' sentiment feedback compared to the exact same period in the previous year.

```dax
YoY_Positive_Sentiment_Growth % = 
VAR CurrentYearPositive = 
    CALCULATE(
        COUNTROWS(Feedback), 
        Feedback[SentimentCategory] = "Positive"
    )
VAR PreviousYearPositive = 
    CALCULATE(
        COUNTROWS(Feedback), 
        Feedback[SentimentCategory] = "Positive", 
        SAMEPERIODLASTYEAR('DateTable'[Date])
    )
RETURN 
    DIVIDE(CurrentYearPositive - PreviousYearPositive, PreviousYearPositive, 0)
```

## 3. Customer Retention / Churn Risk Flag
Flags a customer as "At Risk" if their average feedback score drops below 2.5 in the last 30 days while having previously spent > $1000.

```dax
Churn_Risk_Flag = 
VAR RecentAvgRating = 
    CALCULATE(
        AVERAGE(Feedback[Rating]),
        DATESINPERIOD('DateTable'[Date], MAX('DateTable'[Date]), -30, DAY)
    )
VAR TotalLifetimeSpend = 
    CALCULATE(SUM(Sales[TotalAmount]))
RETURN
    IF(RecentAvgRating < 2.5 && TotalLifetimeSpend > 1000, 1, 0)
```
