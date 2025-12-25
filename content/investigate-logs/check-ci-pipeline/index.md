# 🔧 Checking the CI/CD Pipeline

**Friday, 4:58 PM**

You dive into the `.gitlab-ci.yml` file (or `.github/workflows/deploy.yml` if you're a GitHub person). 

Something catches your eye immediately:

```yaml
build:
  image: node:18-alpine
  script:
    - npm ci
    - npm run build
  # memory: 2GB  <-- This line is commented out!
```

Wait. Someone commented out the memory limit? You check the blame:

```
Author: intern-alex
Date: Yesterday
Message: "cleanup: remove unused comments"
```

The intern. Of course. They thought it was just a comment, but it was actually configuring the container memory.

You also notice the analytics dashboard commit added a **massive** dependency that bloats the build.

## ✅ [Fix the YAML and restore memory limits](/investigate-logs/check-ci-pipeline/fix-yaml)

Uncomment the memory configuration, bump it to 4GB to handle the new dashboard, and redeploy. This is the right fix.

## 🔄 [Just restart the runners](/investigate-logs/check-ci-pipeline/restart-runners)

Maybe the runners are just stuck. Hit that restart button and pray. Sometimes it just works™.

---

**Time elapsed: 11 minutes**

_You found the smoking gun. Now fix it properly._
