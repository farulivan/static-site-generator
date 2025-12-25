# ⏮️ The Safe Rollback

**Friday, 5:08 PM**

You create a quick revert commit:

```bash
git revert abc123 -m "Revert dependency updates - causing OOM in build"
git push origin main
```

The pipeline triggers. You watch nervously.

**5:11 PM** - Build starts...  
**5:14 PM** - Build completes successfully  
**5:16 PM** - Deployment successful! ✅

> **#incidents**: "Site is back online. What happened?"

You post in the channel:

_"Reverted recent dependency updates that caused build memory issues. Site is stable. Will investigate proper fix on Monday with increased build resources."_

Your manager gives you a 👍 reaction.

## 🎉 Victory: The Pragmatist

You chose the safe, boring solution. Production is up. You can fix it properly next week with proper testing.

**Ending Stats:**
- Time to resolution: 21 minutes
- Reputation: +35 (Reliable under pressure)
- Stress level: Medium → Low
- Career trajectory: Steady →

---

### What you learned:
- Sometimes the best fix is a revert
- Ship working code, optimize later
- Friday deployments are dangerous
- You can always fix it properly on Monday

**Technical debt created:** Medium (need to update dependencies properly)

[🏠 Start a new adventure](/start) | [📊 View all endings](/endings)
