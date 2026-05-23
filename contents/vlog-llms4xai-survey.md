Using LLMs for explainability has exploded in the last two years. Most papers in this space are noise. This survey is different. It actually organizes the chaos.

The core problem is simple. Traditional XAI methods need humans to design explanation formats. SHAP values. Heatmaps. Decision boundary plots. Engineers choose these formats. LLMs break this limit. They generate natural language explanations. They answer follow-up questions. They adjust explanation granularity for different audiences.

The survey sorts methods into three buckets. LLMs as explainers directly interpret black-box predictions. LLMs as evaluators judge explanation quality from other methods. LLMs as enhancers convert traditional XAI outputs into natural language.

The most valuable section analyzes the faithfulness versus comprehensibility trade-off. Traditional XAI methods have relatively high faithfulness but low comprehensibility. Regular users cannot read SHAP values. LLM-generated explanations have high comprehensibility but questionable faithfulness. How do you verify the LLM explanation actually reflects the black-box decision process?

The survey identifies a critical gap in evaluation. Most work uses human judgment as the gold standard. Humans rate explanations as reasonable. But humans are good at being persuaded by plausible narratives. They are bad at judging whether narratives are faithful. This creates a dangerous loop. LLM explanations get more fluent. Humans get more satisfied. But satisfaction and faithfulness may have zero correlation.

The LLM-as-explainer approach has a fundamental problem. You use one black box to explain another. Unless you have independent verification, you are just shifting trust. The LLM-as-enhancer approach is slightly better. Base explanations come from verifiable traditional methods. But the enhancement step itself introduces uncontrolled variables.

The section on conversational explanations is forward-looking. Instead of one-shot explanations, users can ask follow-up questions. Why is this feature important? What if this feature value changes? This interactive format is valuable in healthcare and finance. But each extra dialogue round means another LLM call. Latency and cost become real problems.

The survey's biggest contribution is structural. It maps a messy field into clear categories. If you work on LLM plus XAI, this is required reading. But you may feel anxious after reading it. The basic evaluation problem remains unsolved. Papers are flying everywhere. The foundation is shaky.

We need standardized faithfulness benchmarks. We need evaluation protocols that separate fluency from accuracy. Until then, every claim in this space should be read with healthy skepticism. The survey implicitly makes this point. It is the most honest thing about it.