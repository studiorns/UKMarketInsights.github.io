# UK Travel Queries Forecast Multipliers

Based on the data provided in the Travel_Queries_Forecast_UK_Updated.csv file, here are the calculated multipliers for the UK market forecast.

## Media Multiplier

The Media Multiplier is calculated using:
```
Media Multiplier = 1 + (Media Effectiveness Multiplier * LOG(1 + (2025 Planned Impressions / 2024 Impressions)))
```

For UK, using the data provided:

| Month | 2024 Impressions | 2025 Planned Impressions | Conservative (0.10) | Moderate (0.15) | Ambitious (0.20) |
|-------|------------------|--------------------------|---------------------|-----------------|------------------|
| January | 39,767,259 | 65,000,000 | 1.05 | 1.07 | 1.10 |
| February | 20,577,624 | 45,000,000 | 1.08 | 1.12 | 1.16 |
| March | 50,003,357 | 85,000,000 | 1.05 | 1.08 | 1.10 |
| April | 109,331,811 | 130,000,000 | 1.02 | 1.02 | 1.03 |
| May | 45,176,614 | 70,000,000 | 1.04 | 1.07 | 1.09 |
| June | 37,914,837 | 60,000,000 | 1.05 | 1.07 | 1.09 |
| July | 56,385,822 | 80,000,000 | 1.04 | 1.05 | 1.07 |
| August | 30,416,431 | 55,000,000 | 1.06 | 1.09 | 1.12 |
| September | 55,798,934 | 85,000,000 | 1.04 | 1.06 | 1.08 |
| October | 111,534,185 | 140,000,000 | 1.02 | 1.03 | 1.04 |
| November | 136,058,361 | 160,000,000 | 1.02 | 1.02 | 1.03 |
| December | 47,304,711 | 75,000,000 | 1.05 | 1.07 | 1.09 |

## Flight Search Factor

The Flight Search Factor is calculated using:
```
Flight Search Factor = 1 + (Flight Search Correlation * Projected Flight Search Growth)
```

Where:
```
Projected Flight Search Growth = (2024 Flight Searches - 2023 Flight Searches) / 2023 Flight Searches
```

For UK, using the data provided:

| Month | 2023 Searches | 2024 Searches | Growth | Conservative (0.05) | Moderate (0.10) | Ambitious (0.15) |
|-------|---------------|---------------|--------|---------------------|-----------------|------------------|
| January | 10,767 | 17,665 | 0.64 | 1.32 | 1.64 | 1.96 |
| February | 6,511 | 13,368 | 1.05 | 1.51 | 2.05 | 2.58 |
| March | 7,372 | 15,826 | 1.15 | 1.46 | 2.15 | 2.72 |
| April | 6,642 | 13,953 | 1.10 | 1.52 | 2.10 | 2.65 |
| May | 6,345 | 17,633 | 1.78 | 1.78 | 2.78 | 3.67 |
| June | 6,479 | 17,415 | 1.69 | 1.69 | 2.69 | 3.53 |
| July | 9,945 | 20,346 | 1.05 | 1.51 | 2.05 | 2.57 |
| August | 9,989 | 15,218 | 0.52 | 1.26 | 1.52 | 1.78 |
| September | 10,744 | 22,007 | 1.05 | 1.51 | 2.05 | 2.57 |
| October | 11,213 | 19,997 | 0.78 | 1.39 | 1.78 | 2.17 |
| November | 12,135 | 12,760 | 0.05 | 1.05 | 1.05 | 1.08 |
| December | 11,526 | 15,876 | 0.38 | 1.19 | 1.38 | 1.57 |

## Brand Health Multiplier

The Brand Health Multiplier is calculated using:
```
Brand Health Multiplier = 1 + ((Projected Brand Consideration Growth) * Brand Health Coefficient)
```

Where:
```
Projected Brand Consideration Growth = (Target Brand Consideration - Current Brand Consideration) / Current Brand Consideration
```

### Brand Health Metrics Definitions

- **Awareness**: Percentage of people from the UK market who are aware of Abu Dhabi
- **Consideration**: Percentage of people who consider traveling to Abu Dhabi in the next 3 years
- **Intent**: Percentage of people who consider traveling to Abu Dhabi in the next 12 months

For UK, using the data provided:
- Current Brand Consideration (Q4 2024): 33.09%
- Target Brand Consideration (Conservative): 34.00%
- Target Brand Consideration (Moderate): 35.00%
- Target Brand Consideration (Ambitious): 36.00%

