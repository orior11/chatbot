import { useState, useEffect } from "react";

/**
 * Persist a value in localStorage; falls back to default on invalid/missing.
 */
export function useLocalStorage(key, defaultValue, validate = () => true) {
  const [value, setValue] = useState(() => {
    try {
      const stored = localStorage.getItem(key);
      if (stored != null && validate(stored)) return stored;
    } catch (_) {}
    return defaultValue;
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, value);
    } catch (_) {}
  }, [key, value]);

  return [value, setValue];
}
