# Keyword measurement

This repository no longer needs a separate AI writer to research opportunities.

## Three distinct metrics
1. **Search volume:** approximate monthly searches from Google Ads Keyword Planner export.
2. **Ads competition:** Google Ads advertiser competition, NOT organic ranking difficulty.
3. **Organic keyword difficulty:** an independent 0-100 estimate from an SEO dataset such as DataForSEO. It is absent unless you provide it.

## Getting data

1. In Google Ads Keyword Planner, use *Discover new keywords* or *Get search volume and forecasts*. Select Canada and English for Canadian articles, or the target market for the intended page.
2. Export historical keyword statistics to CSV. Save as `data/keyword_metrics.csv` on your local computer.
3. Run `python keyword_metrics.py --input data/keyword_metrics.csv`.
4. Inspect `research_reports/keyword_opportunities.md` and CSV. Share them here, or commit the report to GitHub if it contains no private account information.
5. For organic difficulty, add a column named `organic_keyword_difficulty` populated from a separately sourced SEO provider. Do not insert guesses.

Do not commit raw exports if they contain private account IDs or other sensitive details. Automated Google Ads API access needs customer authentication, a developer token and appropriate access. A public keyword report cannot be generated from nothing.

## Selection criteria

Use real measured search demand, organic competitiveness, relevance to existing tools, and whether the top search results satisfy intent. Do not confuse low advertiser competition with easy organic rankings. A low difficulty score is an estimate, not proof.

The analyzer deliberately leaves missing measurements blank. It does not write blog posts or publish to Blogger.
