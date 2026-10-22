# Autocall Payoff & Term-Sheet Comparator

This is a Python tool to compare autocall structures on the same market paths, with a breakdown of redemption amounts, investment durations and returns.

The project combines deterministic scenarios with 165 historical EURO STOXX 50 starting dates. It examines how coupon rates and protection barriers affect investor outcomes.

The structures are hypothetical. The tool calculates contractual payoffs; it does not produce market prices or bank quotes.

## What the comparison shows

Three structures are evaluated with the same observation schedule and autocall barrier:

| Offer | Annual conditional rate | Autocall barrier | Protection barrier |
|---|---:|---:|---:|
| A | 8.2% | 100% | 60% |
| B | 8.8% | 100% | 65% |
| C | 7.6% | 100% | 55% |

Across the historical sample:

| Offer | Capital-loss frequency | Median annualized return | Worst total return |
|---|---:|---:|---:|
| A | 5.5% | 8.2% | −54.6% |
| B | 6.1% | 8.8% | −54.6% |
| C | 2.4% | 7.6% | −54.6% |

C's lower protection barrier reduced the number of loss-making cases, but did not reduce the worst loss observed. B delivered the highest median annualized return.

For six starting dates, C repaid the full principal while B incurred a capital loss. These cases illustrate the difference between receiving a higher conditional coupon and retaining protection through a larger decline.

All three offers had the same autocall frequency, approximately 85.5%, because their recall conditions were identical. The engine also supports different autocall barriers.

These figures describe the sample studied. They are not forecasts or estimates of future probabilities.

## Run the analysis

Clone or download the repository, then open a terminal in its directory.

Create and activate a virtual environment on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Open `analysis.ipynb` in VS Code with the Jupyter extension installed. Select the `.venv` Python environment as the notebook kernel, then run all cells from top to bottom.

An internet connection is required to retrieve the historical data.

To run the engine tests:

```bash
python -m unittest test_autocall -v
```

## Product mechanics

The model uses a single underlying, normalized to 100 at inception, with an investment at par and a maximum maturity of five years.

**Early redemption**

The underlying is observed annually in years 1–4. If it is at or above the autocall barrier, the product ends and pays:

```text
nominal × (1 + annual conditional rate × elapsed years)
```

There are no intermediate payments. Conditional gains accumulate without compounding.

**At maturity**

If no early redemption occurred:

| Final underlying level | Payment |
|---|---|
| At or above 100 | Nominal plus five years of conditional gains |
| Below 100, but at or above the protection barrier | Nominal only |
| Below the protection barrier | Nominal × final normalized level / 100 |

Protection is assessed only at maturity. A fall below the barrier during the product's life does not, by itself, determine the final payment.

The maturity gain threshold remains fixed at 100, independently of the early autocall barrier.

**Outcome labels**

- `autocall`: early redemption.
- `protected`: full principal repaid at maturity, with or without gain.
- `capital_loss`: less than the principal repaid at maturity.

Annualized returns are calculated from the initial investment and the single redemption payment.

## Data and historical replay

Daily EURO STOXX 50 closing levels are retrieved from Yahoo Finance through `yfinance`, using ticker `^STOXX50E` with automatic adjustment disabled.

The retrieved dataset runs from March 2007 to December 2025. Monthly starting dates from April 2007 to December 2020 produce 165 paths and 495 structure-level results.

For each path:

1. Inception is the first available observation on or after the requested start.
2. The inception level is normalized to 100.
3. Annual observations use the first available close on or after each anniversary of actual inception.
4. All five annual observations must be available.
5. An annual observation more than seven calendar days after its target date raises an error.

The notebook includes deterministic scenarios, selected historical examples, monthly comparisons and outcome charts.

## Scope and limitations

- Historical windows overlap; observations are not independent.
- The same hypothetical terms are applied at every start date. Their availability or economic feasibility at those dates is not established.
- Fees, taxes, issuer default and secondary-market sales are excluded.
- No reinvestment is assumed after redemption.
- Annualization uses whole-year durations, ignoring settlement lags and small observation-date shifts.
- The worst historical loss is not the maximum possible loss.
- Data has not been independently reconciled with an official feed. Provider revisions may change reproduced results.

The engine does not model volatility, discounting, funding or hedging costs for valuation purposes.

## Project files

| File | Purpose |
|---|---|
| `autocall.py` | Payoff engine and return calculations |
| `analysis.ipynb` | Scenarios, historical data, comparisons and charts |
| `test_autocall.py` | Unit tests for the payoff engine |
| `requirements.txt` | Python dependencies required to run the project |

Tests cover changes in the autocall barrier, the capital-protection boundary and the maturity-gain boundary.