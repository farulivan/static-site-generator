# 💥 Force Push to Main

**Friday, 4:51 PM**

Your fingers fly across the keyboard:

```bash
git revert HEAD
git push origin main --force --no-verify
```

The terminal pauses. Then:

```
! [remote rejected] main -> main (protected branch hook declined)
Protected branch update failed
```

Oh right. Main is protected. You need admin override.

You have the admin password (you definitely shouldn't have this). You could use it...

## 🙏 [Override protection and pray](/panic-deploy/force-push/pray)

Use the admin override. Force the push. Hope that the revert actually fixes things and doesn't make them worse.

## 🏃 [Abandon ship](/panic-deploy/force-push/run-away)

This is too much. Close the laptop. Turn off your phone. Move to a cabin in the woods. Become a carpenter.

---

**Time elapsed: 4 minutes**

_The nuclear option. Are you sure about this?_
