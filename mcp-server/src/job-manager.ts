export interface ScrapeJob {
  id: string;
  name: string;
  displayName: string;
  url: string;
  status: 'pending' | 'analyzing' | 'scraping' | 'completed' | 'failed';
  progress: {
    phase: string;
    current: number;
    total: number;
    currentUrl?: string;
  };
  startedAt: string;
  completedAt?: string;
  error?: string;
  result?: {
    totalPages: number;
    totalFiles: number;
    version: string;
  };
  logs: string[];
}

class JobManager {
  private jobs: Map<string, ScrapeJob> = new Map();
  private jobCounter = 0;

  createJob(name: string, displayName: string, url: string): string {
    const id = `job_${Date.now()}_${++this.jobCounter}`;
    const job: ScrapeJob = {
      id,
      name,
      displayName,
      url,
      status: 'pending',
      progress: {
        phase: 'Initializing',
        current: 0,
        total: 0
      },
      startedAt: new Date().toISOString(),
      logs: []
    };
    this.jobs.set(id, job);
    return id;
  }

  getJob(id: string): ScrapeJob | undefined {
    return this.jobs.get(id);
  }

  getAllJobs(): ScrapeJob[] {
    return Array.from(this.jobs.values());
  }

  getActiveJobs(): ScrapeJob[] {
    return this.getAllJobs().filter(j => 
      j.status === 'pending' || j.status === 'analyzing' || j.status === 'scraping'
    );
  }

  getJobByName(name: string): ScrapeJob | undefined {
    return this.getAllJobs().find(j => j.name === name && 
      (j.status === 'pending' || j.status === 'analyzing' || j.status === 'scraping'));
  }

  updateJob(id: string, updates: Partial<ScrapeJob>): void {
    const job = this.jobs.get(id);
    if (job) {
      Object.assign(job, updates);
    }
  }

  updateProgress(id: string, phase: string, current: number, total: number, currentUrl?: string): void {
    const job = this.jobs.get(id);
    if (job) {
      job.progress = { phase, current, total, currentUrl };
    }
  }

  completeJob(id: string, result: ScrapeJob['result']): void {
    const job = this.jobs.get(id);
    if (job) {
      job.status = 'completed';
      job.completedAt = new Date().toISOString();
      job.result = result;
      job.progress.phase = 'Completed';
    }
  }

  failJob(id: string, error: string): void {
    const job = this.jobs.get(id);
    if (job) {
      job.status = 'failed';
      job.completedAt = new Date().toISOString();
      job.error = error;
      job.progress.phase = 'Failed';
    }
  }

  addLog(id: string, message: string): void {
    const job = this.jobs.get(id);
    if (job) {
      const timestamp = new Date().toISOString();
      job.logs.push(`[${timestamp}] ${message}`);
      // Keep only last 1000 log lines to prevent memory issues
      if (job.logs.length > 1000) {
        job.logs = job.logs.slice(-1000);
      }
    }
  }

  getLogs(id: string, lines: number = 100): string[] {
    const job = this.jobs.get(id);
    if (!job) {
      return [];
    }
    const maxLines = Math.min(Math.max(1, lines), 1000);
    return job.logs.slice(-maxLines);
  }

  cleanupOldJobs(maxAgeMs: number = 24 * 60 * 60 * 1000): void {
    const now = Date.now();
    for (const [id, job] of this.jobs) {
      if (job.completedAt) {
        const completedTime = new Date(job.completedAt).getTime();
        if (now - completedTime > maxAgeMs) {
          this.jobs.delete(id);
        }
      }
    }
  }
}

export const jobManager = new JobManager();
