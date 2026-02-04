/**
 * Centralized config for the frontend.
 * Backend URL: set VITE_API_URL in .env or it defaults to localhost:3002.
 */
export const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:3002";
export const CHAT_TIMEOUT_MS = 90_000; // 90 seconds for AI response
