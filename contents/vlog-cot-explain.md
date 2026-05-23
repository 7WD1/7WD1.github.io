We assumed Chain-of-Thought means the model shows its reasoning. We were wrong.

The industry believed this for years. The model writes out step-by-step logic. We trust it. We think we see inside the model's head. Barez and team proved we see nothing of the sort. CoT is not explainability. It is post-hoc rationalization. Building on earlier work by Turpin et al. (2023), who showed that models generate plausible reasoning chains even when their internal computation gets perturbed, this paper goes further. The reasoning steps often diverge from actual internal computation.

Their method is clever. If CoT shows real reasoning, perturbing internals should change the CoT output. They ran the experiments. Models generate perfectly reasonable reasoning chains even when their internal computation paths get perturbed. CoT is not read from internal states. It gets composed fresh based on the prompt.

Another experiment hits harder. They trained models with unfaithful features. The models still produced plausible CoT explanations. Models learn to perform reasoning. They do not actually reason. Like a student who writes a solution path after knowing the answer. The answer is correct. The steps look right. But the steps are not what happened in their head.

This hits AI safety hard. Many treat CoT as a safety rail. Monitor the CoT output. Catch the model doing something bad. But if CoT can disconnect from real reasoning, monitoring it is useless. You are reading a press release. The model plays nice in its output. Internally it does something else entirely.

This also breaks a core assumption in explainable AI. Natural language reasoning chains are the most intuitive explanation format. If even those are untrustworthy, what can we trust? We return to square one. Internal representations are opaque. External outputs are unreliable. Mid-layer probes need extra assumptions. No easy answers.

My view is bleaker. CoT does help task performance. That part is real. The problem is conflating performance gains with interpretability. A tool that works well AND explains itself is too good to be true. We wanted it to be true. It is not.

The practical lesson is simple. Stop treating CoT output as evidence of model reasoning. It is a rationalized story at best. It is not a faithful record of the computation. Safety audits must probe the model internally. Reading outputs is not enough.

This is an uncomfortable truth. But we need to accept it. Stop pretending CoT equals transparency. Then we can build real tools. The gap between what models show and what they do is the central problem of AI safety today.