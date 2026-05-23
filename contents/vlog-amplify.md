Post-hoc explanations can make models better. I thought this was a joke when I first heard it.

Explanations are for humans, right? You explain, you move on. You do not feed explanations back to the model. But Krishna and team built AMPLIFY. And it works. Not a marginal gain. A 10 to 25 percent accuracy jump.

The idea is straightforward. Standard flow: model predicts, then post-hoc methods explain. LIME, SHAP, gradient attribution. Humans read the explanation. AMPLIFY inserts a new step. It converts post-hoc explanations into natural language rationales. These rationales go back into the prompt for in-context learning. The model reads its own explanation. Then it predicts better next time.

Think of a student checking an answer key. They do a problem. They read the solution. The next similar problem goes better. This is the same idea. But there is a trap. Does the model actually learn from the explanation? Or does any extra text in the prompt help? Ablation studies address this. Random rationales help a little. Carefully constructed explanations help much more. The content matters.

Self-AMPLIFY goes further. It applies the same trick to small models. Small models cannot call GPT-4 for rationales. They generate their own. LIME gives feature importance. The model converts this to text. It feeds the text back to itself. EMNLP 2024 results show a 7B model matching a 13B model. Explanations buy you parameter efficiency.

But I have concerns. First, circular reasoning. You use model outputs to improve model inputs. This resembles self-training. Self-training has known problems. Errors compound. Biases amplify. AMPLIFY uses explanations as a buffer. This helps but does not fully solve the issue.

Second, faithfulness. LIME and SHAP are approximation methods. Their "explanations" may not reflect the model's real decision process. We have known this for years. If the explanation is unfaithful, does it still improve the model? Maybe. Maybe the improvement comes from something else entirely. The paper does not answer this directly.

Third, engineering cost. Every sample needs a post-hoc explanation run. Then rationale generation. Then another inference pass. Your compute bill triples or more. The gap between demo and production is enormous. Compute cost triples.

That said, the conceptual contribution is significant. AMPLIFY breaks the assumption that explanations are post-hoc analysis tools only. Explanations can be training signals. They can be self-improvement mechanisms. This mindset shift matters more than any single number.

If future work provides stronger faithfulness guarantees, this approach could become standard practice. For now, it is a beautiful idea. But it is not ready for production. The research community should take this direction seriously though. Connecting explanation to improvement is the most interesting direction in XAI right now.