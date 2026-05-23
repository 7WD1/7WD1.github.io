Your model explains itself. You trust the explanation. You should not.

Post-hoc explanations are the standard tool for interpreting deep networks. GradCAM, LIME, Integrated Gradients — pick your favorite. They all share one assumption. They assume the explanation is independent of training. This paper from ICLR 2025 destroys that assumption. It shows that less than 10% of model parameters control most of the explanation quality. Those parameters live in the final classification layer. The probe matters more than the backbone.

The paper is called "How to Probe." The authors are Gairola, Böhle, Locatello, and Schiele. The finding is simple and devastating. The way you train your last layer decides whether your explanations are useful or garbage.

Here is the core insight. Everyone trains probes with cross-entropy loss. CE loss uses softmax. Softmax normalizes across all classes. This creates a softmax-invariance problem. The gradient-based attribution treats all classes symmetrically. The result is blurry, class-agnostic heatmaps. The explanation highlights everything and nothing.

The fix is embarrassingly simple. Use binary cross-entropy instead. BCE trains each class independently. There is no softmax normalization. Each class gets its own clean signal. The attributions become sharper. They localize to the right regions. The improvement is immediate and consistent across methods.

But the authors go further. They replace the linear probe with a B-cos MLP. B-cos networks enforce weight-input alignment during training. This alignment pressure makes the model inherently more interpretable. The authors apply B-cos probes on top of standard backbones. You keep your ResNet. You keep your ViT. You just swap the classification head.

The results speak for themselves. BCE probes localize better than CE probes. B-cos probes localize better than linear probes. The combination of BCE and B-cos is the best. This holds across fully-supervised, self-supervised, and contrastive vision-language models. It holds across GradCAM, Integrated Gradients, and other attribution methods. It holds across multiple evaluation metrics.

Why does this matter? The interpretability community has spent years building better attribution methods. This paper says the problem was never the method. The problem was the probe. A simple training change fixes more than years of method engineering. That is a humbling result.

The practical implications are real. If you deploy models in healthcare or autonomous driving, you need reliable explanations. Right now your explanations might be wrong. Not because the method is bad. Because your probe was trained with the wrong loss. You can fix this today. Retrain your classification head with BCE. Replace it with a B-cos probe. Done.

The paper tests on ImageNet-scale experiments. It covers CNNs and transformers. It covers CLIP and DINO. The breadth of evaluation is impressive. The authors do not cherry-pick. They show the effect is systematic.

I have reservations. The improvements are measured on standard benchmarks. Real-world deployment introduces noise that benchmarks ignore. A sharper heatmap is not always a correct heatmap. The paper acknowledges this gap. But it could address it more directly.

The B-cos probe adds complexity to the pipeline. You need to retrain your classification layer. For large-scale deployment, this is non-trivial. The paper shows it is worth the effort. But the engineering cost is real.

The softmax-invariance argument is elegant. But BCE is not a universal solution. Multi-label tasks already use BCE. The insight is most impactful for multi-class single-label setups. The paper focuses on these cases. That is the right scope.

There is a deeper philosophical point. The interpretability field has treated explanations as post-processing. You train the model. Then you explain it. This paper shows the two steps are coupled. You cannot separate training from explaining. The model and the explanation are one system. We need to stop pretending otherwise.

The writing in the paper is clear. The experiments are thorough. The code is public on GitHub. The authors deserve credit for reproducibility.

Here is my take. This is one of the most important interpretability papers of 2025. Not because it is complex. Because it is simple. It identifies a basic flaw in how we evaluate explanations. Then it fixes the flaw with a one-line change to the loss function. That is good science.

If you work on model interpretability, read this paper. If you deploy models that need explanations, implement these changes. Stop trusting CE-trained probes. Your explanations are lying to you.

The paper is arXiv:2503.00641. Go read it. Then fix your probes.
