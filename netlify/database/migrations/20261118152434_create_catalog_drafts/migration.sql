CREATE TABLE "catalog_drafts" (
	"id" text PRIMARY KEY,
	"run_id" text NOT NULL,
	"kind" text NOT NULL,
	"source_key" text NOT NULL,
	"name" text NOT NULL,
	"status" text DEFAULT 'pending' NOT NULL,
	"source" jsonb NOT NULL,
	"result" jsonb,
	"edited" jsonb,
	"error" text,
	"review" text DEFAULT 'unreviewed' NOT NULL,
	"notes" text DEFAULT '' NOT NULL,
	"model" text,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "catalog_runs" (
	"id" text PRIMARY KEY,
	"status" text DEFAULT 'running' NOT NULL,
	"phase" text DEFAULT 'discover' NOT NULL,
	"page" integer DEFAULT 1 NOT NULL,
	"error" text,
	"lease_token" text,
	"lease_until" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX "catalog_source_per_run" ON "catalog_drafts" ("run_id","kind","source_key");--> statement-breakpoint
CREATE INDEX "catalog_queue" ON "catalog_drafts" ("run_id","status");--> statement-breakpoint
CREATE UNIQUE INDEX "one_running_catalog" ON "catalog_runs" ("status") WHERE "status" = 'running';--> statement-breakpoint
ALTER TABLE "catalog_drafts" ADD CONSTRAINT "catalog_drafts_run_id_catalog_runs_id_fkey" FOREIGN KEY ("run_id") REFERENCES "catalog_runs"("id");