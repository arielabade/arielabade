# Ariel Abade

**Growth, data science and machine learning applied to revenue.**

I build the layers between marketing activity and the money it produces: measurement that can be
trusted, analysis that survives being questioned, and models that end in a decision someone can act
on. Around five years across paid media, SaaS growth and analytics, mostly in businesses where the
marketing number and the finance number had to agree.

What I am useful for is the join: connecting campaign behaviour to CAC, LTV, payback and contribution
margin, and then building the thing that computes it rather than stopping at the recommendation.

---

## Featured projects

### [unit-economics-olist](https://github.com/arielabade/unit-economics-olist)
**Business problem** · Which acquisition channels pay for themselves in a marketplace, where the
platform keeps a commission rather than the GMV.
**Key result** · 97.0% of customers buy exactly once, so CAC has to clear on the first order. At a 15%
take rate, contribution margin is R$16.13 per customer — a hard ceiling that paid channels consume
71% of.
**Stack** · DuckDB, SQL, Python, Streamlit.

### [clv-cohort-prediction](https://github.com/arielabade/clv-cohort-prediction)
**Business problem** · Who deserves retention budget, predicted from behaviour before the spend
happens.
**Key result** · BG/NBD + Gamma-Gamma beat LightGBM on every measure (MAE £484 vs £645, Spearman
0.601 vs 0.485) and its decile ranking is monotonic where LightGBM's bottom decile is worth more than
its middle. Top decile captures 51.2% of holdout value.
**Stack** · PyMC-Marketing, LightGBM, pandas.

### [lead-scoring-api](https://github.com/arielabade/lead-scoring-api)
**Business problem** · Which leads a call centre works first, scored before anyone picks up the phone.
**Key result** · The AUC this dataset is usually reported with, 0.954, becomes 0.640 once call
duration and the macroeconomic time proxies are removed. What survives is a 1.54x lift on call
ordering: 30% of capacity reaches 46% of conversions.
**Stack** · LightGBM, FastAPI, Docker, MLflow, scikit-learn.

### [marketing-mix-modeling](https://github.com/arielabade/marketing-mix-modeling)
**Business problem** · How much revenue each channel actually caused, and where the next unit of
budget should go.
**Key result** · Fitted against a simulated process with known parameters, which is the only way to
score an MMM rather than admire it. The model recovers the channels that carry signal and fails
completely on one that does not — and a signal-to-noise diagnostic identifies which is which before
fitting.
**Stack** · PyMC-Marketing, PyMC, pandas.

### [churn-cost-sensitive](https://github.com/arielabade/churn-cost-sensitive)
**Business problem** · Who gets a retention offer, when the offer costs money and only works some of
the time.
**Key result** · The break-even churn probability ranges from 2.7% to 19.6% across customers, so no
global cutoff can express it. Choosing the threshold from retention economics instead of the 0.5
default recovers £10,285 — 21% of achievable value.
**Stack** · LightGBM, scikit-learn, pandas.

### [ab-testing-toolkit](https://github.com/arielabade/ab-testing-toolkit)
**Business problem** · Whether an experiment can answer its question, and what to do with the answer.
**Key result** · Separates "we tested and found nothing" from "we never had the power to find it",
which lead to opposite actions. CUPED with a 0.87-correlated covariate cuts variance 75%, worth 4x the
traffic. The false-positive rate is validated against 2,000 simulated A/A tests.
**Stack** · NumPy, SciPy, statsmodels.

---

## Also here

- [carbon](https://github.com/arielabade/carbon) — exon/intron classification in human DNA with a
  bidirectional LSTM, 99.80% test accuracy against three controlled baselines. Developed for a paper
  accepted at a bioinformatics conference.
- [visppy-cv](https://github.com/arielabade/visppy-cv) — computer vision for physical spaces, selected
  in the Centelha Sergipe III preliminary Phase 2 result.
- [mandacaru](https://github.com/arielabade/mandacaru) — intelligent document processing built in the
  STI/UFS context.
- [echo-womens-health-research-analytics](https://github.com/arielabade/echo-womens-health-research-analytics)
  — survey-based evaluation of a remote women's health training programme.

---

## Stack

**Analytics** · SQL · Python · pandas · DuckDB · dbt
**ML** · scikit-learn · LightGBM · PyMC-Marketing · MLflow
**Engineering** · FastAPI · Docker · GitHub Actions
**Marketing** · GA4 · Meta Ads · Google Ads

---

## How I work

Every project here states what it cannot show. The limitations sections are not boilerplate: they
carry the assumptions that would change the conclusion, the data that is simulated and why, and the
question the analysis was not able to answer. A result without its boundary is not a result.

Where a number is assumed rather than measured, it is named and isolated in one file, so a reviewer
can change it and re-run.

---

- [LinkedIn](https://www.linkedin.com/in/ariel-abade-669869171/)
- [Portfolio](https://arielabade.github.io/abade/)

---

## Em português

Trabalho na junção entre marketing e receita: mensuração confiável, análise que sobrevive a
questionamento, e modelos que terminam numa decisão — CAC, LTV, payback, margem de contribuição,
retenção e incrementalidade.

Cerca de cinco anos entre mídia paga, growth em SaaS e analytics. O diferencial é construir a
ferramenta, não parar no relatório: os projetos acima têm código rodando, testes e documentação de
premissas, não notebooks soltos.

Cada projeto declara o que **não** consegue mostrar. É de propósito: premissa escondida é a forma mais
cara de errar uma decisão de investimento.
