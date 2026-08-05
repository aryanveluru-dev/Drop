import express, { type Express, type NextFunction, type Request, type Response } from 'express';
import type { Config } from './config.js';
import type { Database } from './db.js';
import { createRouter } from './routes.js';

export interface AppOptions {
  db: Database;
  config: Config;
}

export function createApp({ db, config }: AppOptions): Express {
  const app = express();

  app.disable('x-powered-by');
  app.use(express.json({ limit: '64kb' }));

  app.get('/health', (_req: Request, res: Response) => {
    res.json({ ok: true });
  });

  app.use(createRouter(db, config));

  app.use((_req: Request, res: Response) => {
    res.status(404).json({ error: 'not_found', message: 'No such endpoint' });
  });

  app.use((error: unknown, _req: Request, res: Response, _next: NextFunction) => {
    if (error instanceof SyntaxError && 'body' in error) {
      res.status(400).json({ error: 'invalid_json', message: 'Request body is not valid JSON' });
      return;
    }
    console.error('Unhandled error:', error);
    res.status(500).json({ error: 'internal_error', message: 'Something went wrong' });
  });

  return app;
}
