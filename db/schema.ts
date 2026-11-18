import { pgTable, text, integer, timestamp, jsonb, uniqueIndex, index } from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';

export const runs = pgTable('catalog_runs', {
  id: text().primaryKey(),
  status: text().notNull().default('running'),
  phase: text().notNull().default('discover'),
  page: integer().notNull().default(1),
  error: text(),
  leaseToken: text('lease_token'),
  leaseUntil: timestamp('lease_until', { withTimezone: true }),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
}, table => [uniqueIndex('one_running_catalog').on(table.status).where(sql`${table.status} = 'running'`)]);

export const drafts = pgTable('catalog_drafts', {
  id: text().primaryKey(),
  runId: text('run_id').notNull().references(() => runs.id),
  kind: text().notNull(),
  sourceKey: text('source_key').notNull(),
  name: text().notNull(),
  status: text().notNull().default('pending'),
  source: jsonb().notNull(),
  result: jsonb(),
  edited: jsonb(),
  error: text(),
  review: text().notNull().default('unreviewed'),
  notes: text().notNull().default(''),
  model: text(),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
}, table => [uniqueIndex('catalog_source_per_run').on(table.runId, table.kind, table.sourceKey), index('catalog_queue').on(table.runId, table.status)]);
