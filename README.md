# Understanding and Predicting Delays at Virginia Airports

This repository is the reproducible data package for Dan DiCrisis's DASC 605 Bring Your Own Data (BYOD) presentation. It uses the U.S. Department of Transportation, Bureau of Transportation Statistics (BTS), Reporting Carrier On-Time Performance data for calendar year 2025.

## Research focus

Which operational factors are associated with arrival delays, and when do flights departing Virginia airports recover time after a delayed departure?

## Public source

- Database description: https://transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFD
- Field selection/download: https://www.transtats.bts.gov/DL_SelectFields.aspx?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ
- Data.gov catalog record: https://catalog.data.gov/dataset/u-s-marketing-air-carriers-on-time-performance

BTS collects individual-flight operational reports monthly from reporting U.S. air carriers. The source includes scheduled and actual times, carriers and airports, cancellations and diversions, taxi and airborne time, distance, and delay causes.

## Study population

- **Unit of observation:** one reported domestic flight.
- **Population represented:** reported domestic flights that originated at a Virginia airport from January through December 2025.
- **Target population:** comparable scheduled domestic passenger flights originating at Virginia airports.
- **Scope filter:** `OriginState == "VA"` and `Year == 2025`.

The completed file contains **241,078 flights and 35 variables**, covering CHO, DCA, IAD, ORF, PHF, RIC, and ROA. The compressed CSV is approximately 7.3 MB, small enough for a normal GitHub repository.

Because the data are carrier reports rather than a random sample, conclusions should be limited to the defined operational population. Association does not establish causation.

## Included files

- `data/va_flights_2025.csv.gz` — complete filtered analytic dataset.
- `data/va_flights_2025_sample.csv` — first 1,000 rows for quick review.
- `data/data_dictionary.csv` — selected and derived variable definitions.
- `scripts/build_dataset.py` — rebuilds the data from the 12 official monthly ZIP files.
- `presentation/DASC605_BYOD_Virginia_Airline_Delays.pptx` — two-slide presentation.
- `presentation/BYOD_Presentation_Script.docx` — timed five-minute narration.

## Reproduce the dataset

1. Install Python 3.10 or later.
2. Run `python -m pip install -r requirements.txt`.
3. Run `python scripts/build_dataset.py`.
4. The script downloads the 12 official 2025 monthly ZIP files, selects the documented fields, filters Virginia origins, derives `MinutesRecovered` and `Delayed15`, and writes the two data files.

Cancelled or diverted flights remain in the dataset, but the script never replaces their missing arrival delay with zero. Exclude them when modeling arrival-delay minutes; retain them for cancellation or diversion analyses.

## Candidate course analyses

- Correlation: departure delay with arrival delay; distance with air time.
- Estimation: confidence intervals for mean or median arrival delay.
- Hypothesis testing: compare airlines, airports, weekdays, and weekends.
- PCA: summarize correlated operational time measures.
- Regression: predict arrival-delay minutes.
- Classification: predict whether arrival delay is at least 15 minutes.

## Citation

U.S. Department of Transportation, Bureau of Transportation Statistics. *Reporting Carrier On-Time Performance (1987–present)*, calendar year 2025. Accessed September 4, 2026.
