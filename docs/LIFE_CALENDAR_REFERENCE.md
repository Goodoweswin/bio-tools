# Life calendar reference

The owner supplied the Gregorian birthday **2000-09-05** in this chat. It is fixed
in `src/js/life-profile.js` so every visitor sees the owner's timeline, independent
of browser storage. No example birthday or editable life-expectancy field remains.

## Statistical scale

- Population: China (`CHN`), male.
- Indicator: life expectancy at birth, male (years), `SP.DYN.LE00.MA.IN`.
- Publisher: World Bank, World Development Indicators; source organizations include
  the UN Population Division / World Population Prospects and national statistics.
- Latest non-null observation verified on 2026-11-02: **2024, 75.249 years**.
- UI value: **75.25 years**. Calculations retain **75.249**.
- API metadata `lastupdated`: `2026-10-08`.
- [Human-readable source](https://data.worldbank.org.cn/indicator/SP.DYN.LE00.MA.IN?locations=CN).
- [Exact observation API](https://api.worldbank.org/v2/country/CHN/indicator/SP.DYN.LE00.MA.IN?format=json&date=2024).
- [Indicator definition](https://api.worldbank.org/v2/indicator/SP.DYN.LE00.MA.IN?format=json).

This is a population period life expectancy at birth, not a prediction for the
owner, the life expectancy of the 2000 birth cohort, or remaining life expectancy
conditional on the owner's current age. The page labels the limitation directly.
The chosen data remain a fixed cited snapshot rather than changing silently with
an external request. Update the value and year together after source verification.

## Date calculation

Start at 2000-09-05 and add 75 whole calendar years. Interpolate the fractional
0.249 year over the actual days between the 75th and 76th anniversaries, rounding
the resulting fraction to the nearest calendar day. This yields a reference end
of 2075-12-05; it is a visualization boundary, not a predicted death date.
Use UTC calendar-day serials to avoid DST errors. Each dot is seven days; the final
dot may be a partial week. The year view still uses the actual 365 or 366 days.
If the owner outlives the reference scale, the interface says time continues.
