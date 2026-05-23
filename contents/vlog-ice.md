Using LLMs to explain black-box decisions has obvious appeal. You need no model access. No gradients. No training modifications. Just input data, model outputs, and a smart enough LLM.

In-Context Explainers does exactly this. Feed input-output pairs from a black-box model into an LLM as context examples. The LLM infers the decision logic. Then it generates natural language explanations. Simple idea. But the implementation details matter enormously. How you organize the examples in the prompt determines how well the LLM infers decision rules from limited samples.

Experiments across multiple datasets show comprehensibility scores beating LIME and SHAP. No surprise there. Natural language is easier to understand than numerical scores. But I care more about faithfulness. How consistent are LLM explanations with actual black-box decision processes?

The answer depends on complexity. For simple decision rules, faithfulness is high. The LLM correctly identifies linear thresholds. For complex nonlinear boundaries, faithfulness drops significantly. LLMs prefer generating simple linear explanations. Even when real decision logic is highly nonlinear. This is a fundamental limitation. Explanations are constrained by the LLM's own reasoning preferences.

An interesting experiment compares explanation quality across LLM scales. Larger models produce more faithful explanations. No surprise. But this raises an awkward question. If you need GPT-4 to explain a tiny model, just use GPT-4. The economics do not make sense.

I am cautious about practical value here. The biggest strength of In-Context Explainers is also its biggest weakness. No internal model access. You cannot reverse-engineer a system from the outside. There are hard limits. Like someone who never opened a car hood trying to explain engine noise. They can make educated guesses. They cannot truly diagnose the problem.

That said, In-Context Explainers provide something unprecedented for non-technical users. No need to understand SHAP values or attention weights. Just read natural language. For user education and initial model debugging, this tool has real value.

The future of this direction depends on one question. Can natural language explanation faithfulness approach numerical method levels? If yes, this becomes the default XAI approach. If no, it remains a pretty toy with limited practical impact. We do not know yet.