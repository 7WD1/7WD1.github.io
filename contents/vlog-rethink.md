Interpretability needs a new definition for the LLM era. The old definition is not wrong. The subject of study has changed.

We used to explain a ResNet. The task was clear. Why was this image classified as a cat? Feature attribution gave the answer. Pixel-level contributions. Explanations mapped cleanly to predictions. You could point to a pixel. You could see the evidence. LLMs changed the game. A language model's output is not a single class label. It is text that may contain reasoning, creativity, and fact retrieval. What do you explain? The entire generation process? Or a specific token choice?

This paper asks better questions than it answers. It challenges several deep industry assumptions.

First is the granularity problem. Traditional XAI works at the feature level. Which input dimension matters most? But LLM inputs are token sequences. Outputs are token sequences too. Feature attribution at the token level is nearly useless. Token "the" has high contribution to the output. What does that tell you? Nothing useful. We need coarser granularity. Concept level. Sentence level. Reasoning step level.

Second is the definition of faithfulness itself. In the small model era, you could verify faithfulness through input perturbation. Change one feature. Check if the output changes as expected. LLM input spaces are enormous. The perturbation space grows exponentially. Exhaustive verification is impossible. Sampling verification is unreliable. Faithfulness becomes a concept we cannot rigorously define.

Third is the audience problem. Engineers need technical explanations. Regular users need something entirely different. Old XAI methods assumed an engineer audience. In the LLM era, explanations must serve everyone. This means natural language. But natural language explanations have inherently low faithfulness. You cannot precisely describe complex computations in plain words.

The paper does not offer a complete solution. But it points in the right direction. Interpretability is not one technical problem. It is a collection of problems. Different model scales need different approaches. Different applications need different formats. Different audiences need different depths. A one-size-fits-all framework cannot work anymore.

I would add this. We may need to abandon the goal of perfect explanations. In the small model era, we pursued faithful explanations for every prediction. For LLMs, this goal is neither feasible nor necessary. Nobody cares why the model chose "however" over "but." Users need to know: is the answer reliable? When might it fail?

The real shift: stop explaining every prediction. Start building systems users can trust. This paper is one of few that recognizes this shift. The field needs more work like this. Less method tinkering. More foundational questioning.