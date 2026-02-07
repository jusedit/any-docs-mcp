import { describe, it, expect } from 'vitest';
import { simpleStem } from '../markdown-parser';

describe('simpleStem', () => {
  it('returns short words unchanged', () => {
    expect(simpleStem('cat')).toBe('cat');
    expect(simpleStem('dog')).toBe('dog');
    expect(simpleStem('run')).toBe('run');
  });

  it('strips -ing suffix', () => {
    expect(simpleStem('running')).toBe('run');
    expect(simpleStem('walking')).toBe('walk');
    expect(simpleStem('managing')).toBe('manage');
  });

  it('strips -tion suffix', () => {
    expect(simpleStem('configuration')).toBe('configura');
    expect(simpleStem('installation')).toBe('installa');
  });

  it('strips -ed suffix', () => {
    expect(simpleStem('configured')).toBe('configur');
    expect(simpleStem('installed')).toBe('install');
  });

  it('strips -s suffix', () => {
    expect(simpleStem('functions')).toBe('function');
    expect(simpleStem('sections')).toBe('section');
  });

  it('strips -ly suffix', () => {
    expect(simpleStem('quickly')).toBe('quick');
    // 'easily' is protected from over-stemming
    expect(simpleStem('easily')).toBe('easily');
  });

  it('does not over-stem', () => {
    // 'string' is protected from becoming 'str'
    expect(simpleStem('string')).toBe('string');
    expect(simpleStem('ring')).toBe('ring');
  });

  it('handles edge cases', () => {
    expect(simpleStem('')).toBe('');
    expect(simpleStem('a')).toBe('a');
    expect(simpleStem('ab')).toBe('ab');
  });
});
