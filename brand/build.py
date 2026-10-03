"""Generate the ABADE README assets for every public repository.

Usage: python build.py <folder containing the cloned repositories>
Needs fontTools and the Lato TTFs in ~/.local/share/fonts.
"""
import sys
from pathlib import Path

from brandkit import COBALT, RISK, arc, bars, emit, header, kpis, portfolio_map, symbol, track, svg, IVORY, CARBON

REPOS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]

SPEC = {
    "unit-economics-olist": dict(
        stage="Scale",
        head=("Scale · Unit economics · DuckDB SQL", "Unit Economics by Channel",
              "CAC, LTV, payback and contribution margin by acquisition channel, on real marketplace data."),
        kpis=[("Buy exactly once", "97.0%", "of 93,358 customers: CAC must clear on the first order"),
              ("Margin ceiling", "R$16.13", "first-order contribution per customer at a 15% take rate"),
              ("Paid search CAC", "71%", "of a customer's entire first-order margin")],
        arc=["A marketplace keeps a commission, not the GMV, and spends on paid acquisition.",
             "Which channels bring customers worth more than they cost?",
             "Margin on commission in DuckDB SQL, assumptions isolated, spend lagged to avoid circular CAC.",
             "Only email/CRM clears 3x LTV/CAC. Raise margin per order before raising paid budget."],
        chart=dict(title="Only email/CRM clears the 3x planning target",
                   subtitle="LTV/CAC by paid channel · first-order contribution margin over CAC",
                   rows=[("email_crm", 4.28), ("paid_social", 1.43), ("paid_search", 1.40)], fmt="{:.2f}x",
                   highlight={"email_crm": COBALT}, refs=[(1.0, "break-even"), (3.0, "3x target")],
                   source="Retention and margin: real Olist data · channel and spend: SIMULATED (see Data)")),
    "clv-cohort-prediction": dict(
        stage="Retain",
        head=("Retain · CLV · Probabilistic models", "CLV Cohort Prediction",
              "BG/NBD + Gamma-Gamma against LightGBM, scored on a six-month holdout of real transactions."),
        kpis=[("Top-decile capture", "51.2%", "of holdout value by contacting 10% of customers"),
              ("MAE", "£484", "vs £645 for LightGBM on unseen customers"),
              ("Spearman", "0.601", "rank correlation vs 0.485 for LightGBM")],
        arc=["A UK retailer with a finite retention budget and 5,878 customers.",
             "Rank customers by future value before the spend happens.",
             "Temporal and by-customer splits; BG/NBD + Gamma-Gamma vs LightGBM on identical customers.",
             "The probabilistic model wins on every metric and its ranking never inverts."],
        chart=dict(title="Only the probabilistic model's ranking degrades cleanly",
                   subtitle="Holdout value per decile relative to the average customer (lift). LightGBM's bottom decile is worth more than deciles 5–9.",
                   rows=[(f"Decile {i + 1}", [a, b]) for i, (a, b) in enumerate(zip(
                       [5.09, 1.67, 0.92, 0.65, 0.45, 0.40, 0.30, 0.20, 0.16, 0.12],
                       [4.26, 1.76, 1.02, 0.75, 0.43, 0.44, 0.36, 0.22, 0.10, 0.64]))],
                   series=[("BG/NBD + Gamma-Gamma", COBALT), ("LightGBM", "muted")], fmt="{:.2f}x",
                   refs=[(1.0, "average")], source="Source: Online Retail II (UCI) · holdout 2011-06-10 to 2011-12-09")),
    "lead-scoring-api": dict(
        stage="Scale",
        head=("Scale · Lead scoring · FastAPI + Docker", "Lead Scoring API",
              "A deployable lead-scoring service, and an honest account of what the model is worth."),
        kpis=[("Call-order lift", "1.54x", "30% of capacity reaches 46% of conversions"),
              ("Honest AUC", "0.640", "after removing two leaks; the usual 0.954 is not deployable"),
              ("Brier", "0.237", "calibrated; beats logistic regression's 0.264")],
        arc=["A bank's outbound team has more leads than it can call.",
             "Who should be called first, using only what is known at dialling time?",
             "Chronological split, leakage rules in code, isotonic calibration, served over FastAPI in Docker.",
             "A 1.54x lift on call ordering, worth £167,752 at 30% capacity."],
        chart=dict(title="Two leaks inflate AUC from 0.640 to 0.954",
                   subtitle="Test AUC by evaluation setup · the call duration and macro time proxies are not available before dialling",
                   rows=[("Random split + duration + macro", 0.954), ("Random split + macro", 0.811),
                         ("Random split", 0.778), ("Time split + duration + macro", 0.728),
                         ("Time split + macro", 0.597), ("Time split · deployable", 0.640)],
                   fmt="{:.3f}", highlight={"Time split · deployable": COBALT}, refs=[(0.5, "random")], xmax=1.05,
                   source="Source: Bank Marketing (UCI), 41,188 contacts, May 2008 – Nov 2010")),
    "marketing-mix-modeling": dict(
        stage="Validate",
        head=("Validate · MMM · Bayesian", "Marketing Mix Modeling",
              "A Bayesian MMM with adstock and saturation, scored against a known data-generating process."),
        kpis=[("Rank correlation", "1.000", "true vs estimated ROI on every channel that carries signal"),
              ("Affiliate ROI error", "+636%", "the one channel with no measurable signal"),
              ("Signal-to-noise", "0.04", "affiliate, flagged before fitting")],
        arc=["A business spends across TV, search, social and affiliate.",
             "Incremental contribution is never observed, so an MMM can be inspected but not scored.",
             "Fit against a simulation with known parameters; compute signal-to-noise before fitting.",
             "Perfect ranking where signal exists. Pin unmeasurable channels instead of optimising them."],
        chart=dict(title="Affiliate carries no measurable signal, and causes the ranking failure",
                   subtitle="Signal-to-noise per channel: sd(weekly contribution) / sd(revenue noise), computed before fitting",
                   rows=[("tv", 0.88), ("search", 0.45), ("social", 0.30), ("affiliate", 0.04)], fmt="{:.2f}",
                   highlight={"affiliate": RISK}, refs=[(0.1, "min. measurable")],
                   source="SIMULATED data with known parameters · 104 weeks · src/mmm/config.py")),
    "ab-testing-toolkit": dict(
        stage="Validate",
        head=("Validate · Experimentation · Frequentist + Bayesian", "A/B Testing Toolkit",
              "Design an experiment, read it honestly, and decide: ship, hold, inconclusive or stop."),
        kpis=[("CUPED variance cut", "75.3%", "worth 4.05x the traffic with a 0.87-correlated covariate"),
              ("Sample needed", "122,124", "users per variant for a 5% lift at a 5% baseline"),
              ("A/A calibration", "2,000", "simulated tests confirm the 5% false-positive rate")],
        arc=["Teams run tests and report p-values as if they were decisions.",
             "Underpowered tests read as 'no effect'; real but small effects get shipped.",
             "Power before launch, CUPED, Bayesian expected loss, and a minimum worthwhile lift.",
             "Three verdicts that separate 'no effect' from 'never had the power to tell'."],
        chart=dict(title="A one-week test cannot detect the lift the team cares about",
                   subtitle="Smallest detectable relative lift by users per variant · 5% baseline, alpha 0.05, power 0.80",
                   rows=[("5,000", 25.9), ("20,000", 12.6), ("100,000", 5.5), ("122,124", 5.0)], fmt="{:.1f}%",
                   highlight={"122,124": COBALT}, refs=[(5.0, "target lift")],
                   source="Computed by src/abtest/design.py · validated against 2,000 simulated A/A tests")),
    "churn-cost-sensitive": dict(
        stage="Retain",
        head=("Retain · Churn · Decision economics", "Cost-Sensitive Churn",
              "A churn model is not the deliverable. The decision rule is."),
        kpis=[("Value recovered", "£10,285", "vs the 0.5 default: 21% of achievable value"),
              ("Break-even range", "2.7–19.6%", "churn probability, 10th to 90th percentile"),
              ("Model", "AUC 0.848", "isotonic-calibrated, Brier 0.142")],
        arc=["A telecom with a finite retention budget and a churn model.",
             "An offer costs money and works only sometimes: who should get it?",
             "Calibrate, then contact only where expected value is positive, per customer.",
             "£48,621 net value; the 0.5 default leaves £10,285 behind."],
        chart=dict(title="The 0.5 default leaves £10,285 on the table",
                   subtitle="Net campaign value by decision rule · same model, same 1,761 test customers",
                   rows=[("Per-customer expected value", 48621), ("Best-F1 threshold (0.18)", 48237),
                         ("Default threshold (0.5)", 38336), ("Contact everyone", 36950)], fmt="£{:,.0f}",
                   highlight={"Per-customer expected value": COBALT},
                   source="Source: IBM Telco Customer Churn · economics declared in src/churn/config.py")),
    "growth-analytics-warehouse": dict(
        stage="Scale",
        head=("Scale · Analytics engineering · Synthetic data", "Growth Analytics Warehouse",
              "Generator, tested pipeline, DuckDB snowflake warehouse, SQL catalog, analysis and a Dash app."),
        kpis=[("Blended LTV/CAC", "2.35x", "payback 7.5 months; only the US clears 3x"),
              ("Usage concentration", "29.8%", "of active users produce 80% of volume"),
              ("Upgrade model lift", "6.8x", "top decile, PR-AUC 0.105 vs 0.006 base rate")],
        arc=["A freemium B2B SaaS buys paid media in 8 countries with very different economics.",
             "Where does paid media pay back, and who upgrades next? And can the data be trusted?",
             "Seeded generator → tested pipeline → snowflake warehouse → SQL catalog → model → app.",
             "Only the US clears 3x LTV/CAC; 68 data-quality checks guard every number."],
        chart=dict(title="Cheap signups are not cheap customers: only the US clears 3x",
                   subtitle="LTV/CAC by country · paid CAC on mature 90-day cohorts · SYNTHETIC company",
                   rows=[("US", 5.28), ("ES", 2.60), ("DE", 2.10), ("MX", 1.66), ("BR", 1.30), ("CO", 0.92),
                         ("PE", 0.62), ("AR", 0.34)], fmt="{:.2f}x", highlight={"US": COBALT, "AR": RISK},
                   refs=[(1.0, "break-even"), (3.0, "3x target")],
                   source="SYNTHETIC data from a seeded simulator · docs/RESULTS.md")),
    "tracking-attribution-lab": dict(
        stage="Validate",
        head=("Validate · Measurement · SQL + docs", "Tracking & Attribution Lab",
              "Measurement quality is the first budget decision. Bad events make better bidding buy the wrong outcome faster."),
        kpis=[("Event states", "5", "observed → sent → received → attributed → reported"),
              ("SQL quality checks", "3", "missing UTMs, duplicate conversions, source consistency"),
              ("Client data", "0", "generic schema; adapt names to your warehouse")],
        arc=["Every CPA and ROAS downstream inherits the quality of the event layer.",
             "Disputed numbers live between what happened and what the dashboard reports.",
             "Name the five event states, govern UTMs, and catch loss with SQL before reporting.",
             "A number can be defended, because the stage where it breaks is named."],
        chart=None),
    "paid-media-budget-optimizer": dict(
        stage="Scale",
        head=("Scale · Paid media · Rule-based allocation", "Paid Media Budget Optimizer",
              "From campaign metrics to a budget split that survives being questioned."),
        kpis=[("Signals", "5", "efficiency, cost, volume, stability, scale capacity"),
              ("Efficiency weight", "35%", "ROAS capped so one outlier cannot dominate"),
              ("Decision rule", "Headroom", "a high score earns budget, headroom earns growth")],
        arc=["A fixed budget spread across campaigns with different returns and headroom.",
             "Decide where each marginal unit goes, and say why in one sentence per campaign.",
             "Transparent weighted score, proportional allocation, a separate prioritise/observe/reduce rule.",
             "The top scorer is not prioritised: brand search has no headroom left to buy."],
        chart=dict(title="Efficiency ranks campaigns; it does not decide alone",
                   subtitle="Weight of each signal in the campaign score",
                   rows=[("Efficiency (ROAS)", 35), ("Cost (CPA)", 25), ("Volume", 20), ("Stability", 10),
                         ("Scale capacity", 10)], fmt="{:.0f}%", highlight={"Efficiency (ROAS)": COBALT}, xmax=40,
                   source="src/paid_media_budget_optimizer/optimizer.py · SYNTHETIC sample campaigns")),
    "marketing-analytics-portfolio": dict(
        stage="Scale",
        head=("Scale · Marketing analytics · KPI layer", "Marketing Analytics Portfolio",
              "A campaign report is not a decision. This layer turns campaign behaviour into a next action."),
        kpis=[("Questions per case", "3", "what changed, what matters, what follows"),
              ("Core KPIs", "CPA · ROAS · CVR", "one definition each, shared by every case"),
              ("Silent zeros", "0", "a missing metric returns None, never 0.0")],
        arc=["Campaign and funnel data reach the team as reports, not decisions.",
             "Movement is not meaning: what changed, what matters, and what to do?",
             "One KPI layer with guarded definitions, and one case format that ends in a limitation.",
             "Findings stay auditable, and every case ends in a named next action."],
        chart=None),
    "carbon": dict(
        stage="Build",
        head=("Build · Bioinformatics · Deep learning", "Carbon",
              "Exon and intron classification in human DNA with a bidirectional LSTM. Paper accepted at an international conference."),
        kpis=[("Test accuracy", "99.80%", "Bi-LSTM on held-out sequences"),
              ("Specificity", "1.000", "where Simple RNN collapses to 0.338"),
              ("Sequences", "9,971", "8 human genes from Ensembl")],
        arc=["Gene-structure analysis needs coding and non-coding regions told apart.",
             "Distinguish exons from introns from the raw nucleotide sequence alone.",
             "FASTA → CSV ETL, character-level tokens, Bi-LSTM vs RNN, LSTM and GRU on identical splits.",
             "Bi-LSTM leads every metric: 99.80% accuracy, F1 0.998."],
        chart=dict(title="High sensitivity alone hides a model that guesses one way",
                   subtitle="Specificity on the same test split · Simple RNN reaches 0.998 sensitivity by calling almost everything an exon",
                   rows=[("Bi-LSTM", 1.000), ("GRU", 0.998), ("LSTM", 0.979), ("Simple RNN", 0.338)], fmt="{:.3f}",
                   highlight={"Bi-LSTM": COBALT, "Simple RNN": RISK}, xmax=1.12,
                   source="Source: Ensembl Genome Browser · 80/10/10 split · 60 epochs")),
    "visppy-cv": dict(
        stage="Build",
        head=("Build · Computer vision · Spatial intelligence", "Visppy",
              "Turn movement in physical spaces into decisions about layout, staffing, engagement and operations."),
        kpis=[("Centelha SE III", "Top 47", "approved in the preliminary Phase 2 general classification"),
              ("Case studies", "3", "stand activation, retail store, lecture room"),
              ("Customer footage published", "0", "decision layer only; privacy by design")],
        arc=["Stores, stands and rooms are run on intuition about how people move.",
             "Where does attention or congestion accumulate, and what should change?",
             "Zones, flows, dwell and occupancy from video, read with layout and measurement quality.",
             "Prioritised layout and staffing experiments, with explicit measurement limits."],
        chart=None),
    "mandacaru": dict(
        stage="Build",
        head=("Build · Document AI · STI/UFS", "Mandacaru",
              "Intelligent document processing that turns institutional PDFs into structured, reusable records."),
        kpis=[("Fastest valid output", "176 s", "p50 for the best model alternative"),
              ("Export formats", "3", "CSV, XLSX and JSONL"),
              ("Document types", "4 + 1", "four institutional types and a generic fallback")],
        arc=["University teams read official PDFs and copy fields into spreadsheets by hand.",
             "Key fields stay trapped in layouts built for human reading.",
             "Validate, extract, classify, apply type-specific schemas, and benchmark model alternatives.",
             "A working upload-to-export flow; one alternative ruled out for breaking the output contract."],
        chart=dict(title="Only one alternative was both valid and fast",
                   subtitle="Recorded p50 latency per model alternative (seconds) · Alternative C failed the CSV contract",
                   rows=[("Alternative A · valid", 176.12), ("Alternative C · invalid CSV", 187.50),
                         ("Alternative B · valid", 445.30)], fmt="{:.0f} s",
                   highlight={"Alternative A · valid": COBALT, "Alternative C · invalid CSV": RISK},
                   source="Repository benchmark snapshot · not a production SLA")),
    "echo-womens-health-research-analytics": dict(
        stage="Build",
        head=("Build · Research analytics · Health", "ECHO Research Analytics",
              "Survey-based evaluation of a remote women's health training programme at UFS and Project ECHO."),
        kpis=[("Instructional scores", "8.66–9.45", "item means on a 0–10 scale; mode 10 on all 15"),
              ("Knowledge management", "3.95–4.68", "item means on a 1–5 scale"),
              ("Participant records published", "0", "aggregate outputs only")],
        arc=["A remote women's health training programme for primary-care professionals.",
             "Did participants rate the instruction and knowledge transfer as useful?",
             "Validated Likert scales, non-parametric tests, Spearman correlations, aggregate reporting.",
             "Consistently high ratings, strongest on work quality and usefulness."],
        chart=None),
    "abade": dict(
        stage="Build",
        head=("Build · Web · Static site", "Portfolio Site",
              "A one-page portfolio, built rather than templated. Three files, no framework, no dependencies."),
        kpis=[("Files", "3", "index.html, styles.css, script.js"),
              ("Dependencies", "0", "no build step, no bundler"),
              ("Brand tokens", "5", "Carbon, Graphite, Ivory, Steel, Cobalt")],
        arc=["A portfolio has to load fast and read like the work it presents.",
             "Templates look like every other portfolio and carry weight nobody needs.",
             "Hand-written HTML, CSS and vanilla JS on the ABADE system: Lato, diagonals, one accent.",
             "A static page that deploys anywhere with zero configuration."],
        chart=None),
}

