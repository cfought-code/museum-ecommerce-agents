# Catalog Studio

Catalog Studio gathers public product and artist information from `https://store.toledomuseum.org`, extracts inputs for the existing product and artist workflows, and uses an LLM to produce reviewable drafts. It does not require a GitHub token or dispatch the legacy single-item GitHub workflows. It never writes to Shopify.

## Open the workspace

After deployment, open the site's home page. The workspace requires an invited Netlify Identity account with the `admin` role, or a verified Netlify team-login session on a site protected by team login. Anonymous visitors cannot read drafts, start runs, or consume inference credits.

For the first Identity administrator, invite the account through the project's Identity dashboard, accept the email invitation on the site, then assign the `admin` role to that account in Identity. The page handles invitation acceptance and password recovery. No public signup form is provided; an ordinary registered account has no workspace privileges. Identity is activated by this implementation. The first administrator role must be assigned through the dashboard.

## Run the full catalog

1. Select **Start full catalog run**. This creates a persisted job; deployment alone does not start generation.
2. In production, a scheduled function advances the active job once per minute. Each tick processes one catalog page or one draft, with a 23-second network/inference deadline. Use **Process next batch** to advance a run manually, including in a deploy preview, where scheduled execution does not run.
3. Discovery pages through the public Shopify product feed, 100 products at a time, until it returns an empty page. It deduplicates product handles and stops on repeated pages rather than silently claiming full coverage. Coverage includes publicly exposed products only, not private, unpublished, or hidden catalog records.
4. Product processing combines catalog data with public product pages and up to three same-store artist/about links. Only explicit identification of an artist, maker, designer, or collective should create an artist entry. A vendor is not automatically an artist. Artist entries are grouped by normalized name and aggregate up to 12 source documents before the artist generation phase.
5. Inspect extracted inputs and their exact source quotations. Missing values remain null and are flagged. All copy still requires human review: exact quotation validation proves a quotation exists, not that every interpretation or generated sentence is correct. Namesakes may require manual disambiguation; name normalization alone does not establish identity.
6. Edit draft copy, add notes, and save a review status. The original model output and the source evidence remain available alongside edits. Approval is an internal review label and does not publish anything.
7. Download **drafts & source inputs** for a JSON export of the current run, including pending or failed entries, original drafts, edits, review decisions, and source documents. The input field names correspond to the existing Python/GitHub workflows. Unknown required fields must be supplied before using those legacy workflows.

Each batch uses a database lease so scheduled and manual processing cannot generate the same queue concurrently. Progress, source snapshots, reviews, and errors survive process restarts and deploys. Pause stops new batches; a batch already executing may finish. Resume or retry preserves completed work. A new full run makes a fresh snapshot without deleting previous database records; the current UI and export show the latest run. Previous runs remain in the database.

## Blocked public access

During implementation, the store returned Cloudflare HTTP 403 challenges for its home page, product feed, and sitemap. Catalog generation could not be tested against live store content. The automation treats denied access, redirects, robots exclusions, invalid feeds, and empty catalogs as explicit blocked states. It does not bypass access controls or substitute the four-row sample CSV for the full catalog.

Restore or permit normal public access to the catalog feed and product pages, then select **Retry blocked run**. Missing biography details, media, locations, statements, and product facts are flagged for review rather than invented. Artist discovery is limited to evidence linked from publicly listed products; artists without publicly available product evidence cannot be claimed as covered.

Rate limits, authorization failures, service errors, and batch deadlines block a run for explicit retry. Individual generation/evidence-validation failures are recorded while the remaining entries continue; the run ends blocked if failed entries remain. Retry resets failed entries, preserving successful drafts and reviews.

## Platform and verification

The API runs on a Netlify Server. Netlify Database stores jobs and drafts through Drizzle; the schema is `db/schema.ts`. A generated migration is included under `netlify/database/migrations/` and is applied by the platform on deployment. Do not run manual schema changes. Node.js 24 is required. The scheduled worker runs only saved active jobs; it does not create a new run every minute.

Inference uses `gpt-5.4-mini` through Netlify AI Gateway with the official OpenAI SDK, without a separate provider key. Each product and each identified artist uses one inference request. Large catalogs incur inference usage and may take many hours at one item per minute. Source pages are untrusted input, and source instructions are never used to operate the application. Model output is validated as structured data and source quotes are checked against supplied documents.

Run `npm test` for source/evidence safeguards and `npm run typecheck` for type checks. Use `netlify dev --port 8889` for local route checks. Identity itself requires the deployed Netlify runtime. The browser loads the pinned Identity client from esm.sh and fonts from Google Fonts. No build command is necessary for the static workspace; server and scheduled-function packaging are handled by Netlify.

The existing Python agents and GitHub workflows remain available. This site-wide automation removes the need to manually enter their inputs one product at a time, while keeping all results as drafts for review.
