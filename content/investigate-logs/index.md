# 🔍 Investigating the Logs

**Friday, 4:52 PM**

You take a deep breath and open the CI/CD dashboard. The logs are a mess, but you're a professional. You've debugged worse.

The error message stares back at you:

```
Step 7/12: RUN npm run build
FATAL ERROR: Reached heap limit Allocation failed
JavaScript heap out of memory
```

Interesting. The build is running out of memory. But this worked yesterday...

You check the recent commits:

```
feat: add new analytics dashboard
chore: update dependencies
fix: typo in README
```

Two paths emerge in your investigation:

## 🔧 [Check the CI/CD pipeline configuration](/investigate-logs/check-ci-pipeline)

Maybe someone changed the Docker container specs or the build configuration. The pipeline itself might be misconfigured.

## 📦 [Investigate the dependency updates](/investigate-logs/blame-dependencies)

That `chore: update dependencies` commit looks suspicious. Dependencies are always the culprit, right?

---

**Time elapsed: 5 minutes**

_The CEO is still in the channel. Choose your investigation path._
