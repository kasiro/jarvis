# TypeScript Code Style Guide

## Strict Mode Configuration

All TypeScript code must use strict mode:

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

## Naming Conventions

### General Rules
- **Files & Directories**: `kebab-case` or `snake_case` (e.g., `command-parser.ts`)
- **Classes & Interfaces**: `PascalCase` (e.g., `CommandExecutor`)
- **Variables & Functions**: `camelCase` (e.g., `processCommand()`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_VOLUME`)
- **Types & Type Aliases**: `PascalCase` (e.g., `CommandConfig`)
- **Generics**: `PascalCase`, single letter for simple (e.g., `T`, `K`, `V`)

### Examples
```typescript
// ✅ Good
interface UserConfig {
  volume: number;
  language: string;
}

const DEFAULT_TIMEOUT = 5000;

function processCommand(cmd: string): Promise<void> {
  // ...
}

// ❌ Bad
interface user_config {
  volume: number;
}

const default_timeout = 5000;
```

## Type Definitions

### Prefer Interfaces for Objects
```typescript
// ✅ Good - interface for object shape
interface Command {
  name: string;
  handler: (args: string[]) => Promise<void>;
  description?: string;
}

// ✅ Good - type for unions and primitives
type CommandStatus = 'pending' | 'running' | 'completed' | 'failed';
type Result<T> = { ok: true; value: T } | { ok: false; error: string };
```

### Avoid `any`
```typescript
// ✅ Good - proper typing
interface ApiResponse<T> {
  data: T;
  status: number;
}

async function fetchWeather(city: string): Promise<ApiResponse<Weather>> {
  // ...
}

// ❌ Bad - using any
async function fetchWeather(city: string): Promise<any> {
  // ...
}
```

### Use Utility Types
```typescript
// ✅ Good - utility types
type PartialConfig = Partial<CommandConfig>;
type ReadonlyState = Readonly<AppState>;
type CommandKeys = keyof Command;

// ✅ Good - custom mapped types
type Async<T> = {
  [K in keyof T]: T[K] extends (...args: any[]) => any
    ? (...args: Parameters<T[K]>) => Promise<ReturnType<T[K]>>
    : T[K]
};
```

## Code Organization

### Import Order
1. Third-party libraries
2. Internal modules (alias: `@/` or relative)
3. Type imports

```typescript
// ✅ Good - organized imports
import { useEffect, useState } from 'react';
import { toast } from 'react-hot-toast';

import { Command } from '@/types/command';
import { useJarvis } from '@/hooks/useJarvis';

import type { FC } from 'react';
import type { CommandConfig } from './types';
```

### File Structure
```typescript
// ✅ Good - clear structure
import { useState } from 'react';

// Types
interface Props {
  initialVolume: number;
}

// Component
export const VolumeControl: FC<Props> = ({ initialVolume }) => {
  const [volume, setVolume] = useState(initialVolume);
  
  // Handlers
  const handleVolumeChange = (newVolume: number) => {
    setVolume(newVolume);
  };
  
  // Effects
  useEffect(() => {
    // ...
  }, []);
  
  // Render
  return (
    <div>
      <input
        type="range"
        min="0"
        max="100"
        value={volume}
        onChange={(e) => handleVolumeChange(Number(e.target.value))}
      />
    </div>
  );
};
```

## Error Handling

### Typed Errors
```typescript
// ✅ Good - custom error class
class JarvisError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'JarvisError';
  }
}

// ✅ Good - error handling with types
async function executeCommand(cmd: Command): Promise<Result<void>> {
  try {
    await cmd.handler();
    return { ok: true, value: undefined };
  } catch (error) {
    if (error instanceof JarvisError) {
      return { ok: false, error: error.message };
    }
    return { ok: false, error: 'Unknown error' };
  }
}
```

### Avoid Silent Failures
```typescript
// ✅ Good - explicit error handling
async function loadConfig(): Promise<Config> {
  const response = await fetch('/api/config');
  
  if (!response.ok) {
    throw new JarvisError('Config load failed', 'CONFIG_LOAD', {
      status: response.status,
    });
  }
  
  return response.json();
}

// ❌ Bad - silent failure
async function loadConfig(): Promise<Config | null> {
  try {
    return await fetch('/api/config').then(r => r.json());
  } catch {
    return null; // What went wrong?
  }
}
```

## Async/Await

### Prefer Async/Await over Promises
```typescript
// ✅ Good - async/await
async function processCommands(commands: string[]): Promise<void> {
  for (const cmd of commands) {
    await executeCommand(cmd);
  }
}

// ❌ Bad - promise chains
function processCommands(commands: string[]): Promise<void> {
  return commands.reduce(
    (promise, cmd) => promise.then(() => executeCommand(cmd)),
    Promise.resolve()
  );
}
```

### Error Handling in Async
```typescript
// ✅ Good - try/catch with specific errors
async function fetchWithRetry(url: string, retries = 3): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response;
    } catch (error) {
      if (i === retries - 1) throw error;
      await delay(1000 * (i + 1));
    }
  }
  throw new Error('Unreachable');
}
```

## React/Svelte Guidelines

### Component Props
```typescript
// ✅ Good - typed props with defaults
interface VolumeSliderProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  disabled?: boolean;
}

export const VolumeSlider: FC<VolumeSliderProps> = ({
  value,
  onChange,
  min = 0,
  max = 100,
  disabled = false,
}) => {
  // ...
};
```

### Hooks
```typescript
// ✅ Good - typed custom hook
interface UseVoiceRecognitionReturn {
  isListening: boolean;
  transcript: string;
  startListening: () => void;
  stopListening: () => void;
}

export function useVoiceRecognition(): UseVoiceRecognitionReturn {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  
  // ...
  
  return {
    isListening,
    transcript,
    startListening,
    stopListening,
  };
}
```

## Testing

### Unit Tests with Jest/Vitest
```typescript
// ✅ Good - typed tests
import { describe, it, expect, vi } from 'vitest';

describe('CommandParser', () => {
  it('should parse simple command', () => {
    const result = parseCommand('открыть браузер');
    
    expect(result).toEqual({
      action: 'open',
      target: 'browser',
      args: [],
    });
  });
  
  it('should handle errors gracefully', () => {
    expect(() => parseCommand('')).toThrow(CommandParseError);
  });
});
```

### Mocking
```typescript
// ✅ Good - typed mocks
const mockFetch = vi.fn<(url: string) => Promise<Response>>();

vi.mock('@/api/weather', () => ({
  fetchWeather: mockFetch,
}));
```

## ESLint Configuration

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

## Code Review Checklist

- [ ] Нет `any` типов
- [ ] Все функции имеют явные возвращаемые типы
- [ ] Ошибки типизированы
- [ ] Импорт организован по порядку
- [ ] Тесты покрывают критическую логику
- [ ] ESLint без ошибок
- [ ] Prettier применен

---

**Based on**: TypeScript Handbook, Google TypeScript Style Guide  
**Last Updated**: 2026-02-23
