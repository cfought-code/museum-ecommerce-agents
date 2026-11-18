import type { Config } from '@netlify/functions';
import { step } from '../../lib/pipeline.ts';

export default async () => {
  // A saved run is required. Deploying never starts a catalog generation run.
  await step();
};
export const config: Config = { schedule: '* * * * *' };
