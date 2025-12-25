# 📦 Dependency Investigation

**Friday, 5:01 PM**

You run `git diff HEAD~1 package.json` and your jaw drops:

```diff
  "dependencies": {
-   "chart.js": "^3.9.1",
+   "chart.js": "^4.4.0",
+   "react-big-calendar": "^1.8.5",
+   "moment": "^2.29.4",
+   "moment-timezone": "^0.5.43",
+   "lodash": "^4.17.21"
  }
```

Someone updated Chart.js to v4 (breaking changes!) and added a bunch of heavy libraries. The bundle size probably exploded.

You check the bundle analyzer output from the last successful build: **2.3 MB**

Current build attempt: **8.7 MB** 😱

## ⏮️ [Rollback the dependencies](/investigate-logs/blame-dependencies/rollback)

Revert the package.json to the previous version. Ship the old code. Fix it properly on Monday. Safe and boring.

## 🚀 [Update ALL dependencies to latest](/investigate-logs/blame-dependencies/update-all)

Maybe the issue is that we're not on the LATEST latest? Update everything to the newest versions. YOLO.

---

**Time elapsed: 14 minutes**

_Dependencies: the cause of, and solution to, all of life's problems._
