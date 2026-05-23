**TileRT: Rescuing GPU Compute from Execution Boundaries**

I have worked on inference engines for years. I keep seeing the same thing. The spec sheet says 38 TB/s bandwidth. Your model has 42 GB of active parameters. You do the math. The ceiling should be 1000 tokens per second. Then you run it. You get dozens. That is a full order of magnitude off. Not a 10% tuning gap. It is 10x.

This is not a new problem. In 2023, people asked if the model fit on a GPU. In 2024, they asked how high continuous batching could push throughput. Then 2025 hit. The agentic era arrived. Users wait for the next token. They wait for the next tool call. They wait for the next reasoning step. Nobody cares how many tokens you serve in an hour. They care about one thing. They press Enter. When does the first token show up?

The TileRT team nailed this insight. Latency is becoming intelligence. This is not a metaphor. Under Test-Time Scaling, speed decides how deep a model can reason within a fixed budget. Inference speed is no longer just a cost metric. Speed is part of the capability itself.

So where is the root cause? One line in the TileRT blog stuck with me. I read it several times. GPUs do not lack compute. Compute is trapped between execution boundaries.

Traditional inference frameworks use a graph-to-operator-to-kernel model. Each operator launches separately. Each one synchronizes. Each one does a round trip to memory. This abstraction worked fine for training. The kernels were large enough. Launch overhead, sync overhead, and scheduling overhead all got amortized by heavy computation. But decode is different. Batch size drops to 1. The attention kernel lifetime falls into microseconds. Launch gaps. Cross-kernel barriers. Data spilling. TP synchronization. All the costs that batching used to hide come back.

You see something strange in the profiler. A kernel finishes before it fully warms up. The GPU repeats the same cycle. Launch. Load. Compute. Store. Sync. Every boundary breaks the data flow. It destroys locality. It forces re-synchronization. The bottleneck is not how fast GEMM runs. The bottleneck is whether the next stage can start immediately.

TileRT takes an aggressive approach. I think the direction is right. Stop launching kernels over and over. Statically unroll the entire model at compile time into one persistent Engine Kernel. The host launches once. Execution stays on the GPU.

The execution details are worth unpacking. It is not just concatenating all kernels into one big kernel. That would just move the problem. TileRT breaks operators into tile-level tasks. It schedules them across different warp groups. Each warp group has its own job. One does async data movement. Another does tensor compute. Another overlaps communication. The old pattern was load, barrier, compute, barrier. Now these phases overlap continuously at tile granularity. Intermediate results stay in registers, shared memory, and L2 cache. They do not get written back to global memory over and over.

The difference is obvious in the profiler. The GPU no longer looks like a device that keeps launching kernels. It looks like a continuously running pipeline.

But this only solves the single-card problem. At 8xNVL topology, another limit appears. The limit is homogeneous parallelism itself.

Most tensor parallelism frameworks assume every GPU rank runs the same logic. This made sense for training. Compute patterns were regular. Sync behavior was stable. Inference breaks this assumption. Sparse routing. Top-K selection. Dynamic indexing. Long-context attention. Multi-Token Prediction. More and more stages do not split evenly across cards. Forcing all ranks to run the same logic creates redundant computation. It causes excessive broadcasting. It amplifies synchronization.

TileRT asks a good question. If warps can specialize, why not GPUs? They extend warp specialization to block specialization. Then to GPU specialization. In the GLM-5.1 attention layer, GPU 0 runs the Sparse Indexer. That handles Top-K selection, sparse index building, and routing decisions. GPUs 1 through 7 run MLA. That covers RMSNorm, GEMM, Flash Sparse Attention, and AllReduce. Different stages use different scaling strategies. Sync-heavy stages run centrally. Stages that fit tensor parallelism run distributed.

Since different GPUs are already running different tasks, external NCCL orchestration becomes unnecessary. Communication naturally enters the execution pipeline, embedding directly into the tile flow. The entire attention layer requires only one Engine Kernel launch from the host.

Here are the numbers. GLM-5 FP8 hits 500 tokens per second. DeepSeek-V3.2 on 8xB200 reaches 600 tokens per second at batch size 1. With MTP set to 3, synthetic load hits 590. Real generation hits 440. Compare this to public benchmarks from vLLM and SGLang. The lead is not 10%.

But I have reservations. TileRT only supports 8xB200 today. That limitation itself is not fatal. What is fatal is what you face in production. Mixed short and long contexts. KV cache fragmentation. MTP accept and reject calls changing the flow on the fly. You do not see these in benchmarks. In production, they are lethal. The TileRT team admits this. Going from fast to consistently fast required multiple execution model rewrites. Many changes did not boost theoretical throughput. But they significantly improved tail latency.

What worries me more is the flexibility of persistent kernels. AOT static unrolling means model structure adaptation happens at compile time. Runtime dynamism is constrained. Think about it. Model architectures are evolving fast. MoE. MTP. Mixed sparse attention. Every architecture change may require re-pipelining the entire flow. This is not a theoretical concern. It is a wall that every production team hits.

Look further ahead, and the endgame is not TileRT itself. The team says this clearly. The next step is model-compiler-hardware co-design. When performance approaches hardware limits, the bottleneck is no longer one GEMM operator. The bottleneck is the structure of the execution pipeline. Conflicts between model architecture, memory hierarchy, communication topology, and routing patterns cannot be solved by runtime alone. Inference frameworks need to push upward into model design. They need to reach downward into hardware characteristics.

I fully agree with this trend. For the past decade, the GPU role was to maximize parallel throughput. The next few years may demand something different. Sustain an execution pipeline under extremely tight latency budgets. Inference systems are evolving from a collection of operator optimizations into real AI execution infrastructure.

TileRT is the most convincing attempt in this direction so far. But it is really posing the right question. The remaining answers? That is on the ecosystem.
