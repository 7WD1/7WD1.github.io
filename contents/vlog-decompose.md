You ran Integrated Gradients on your BERT model. The output looked like TV static. Every token got a similar score. Nothing stood out. You tweaked the baseline. You tried SmoothGrad. Still noise.

This is not your fault. Standard training does not care about attributions. The loss function optimizes for prediction accuracy. It ignores how gradients flow through the network. Representations get entangled. Features mix together. Attribution methods try to untangle them after the fact. They fail.

A new paper from 2024 tackles this head-on. "Decomposition-Enhanced Training for Post-Hoc Attributions In Language Models" proposes a simple fix. Change the training objective. Add a decomposition loss. This encourages the model to keep representations separable. Features stay distinct. Gradients flow cleanly.

The idea is elegant. Standard cross-entropy pushes all useful information into a tangled mess. The decomposition objective pushes back. It penalizes feature entanglement during training. The result: when you later run gradient attributions, they actually mean something.

The math is straightforward. You add a regularization term to the loss. The term measures per-dimension independence. Each hidden dimension gets its own contribution score. High independence means clean attributions. Low independence means noise. The training process optimizes for both accuracy and decomposability.

Experiments confirm the intuition. The authors test on sentiment analysis, NLI, and question answering. On all tasks, decomposition-trained models produce sharper, more faithful attributions. Humans agree with the attributions more often. Gradient noise drops significantly. Attribution faithfulness scores improve by 15-30% across benchmarks.

But here is the catch. You pay a price in accuracy. The decomposition objective competes with the main task. On some benchmarks, accuracy drops 1-3%. For production systems, even 1% matters. You trade prediction quality for interpretability. Whether this trade-off is worth it depends on your use case.

There is a deeper issue too. The decomposition objective makes assumptions about what "good" representations look like. It assumes independence is desirable. But neural networks often benefit from entangled features. Entanglement can encode useful invariances. Forcing decomposition might break these implicit representations.

The evaluation also has gaps. Faithfulness is measured against proxy metrics, not ground truth. Nobody knows if an attribution is actually correct. We only know it looks clean. We only know it looks cleaner. Looking cleaner and being more faithful are not the same thing.

I like the direction though. The core insight is correct. If you want good post-hoc explanations, you need to think about explainability during training. Retrofitting interpretability onto an opaque model has hard limits. This paper shows one way to shift the burden upstream.

The practical takeaway is clear. If your application demands interpretable attributions — healthcare, legal, finance — consider decomposition training. The accuracy cost is small. The interpretability gain is real. Just do not pretend it solves the fundamental problem. We still cannot fully explain why a language model makes any specific decision.

What we have is a better tool. Not a final answer. The gap between "attributions look good" and "we understand the model" remains wide open. But closing it even a little is worth the effort.