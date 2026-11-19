---
layout: section
---

<div class="kicker">Part 4</div>

# What this means

---

# Takeaways

<v-clicks>

- **Measure OOD, not just ID.** ID leaderboards don't predict which model survives a shift.
- **Know your shift.** Temporal is nearly free; sensor and scale are not.
- **Don't assume EO pretraining = robustness.** Generic models are just as robust, or more so.
- **A hypothesis:** pretraining archives skewed to particular sensors and regions may teach sensor- and geography-specific biases; ImageNet's diversity may be why it stays competitive.
- **Open direction:** test-time adaptation for EO shifts, which needs no labelled target data.

</v-clicks>

<!--
The pretraining-bias point is a hypothesis in the paper (§6.2), so keep the "may".
-->

---

# Limitations, and a living benchmark

<div class="grid grid-cols-2 gap-10 mt-6">
<div>

<v-clicks>

- Doesn't cover every possible shift
- Not every GFM is included; the set spans the dominant architectures and pretraining paradigms
- Trends are consistent across many models and tasks

</v-clicks>

</div>
<div v-click class="takeaway">

Designed so new tasks and models drop straight in: <b>contribute yours.</b>

</div>
</div>
