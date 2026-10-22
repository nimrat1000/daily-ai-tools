# Content Automation Engine: Upgrade Plan

This branch starts the transition from a single AI-tools blogger into an automation system for TotalYields, FileFlipHub, MakeForToday, and a broad digital-products business.

## Existing assets
- Keep the existing Blogger OAuth publishing, Anthropic writing, image generation, Cloudinary and Telegram modules as starting points.
- Keep existing GitHub Actions manual dispatch disabled from scheduled publishing while we refactor.
- Keep main branch unchanged until tested.

## Automated pipeline
1. Topic discovery: Search Console queries, competitor gaps and real audience problems.
2. Research: collect reliable primary sources and verified numbers. Fail closed if unavailable.
3. Draft: friendly expert, conversational, practical examples, questions and trade-offs. No fictitious firsthand testing.
4. Assets: keyword-specific realistic hero art, sometimes witty; verified charts and real screenshots.
5. Quality gate: source verification, financial arithmetic, duplicates, useful tool links, alt text and image rights.
6. Approval queue: store drafts and block live publishing by default.
7. Publish: Blogger API only after approval and proper destination configuration.
8. Repurpose: original social carousels/reels using supported Meta scheduling, no spam automation.
9. Measure: impressions, clicks, outbound referrals, tool completions and sales; refresh winners.

## Brands
- TotalYields.com: finance guides and ETF comparisons -> CountYield.
- FileFlipHub: PDF, image and business-file guides -> the precise working tool.
- MakeForToday: seasonal designs, printables and invitations -> precise collection page.
- Digital publishing: ebooks, workbooks, templates and kits -> verified marketplace or store listings.

## Safety requirements
- No invented search volume, rankings, ETF statistics, product testing, screenshots or reviews.
- No unverified financial recommendations or figures.
- No duplicate mass-published content across sites.
- Require draft-first and manual approval for publication until the gates are tested.
- Never commit API keys or OAuth refresh tokens; use GitHub Actions Secrets.
- Limit AI and media API spending.

## Delivery stages
Stage 1: Configuration and architecture on this branch.
Stage 2: Refactor existing Python modules for brand-aware topics, validated source packs and draft creation.
Stage 3: Tests, dry-run workflow, manual approval and one Blogger sandbox draft.
Stage 4: Connect production blogs and analytics; activate schedule only after successful controlled tests.

Status: architecture staged, not deployed. No publication credentials, Blogger blogs or production jobs changed.