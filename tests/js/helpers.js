/**
 * Mock factories for island state helper tests.
 *
 * Each factory returns a teardown function that restores the original state.
 * Call teardown in afterEach() to keep tests isolated.
 */
import { vi } from "vitest";

/**
 * Install a mock window.chirpIslands registry.
 * Returns { register: vi.fn(), teardown: () => void }.
 */
export function mockChirpIslands() {
  const register = vi.fn();
  window.chirpIslands = { register };
  return {
    register,
    teardown() {
      delete window.chirpIslands;
    },
  };
}

/**
 * Install a mock localStorage backed by a plain Map.
 * Returns { store: Map, teardown: () => void }.
 */
export function mockLocalStorage() {
  const store = new Map();
  const mock = {
    getItem: vi.fn((key) => store.get(key) ?? null),
    setItem: vi.fn((key, val) => store.set(key, String(val))),
    removeItem: vi.fn((key) => store.delete(key)),
    clear: vi.fn(() => store.clear()),
    get length() {
      return store.size;
    },
    key: vi.fn((i) => [...store.keys()][i] ?? null),
  };
  Object.defineProperty(window, "localStorage", { value: mock, writable: true, configurable: true });
  return {
    store,
    teardown() {
      store.clear();
    },
  };
}

/**
 * Install a mock localStorage whose every accessor throws, simulating the
 * Safari-private / sandboxed-iframe / quota-exceeded conditions where the
 * Storage API is present but raises on access (it throws rather than returning
 * null). Use this to prove guarded modules degrade gracefully.
 *
 * Returns { error, mock, teardown: () => void }. `error` is the
 * DOMException-like object each accessor throws so tests can assert against it.
 */
export function mockDeniedStorage() {
  const error = new DOMException("The operation is insecure.", "SecurityError");
  const reject = () => {
    throw error;
  };
  const mock = {
    getItem: vi.fn(reject),
    setItem: vi.fn(reject),
    removeItem: vi.fn(reject),
    clear: vi.fn(reject),
    get length() {
      throw error;
    },
    key: vi.fn(reject),
  };
  Object.defineProperty(window, "localStorage", { value: mock, writable: true, configurable: true });
  return {
    error,
    mock,
    teardown() {
      // Restore a benign Map-backed mock so later tests aren't poisoned.
      mockLocalStorage();
    },
  };
}

/**
 * Create a minimal island payload object for testing mount functions.
 *
 * @param {HTMLElement} element - The root DOM element for the island
 * @param {Object} props - Props to pass to the island
 * @param {Object} overrides - Additional payload fields (name, id, version)
 */
export function createPayload(element, props = {}, overrides = {}) {
  return {
    name: "test-island",
    id: "test-1",
    version: "1",
    element,
    props,
    ...overrides,
  };
}

/**
 * Create a spy-based api object matching the Chirp island API contract.
 * Returns { emitState, emitAction, emitError } — all vi.fn() spies.
 */
export function createMockApi() {
  return {
    emitState: vi.fn(),
    emitAction: vi.fn(),
    emitError: vi.fn(),
  };
}