PORTFOLIO = {
    "Validate": [("tracking-attribution-lab", "Can the event layer be trusted?"),
                 ("ab-testing-toolkit", "Did the change cause the lift?"),
                 ("marketing-mix-modeling", "Which channel caused the revenue?")],
    "Scale": [("unit-economics-olist", "Which channel pays for itself?"),
              ("paid-media-budget-optimizer", "Where does the next unit go?"),
              ("lead-scoring-api", "Who gets called first?"),
              ("growth-analytics-warehouse", "End to end, from spend to model"),
              ("marketing-analytics-portfolio", "From report to decision")],
    "Retain": [("clv-cohort-prediction", "Who deserves retention budget?"),
               ("churn-cost-sensitive", "Who gets the offer?")],
    "Build": [("carbon", "Bi-LSTM on human DNA"), ("visppy-cv", "Vision for physical spaces"),
              ("mandacaru", "Document AI for a university"), ("echo-health-analytics", "Health research analytics"),
              ("abade", "Portfolio site")],
}


def symbol_tile(size: int = 128) -> str:
    h = size * 0.5
    return svg(size, size, symbol((size - h * 1.2756) / 2, size * 0.25, h, IVORY), "ABADE symbol", CARBON)


def main() -> None:
    for repo, s in SPEC.items():
        out = REPOS / repo / "assets" / "brand"
        emit(out, "header", header, *s["head"])
        emit(out, "kpis", kpis, s["kpis"])
        emit(out, "arc", arc, s["arc"])
        emit(out, "track", track, s["stage"])
        if s["chart"]:
            c = dict(s["chart"])
            emit(out, "chart", bars, c.pop("title"), c.pop("subtitle"), c.pop("rows"), **c)
    out = REPOS / "arielabade" / "assets" / "brand"
    emit(out, "header", header, "Strategy · Data · Growth", "Ariel Abade",
         "Growth, data science and machine learning applied to revenue.")
    emit(out, "kpis", kpis, [("Years in growth", "~5", "paid media, SaaS growth and analytics"),
                             ("Public case studies", "15", "each with code, tests or documented limits"),
                             ("Method", "3 steps", "validate, scale, retain")])
    emit(out, "map", portfolio_map, PORTFOLIO)
    tile = symbol_tile()
    for p in ("growth-analytics-warehouse/assets/brand/symbol.svg", "growth-analytics-warehouse/app/assets/symbol.svg"):
        (REPOS / p).write_text(tile, encoding="utf-8")


if __name__ == "__main__":
    main()
