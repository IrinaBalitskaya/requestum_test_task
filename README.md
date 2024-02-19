# Requestum test task

Gets GitHub repo url and returns 5 similar projects with the most common contributors

## Installation

1. Clone repository from github
2. Go to requestum_test_task/backend dir

```bash
  cd requestum_test_task/backend
```
3. Create .env file using var names from .env.example and provided or generated GitHub API key:
```bash
https://github.com/settings/tokens
```

4. Go to root directory and run docker-compose:
```bash
  cd ..
  docker-compose up --build
```