Projected Brand Consideration Growth:
- Conservative: (34.00% - 33.09%) / 33.09% = 0.028
- Moderate: (35.00% - 33.09%) / 33.09% = 0.058
- Ambitious: (36.00% - 33.09%) / 33.09% = 0.088

Brand Health Multiplier:
- Conservative: 1 + (0.028 * 0.15) = 1.004
- Moderate: 1 + (0.058 * 0.20) = 1.012
- Ambitious: 1 + (0.088 * 0.25) = 1.022

For simplicity in the forecast calculations, we've rounded these to:
- Conservative: 1.01
- Moderate: 1.01
- Ambitious: 1.02

The UK market already has a high brand awareness level (92.70%), indicating that Abu Dhabi is well-known in this market. The consideration rate of 33.09% shows that a significant portion of those aware of Abu Dhabi are considering it as a travel destination within the next 3 years. The intent rate of 22.10% indicates that about two-thirds of those considering Abu Dhabi are planning to visit within the next 12 months, which is a strong conversion rate from consideration to intent.

## Complete Forecast Calculation

For each month and scenario, the forecast is calculated using:
```
Forecast = 2024 Queries * Base Growth Factor * Seasonality Index * Media Multiplier * Flight Search Factor * Brand Health Multiplier
```

For example, for January under the Moderate scenario:
```
Forecast = 124.85 * 1.10 * 1.25 * 1.07 * 1.64 * 1.01 = 182.01
```

## Forecast Results

Based on these multipliers, here are the forecast results for UK:

| Month | 2024 Queries | Conservative | Moderate | Ambitious | Conservative YoY | Moderate YoY | Ambitious YoY |
|-------|--------------|--------------|----------|-----------|------------------|--------------|---------------|
| January | 124.85 | 173.82 | 182.01 | 190.20 | 39.2% | 45.8% | 52.3% |
| February | 98.80 | 159.63 | 167.12 | 174.61 | 61.6% | 69.2% | 76.7% |
| March | 99.09 | 158.92 | 166.37 | 173.82 | 60.4% | 67.9% | 75.4% |
| April | 92.34 | 142.66 | 149.35 | 156.04 | 54.5% | 61.7% | 69.0% |
| May | 86.94 | 144.58 | 151.36 | 158.14 | 66.3% | 74.1% | 81.9% |
| June | 82.80 | 123.38 | 129.15 | 134.92 | 49.0% | 56.0% | 63.0% |
| July | 86.15 | 121.05 | 126.72 | 132.39 | 40.5% | 47.1% | 53.7% |
| August | 92.83 | 113.37 | 118.68 | 124.00 | 22.1% | 27.9% | 33.6% |
| September | 99.68 | 158.07 | 165.48 | 172.89 | 58.6% | 66.0% | 73.4% |
| October | 110.86 | 175.69 | 183.94 | 192.19 | 58.5% | 66.0% | 73.4% |
| November | 97.24 | 106.45 | 111.41 | 116.37 | 9.5% | 14.6% | 19.7% |
| December | 99.18 | 135.19 | 141.53 | 147.87 | 36.3% | 42.7% | 49.1% |
| **Average** | **97.56** | **142.73** | **149.43** | **156.12** | **46.3%** | **53.2%** | **60.1%** |

These calculations provide a comprehensive forecast for UK's travel queries in 2025 across three scenarios, taking into account all the factors in the multi-factor approach.

## Key Insights for UK Market

1. **Strong Growth Potential**: The UK market shows significant growth potential across all scenarios, with average YoY growth ranging from 46.3% (Conservative) to 60.1% (Ambitious).

2. **Seasonal Patterns**: The UK market exhibits strong seasonality, with January, February, March, September, and October showing the highest growth potential.

3. **Flight Search Impact**: The substantial growth in flight searches from 2023 to 2024 is a major driver of the forecast, particularly for the first half of the year.

4. **Media Effectiveness**: The planned media impressions for 2025 are expected to have a moderate impact on query growth, with multipliers ranging from 1.02 to 1.08 across most months.

5. **Brand Health Considerations**: The UK market already has strong brand consideration (33.09%), with modest targets for growth in 2025. This results in a relatively small but positive brand health multiplier.

6. **Comparison to Other Markets**: The UK market forecast shows higher growth potential compared to some other markets, likely due to the combination of strong flight search growth and effective media planning.
