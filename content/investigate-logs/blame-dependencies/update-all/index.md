# 🚀 Dependency Hell

**Friday, 5:05 PM**

You think: "If some updates caused issues, maybe we need ALL the updates!"

```bash
npm update --latest
npm install
```

Your `package.json` explodes with changes:

```
Updated 247 packages
Added 89 packages
Removed 12 packages
```

You commit and push. The build starts...

**5:08 PM** - Build fails: `Cannot find module 'react-dom/client'`  
**5:10 PM** - You fix that, push again  
**5:12 PM** - Build fails: `TypeError: createContext is not a function`  
**5:15 PM** - You fix that, push again  
**5:18 PM** - Build fails: `Breaking change in Chart.js v5 API`  
**5:22 PM** - You're fixing breaking changes one by one  
**5:35 PM** - Still failing  
**5:47 PM** - The senior engineer takes over

She reverts everything and fixes it properly in 10 minutes.

## ☠️ Game Over: Dependency Hell

You turned a simple memory issue into a nightmare of breaking changes. You made it worse.

**Ending Stats:**
- Time wasted: 42 minutes
- Reputation: -50 (Made it worse)
- Stress level: MAXIMUM
- Packages broken: 247
- Career trajectory: Downward ↘️

---

### What went wrong:
- Never update all dependencies during an incident
- You created 247 new problems
- Breaking changes need testing
- "Update everything" is never the answer

[🔄 Try again](/start) | [📊 View all endings](/endings)
