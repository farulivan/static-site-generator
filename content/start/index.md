# 🚨 The Deployment Incident

**Friday, 4:47 PM**

You're about to leave for the weekend when Slack explodes with notifications. The production deployment you triggered 10 minutes ago has failed spectacularly. 

> **#incidents**: "Site is down. Customers can't login. Revenue is bleeding. WHO DEPLOYED?"

Your heart sinks. The deploy pipeline shows a cryptic error:

```
Error: Build failed at step 7/12
Exit code: 137
Container killed (OOMKilled)
```

The CEO just joined the channel. Your manager is typing...

**What do you do?**

## 🔍 [Investigate the logs methodically](/investigate-logs)

Take a deep breath. Debug like a professional. Check the CI/CD pipeline, review recent changes, and find the root cause.

## 😱 [Panic and try to fix it immediately](/panic-deploy)

No time to think! Just revert, force push, restart everything. What could go wrong?

---

_Your choices matter. Choose wisely, developer._
