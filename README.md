# Keyword & Content Research Engine

Research-only GitHub automation for discovering source leads and analyzing verified keyword exports for websites and digital products.

**This repo does not write articles, generate images, use Anthropic/OpenAI APIs, or publish to Blogger/social media.** Research reports are read in ChatGPT, where content decisions and writing can happen separately.

## Projects
- TotalYields / CountYield: finance educational searches
- FileFlipHub: PDF, image and document workflows
- MakeForToday: invitations and printable guides
- Digital products: ebooks, workbooks and templates

## Run source research
GitHub Actions → **Keyword and Content Research** → Run workflow.
Scheduled runs are configured for Mondays and Thursdays at 12:15 UTC after this branch is merged into the default branch. The workflow collects Google News RSS leads, not organic keyword volumes.

Outputs are committed to `research_reports/latest.md` and `latest.json` and kept as downloadable Actions artifacts. Errors are reported rather than silently treated as good data.

## Evaluate measured keyword data
Export a CSV from Google Keyword Planner, then run:
```bash
python keyword_metrics.py --input path/to/keyword-planner-export.csv
```
Results appear in `research_reports/keyword_opportunities.csv` and `keyword_opportunities.md`. Advertiser competition and organic keyword difficulty are not interchangeable; missing scores remain blank.

See `KEYWORD_MEASUREMENT.md` for instructions. No Google Ads or third-party SEO provider API is connected yet.

## ChatGPT handoff
Ask ChatGPT to inspect `research_reports/latest.md` or an uploaded keyword report through your connected GitHub repository. ChatGPT can then research, assess, recommend and draft content here. **New research runs do not proactively message ChatGPT by themselves.**

## Safety
No credentials are required for the current RSS collector and local CSV analyzer. Avoid committing private Keyword Planner exports. No production publishing is enabled.
