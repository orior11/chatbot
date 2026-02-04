# GitHub Upload Commands

Run these from the **project root** (`c:\Users\PinhasZ\Chatbot`) in order.

## 1. Initialize (if not already a git repo)

```bash
git init
```

## 2. Add remote

```bash
git remote add origin https://github.com/orior11/chatbot.git
```

If `origin` already exists with a different URL:

```bash
git remote set-url origin https://github.com/orior11/chatbot.git
```

## 3. Stage and verify

```bash
git add .
git status
```

Confirm that `.env`, `node_modules`, `venv`, and `backend/chat_logs.xlsx` do **not** appear (they are in `.gitignore`).

## 4. Commit

```bash
git commit -m "Refactor: full-stack chatbot with FastAPI backend and React frontend"
```

## 5. Set main branch and push

```bash
git branch -M main
git push -u origin main
```

## If the remote already has commits

- **Replace remote history** (overwrites existing repo content):
  ```bash
  git push -u origin main --force
  ```

- **Merge with existing history** (keep both):
  ```bash
  git pull origin main --allow-unrelated-histories
  ```
  Resolve any conflicts, then:
  ```bash
  git push -u origin main
  ```
