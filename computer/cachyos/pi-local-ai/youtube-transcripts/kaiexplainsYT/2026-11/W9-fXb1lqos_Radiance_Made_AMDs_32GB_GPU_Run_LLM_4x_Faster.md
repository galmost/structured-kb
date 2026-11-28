[00:00] Okay, so picture this. You've just spent
[00:02] $2,000 or close to it on a GPU, and you
[00:06] didn' buy it for gaming or for video
[00:08] editing. You bought it because you want
[00:10] to run AI locally since you're done
[00:12] paying for API subscriptions, you're
[00:14] done with rate limits, and you're done
[00:16] with your code being shipped off to some
[00:18] server you've never seen. What you want
[00:20] is your own machine running your own
[00:22] models and doing your own work. So you
[00:24] drop two grand on AMD's Radeon AI Pro R
[00:27] 9700, which gives you 32 gigs of VRAM on
[00:31] the brand new RDNA 4 architecture, and
[00:34] you've read the spec sheet and watched
[00:35] the reviews, so you are really pumped
[00:37] about it. And then you open your coding
[00:39] agent, paste in a medium-sized repo of
[00:42] maybe 50,000 tokens and hit enter, and
[00:45] then you wait, and you keep waiting, and
[00:47] nothing comes back because the cursor is
[00:49] just sitting there blinking at you like
[00:51] it's judging you while 30 seconds go by.
[00:53] At some point you start wondering if
[00:55] something broke, so you check the
[00:57] terminal and it is running, it's just
[00:59] slow. That was my experience. And if
[01:01] you've been running any kind of large
[01:03] language model locally on AMD hardware,
[01:06] there's a pretty good chance it was
[01:07] yours too. But the worst part was that
[01:09] you couldn't even blame the hardware
[01:11] because the specs looked great. We're
[01:13] talking 640 GB per second of memory
[01:16] bandwidth and 383 trillion 8-bit matrix
[01:21] operations per second. So on paper this
[01:23] card should fly.
[01:25] So what was actually going on with a
[01:26] card that looks that good and still
[01:28] leaves you staring at a blinking cursor?
[01:30] Now, what blew my mind when I finally
[01:32] understood it is that the chip was not
[01:34] slow at all. It was idle, almost
[01:37] completely idle, using less than 15% of
[01:40] what it was actually capable of. And the
[01:42] reason for that sits at the heart of how
[01:44] language models actually work.
[01:46] Understanding it is what makes this
[01:48] whole story so satisfying because
[01:50] someone fixed it. A developer, working
[01:52] mostly alone at first, wrote a new
[01:55] engine from scratch, and it changed
[01:57] everything about how this card performs.
[01:59] So we're going work out why the forex
[02:01] happened, where it actually lives in
[02:03] your real workflow, and whether this
[02:05] card is worth it at the price it's
[02:07] selling for right now. And to do that,
[02:09] we need to start with the card itself
[02:11] and with why so many people wanted one
[02:13] in the first place. Now, I think the
[02:15] case for this card is genuinely strong,
[02:18] but it is also really specific, which
[02:20] means you have to know exactly what
[02:22] you're buying it for. The Radeon AI Pro
[02:24] R9700 launched on October 27th of last
[02:27] year at $1,299.
[02:31] It is RDNA 4 with 64 compute units and,
[02:34] crucially, 32 GB of GDDR6 memory on a
[02:38] 256-bit bus moving data at 640 GB per
[02:42] second. And that 32 gigs is the reason
[02:45] people want this card.
[02:47] The model most people are running on it
[02:48] right now is Quen 3.8 27B, which is a
[02:52] really capable coding and reasoning
[02:54] model that fits comfortably in 32 GB of
[02:56] VRAM.
[02:57] A 6-bit class quantized copy comes in at
[02:59] about 24 GB and that leaves you roughly
[03:02] 8 GB for context. And that context is
[03:04] all the files, tool logs, stack traces,
[03:08] and conversation history that your
[03:09] coding agent is going to load into
[03:11] memory while it works. That is exactly
[03:13] the kind of setup that makes local AI
[03:16] actually useful for a developer. You get
[03:18] the full 27 billion parameter model and
[03:21] a real context window with no swapping
[03:23] to system RAM, so everything stays in
[03:25] VRAM and runs fast. Now, the other new
[03:28] 32 GB card is Nvidia's RTX 5090, which
[03:33] has GDDR7 running at 1,792
[03:37] GB per second, nearly three times the
[03:39] memory bandwidth of the R9700. And it is
[03:42] faster, it runs everything on Windows on
[03:45] day one, and it supports every tool out
[03:47] of the box. But it is also going for
[03:50] over $9,300
[03:52] on most US listings right now. There's
[03:54] also Intel's Arc Pro B70 with 32 gigs at
[03:58] 608 GB per second, which is honestly
[04:01] competitive with the R9700, but its
[04:04] software ecosystem is even younger. So,
[04:06] from a hardware standpoint, the R9700
[04:09] was always a compelling option. The
[04:11] problem, which people were complaining
[04:13] about in every forum, thread, and
[04:15] comment section for most of the past
[04:17] year, was the software. The standard
[04:20] engine most people were using was
[04:21] llama.cpp, which is a great project that
[04:24] runs everywhere, but on this specific
[04:26] card, with this specific workload, it
[04:29] was leaving an enormous amount of
[04:31] performance on the table. And I didn't
[04:32] understand why until I looked at the
[04:34] numbers. And to read those numbers
[04:36] properly, we first have to split the
[04:38] work a model does into its two halves.
[04:41] Now, this is the part that completely
[04:44] changed how I thought about all of this.
[04:46] Language model inference, which is just
[04:48] the process of running a model, has two
[04:50] completely different phases, and they
[04:52] are limited by completely different
[04:55] things. The first phase is called
[04:57] prefill, and it's the step where the
[04:59] model reads your prompt. So, all those
[05:01] tokens you just pasted in, your repo,
[05:04] your instructions, and your context have
[05:06] to be processed before the model can
[05:08] write a single word back.
[05:10] The second phase is called decode, which
[05:12] is where the model writes the answer one
[05:14] token at a time and sends each word to
[05:16] your screen. And the key insight is that
[05:18] prefill is compute-bound, meaning it is
[05:21] limited by how many math operations the
[05:23] chip can do per second. Decode is
[05:25] memory-bound, meaning it is limited by
[05:28] how fast the chip can read the model
[05:30] weights out of VRAM. So, these two
[05:32] phases hit completely different
[05:34] bottlenecks, and that is exactly what we
[05:36] see in the numbers. Oliver Solcer is a
[05:38] web developer in Vienna who's been doing
[05:40] some of the cleanest benchmarking I've
[05:42] seen on this card. When they ran Quen
[05:44] 3.8 27B on the R9700 with llama.cpp at a
[05:48] 16,000 token prompt, they got 888 tokens
[05:53] per second during prefill. To put that
[05:55] in real time, a 32,000 token prompt,
[05:58] which is a mid-sized repository with
[06:00] some instructions, sat there for 36.5
[06:04] seconds before the first word came out.
[06:06] And at 100,000 tokens, we are waiting
[06:09] two minutes and 18 seconds.
[06:11] Meanwhile, the writing speed, which is
[06:13] decode, sat between 33 and 47 tokens per
[06:17] second. And that isn't blazing, but it
[06:19] is workable. Now, this is the point
[06:22] where I had my weight what moment. AMD
[06:24] rates this card at 383 trillion
[06:27] eight-bit matrix operations per second.
[06:30] And during that 888 token per second
[06:32] prefill, it was using roughly 48
[06:34] trillion, which is about 1/8 of what the
[06:37] card can do. So the chip we're looking
[06:39] at wasn't slow. It was sitting mostly
[06:41] idle. And the reason is that llama CPP
[06:44] at the time wasn't using the specialized
[06:47] math units on RDNA 4 efficiently. So
[06:50] those units, the ones designed for
[06:51] exactly this kind of AI math, weren't
[06:54] getting fed properly.
[06:56] The kernel code, meaning the small
[06:58] programs that run directly on the GPU,
[07:00] wasn't written to take advantage of what
[07:02] RDNA 4 could actually do.
[07:04] But on the decode side, it is a
[07:06] different story. To generate one word,
[07:08] the card has to pull every single weight
[07:11] in the model out of memory. And for a
[07:13] four-bit copy of the 27B model, that is
[07:15] roughly 14.3 GB per token.
[07:19] At 640 GB per second, that puts the
[07:21] theoretical ceiling at about 45 tokens
[07:24] per second. And llama CPP was hitting 29
[07:27] to 30, which is about two-thirds of that
[07:29] ceiling. So on writing, the chip was
[07:31] actually being used reasonably
[07:33] efficiently. The real problem was on
[07:35] reading, which happens to be exactly the
[07:37] half that one developer sat down and
[07:39] wrote new code for.
[07:41] That engine is called radiance. And it
[07:43] was written, initially mostly alone, by
[07:45] a developer who goes by still dead code.
[07:48] It lives on Codeberg rather than GitHub,
[07:50] which is part of why it flew under the
[07:52] radar for a while.
[07:54] The origin story is that still dead code
[07:56] started by writing hand-tuned kernels
[07:58] for RDNA 4, which are those small,
[08:02] low-level programs that do the actual
[08:04] matrix math directly on the GPU
[08:06] hardware. And specifically, they target
[08:09] what AMD calls the AI accelerators on
[08:12] RDNA 4, which are the matrix multiply
[08:14] units we just saw sitting idle during
[08:17] prefill on Llama CPP. Those kernels went
[08:19] into a library called Liber 4D, and at
[08:22] first they were applied as patches on
[08:24] top of VLLM, an existing inference
[08:26] engine, but then Stilled Code dropped
[08:29] VLLM entirely and rewrote the whole
[08:31] engine from scratch in C++ and Hip,
[08:34] which is AMD's equivalent of Nvidia's
[08:36] CUDA programming framework. Version 1
[08:38] shipped on October 4th, and then things
[08:41] moved really fast with 41 tagged
[08:44] versions shipping in the 46 days after
[08:46] that. And as I write this, the
[08:48] repository has over 1,100
[08:51] commits from 58 different contributors,
[08:54] where the founders' accounts wrote about
[08:56] 5% of them. This went from one person
[08:59] side project to a genuine community
[09:01] engine very quickly. It runs in Docker.
[09:04] It's about 423 megabytes. It is Apache 2
[09:08] licensed, and it runs only on Linux,
[09:11] which matters a lot, and we'll come back
[09:12] to it near the end. Now, I want to flag
[09:14] something right up front because there's
[09:16] some genuine confusion about this in the
[09:18] YouTube comments and forum threads.
[09:21] There are at least four different things
[09:23] being called Radiance right now. There's
[09:25] Stilled Code's original VLLM patches,
[09:28] which are archived, and there's the
[09:30] standalone Radiance, which is the C++
[09:33] engine.
[09:34] And then there's VLLM Sly Radiance from
[09:36] a GitHub account called Sly Base, which
[09:39] is a VLLM image that uses the Liber 4D
[09:41] kernels.
[09:42] And there's a fork by Magic Coding Man
[09:44] that one AMD sponsored benchmark video
[09:47] actually linked to. The famous number,
[09:50] 3,900 tokens per second of reading
[09:52] speed, comes from Sly Base's benchmark.
[09:56] And according to Sly Base's own Reddit
[09:57] reply, those were described as benchmark
[10:00] numbers, not what you see in day-to-day
[10:02] work, since they were run on a community
[10:04] fine tune at a specific context length
[10:07] under specific conditions. And when Sly
[10:09] Base's own README compared against the
[10:11] reference stack on the same card, prompt
[10:14] reading landed somewhere between 4.5%
[10:16] faster and 0.7% slower, while writing
[10:20] was essentially a tie. So the kernels,
[10:23] Liber 4D, are what drive the
[10:24] performance, and multiple engines use
[10:27] them. And when someone tells you
[10:28] Radiance hit 3,900 tokens per second,
[10:31] the questions we need to ask are which
[10:34] Radiance, under what conditions, and
[10:36] against what baseline? And that is why
[10:39] the numbers we're going to focus on from
[10:40] here are the ones from same card, same
[10:44] model, same conditions tests, because
[10:46] those are what actually tell us what
[10:48] we're getting. And this is where it gets
[10:49] really interesting. It's also where I
[10:51] think a lot of the YouTube coverage has
[10:53] been a bit incomplete. So let's go
[10:55] through Solser's Vienna test, which is
[10:57] the cleanest one I've seen. Solser ran
[10:59] both engines on one R 9700 with the same
[11:02] base model, Quen 3.8 27B at 24.1 GB.
[11:07] Both had speculative decoding switched
[11:09] on, which is the guessing mechanism
[11:11] we'll get to in a minute, and both ran
[11:13] on Auto CM 10 with Radiance version 2.1
[11:16] on one side and Lama CPP build 11561 on
[11:20] the other. When we look at prefill,
[11:22] which is how fast each engine reads the
[11:24] prompt, at 1,000 tokens, Lama CPP does
[11:27] 720 tokens per second, and Radiance does
[11:30] 3,002, which is 4.2 X. At 16,000 tokens,
[11:35] it is 888 versus 2,868,
[11:39] what about 3.2 X? And at 100,000 tokens,
[11:43] it's 691 versus 2,045,
[11:46] which is about 3 X.
[11:48] So the 4 X lives at short prompts and
[11:50] fades slightly as the prompt gets
[11:52] longer, but even at 100,000 tokens,
[11:56] tripling your reading speed is massive.
[11:59] In real time, that 32,000 token prompt
[12:02] that waited 36.5 seconds now waits 11.6
[12:06] seconds. And the 100,000 token prompt
[12:09] that took 2 minutes and 18 seconds now
[12:12] takes 47 seconds, which is really the
[12:15] gap between a workflow that is
[12:16] frustrating and a workflow that is
[12:18] usable.
[12:19] But what happens on the second turn when
[12:21] the same prompt comes back? There's one
[12:23] more test also ran that no video I've
[12:25] seen covers where they sent the same
[12:28] 32,000 token prompt twice. Cold, the
[12:31] first read took 36.7 seconds on Llama
[12:34] CPP and 11.6 seconds on Radiance, the
[12:37] same as before.
[12:39] Then they asked a new question about the
[12:40] same document and Llama CPP answered in
[12:43] 1.05 seconds while Radiance answered in
[12:47] 1.06 seconds, which is an absolute tie.
[12:50] And the reason for that is that both
[12:52] engines have a prefix cache. Once a
[12:54] prompt has been read, the engine stores
[12:56] the work and skips it on the next turn.
[12:59] And if your coding agent sends the same
[13:01] repository context on turn two, which it
[13:03] will because that is how agents work,
[13:06] the engine doesn't re-read all those
[13:08] tokens. It just reads what's new since
[13:10] the last turn. So when we look at where
[13:12] the speed up actually lives, it is in a
[13:14] few specific moments, which are the
[13:16] first time you load a repo into context,
[13:19] the first message of a new agent
[13:20] session, the moment the agent compacts
[13:23] its history and rewrites the summary
[13:25] from scratch, and anytime the prefix
[13:27] cache gets evicted because another
[13:29] request needed the memory.
[13:30] But it does not live on every turn. A
[13:32] fresh 4,000 token turn, which is a new
[13:35] message with a few thousand tokens of
[13:37] new content, took 4.4 seconds on Llama
[13:40] CPP and 1.3 seconds on Radiance, so it
[13:43] saves you about 3 seconds. And that is
[13:45] meaningful over a full day, but it's not
[13:48] 25 seconds. So if you're evaluating this
[13:51] engine, don't just benchmark the cold
[13:53] prompt. Time a full session because the
[13:55] 4X is real. It just lives on specific
[13:58] moments rather than on every single
[14:00] turn.
[14:01] And everything we've looked at so far
[14:02] has been the reading side. So now we
[14:04] need to turn to the other half of the
[14:06] job, which is writing. Now, the writing
[14:09] side is where it gets genuinely clever
[14:12] and it is also more nuanced than most
[14:14] videos explain. Remember that we said
[14:16] decode is memory bound, so the card has
[14:18] to hold the model weights through VRAM
[14:20] to generate each token.
[14:22] Better kernels can change how fast that
[14:24] memory moves, which is why the ceiling
[14:26] for a 4-bit model on this card stays at
[14:28] roughly 45 tokens per second.
[14:31] So how does radiance get significantly
[14:33] faster on writing? It cheats, but in the
[14:35] best possible way. The trick is called
[14:38] speculative decoding. A small drafter
[14:40] model, called B Flash 2 in this setup,
[14:43] proposes the next seven tokens in one
[14:46] shot, and then the big 27B model checks
[14:49] all seven in a single pass through its
[14:51] weights. The math that makes this work
[14:53] is that checking seven tokens costs
[14:55] about the same as writing one because
[14:57] the expensive part is loading the
[14:59] weights, and that load happens once
[15:00] regardless. So if even three or four of
[15:03] those seven tokens are correct, we get
[15:05] them for free, and if all seven are
[15:07] right, we just wrote seven tokens for
[15:08] the price of one. So the real question
[15:10] is how often the small model guesses
[15:12] right, and the answer depends entirely
[15:15] on what we ask it to generate.
[15:17] In Solsus tests, JSON went from 46.6 to
[15:21] 135.7
[15:23] tokens per second, which is 2.9x, and
[15:26] code went from 44.3 to 124.6,
[15:30] which is 2.8x, while math came in at
[15:33] about 2x and translation at about 1.8x,
[15:36] and plain prose went from 33 to 44.6,
[15:39] which is only 1.4x. And the reason is
[15:42] that prose is predictable in a human
[15:44] way, but not in the mechanical way a
[15:46] small model can easily predict.
[15:49] JSON and code have rigid syntax, so when
[15:52] the model needs to close a bracket, the
[15:53] small model knows it needs to close a
[15:55] bracket, and the guesses land more
[15:57] often. So for a coding agent, which is
[16:00] the main use case for this card, we're
[16:02] mostly in the 2.5x to 2.9x range on
[16:06] writing. For essays or creative content,
[16:09] we're closer to 1.4x. And importantly,
[16:12] the guesses don't affect quality. The
[16:14] big model checks every proposed token
[16:16] and only accepts the ones it would have
[16:18] written anyway. LooseBox, which is
[16:21] another engine that also targets this
[16:22] card, ran the same model with and
[16:25] without speculative decoding and found
[16:27] the output byte identical, aside from
[16:29] rare cases where batching changes
[16:31] floating-point rounding. So the speed is
[16:33] real and it's free. You just have to
[16:35] understand where it applies. And the
[16:37] best way to see that is to stop looking
[16:39] at single prompts for a moment and look
[16:41] at a whole day of work instead. And
[16:43] benchmarks are one thing, but real jobs
[16:45] are another. So let's look at what all
[16:47] of this actually adds up to across a
[16:49] full day. A small channel called BizFlow
[16:52] AI does something I genuinely respect,
[16:54] where they run the same 12 business
[16:56] tasks on this card every episode to
[16:58] track how the engine evolves. And these
[17:00] are real things like customer emails,
[17:03] invoice audits, staff scheduling, broken
[17:05] checkout pages and task boards, not
[17:08] synthetic benchmarks. On November 16th,
[17:10] they ran all 12 on Llama CPP, and on
[17:13] November 22nd, they ran all 12 again on
[17:16] Radiance 2.2. Total time went from 125.5
[17:20] minutes to 61.7 minutes. Both runs
[17:23] scored 100 out of 100 on quality after
[17:26] human review, and every single job got
[17:28] faster, ranging from 1.2x on a simple
[17:31] customer email to 2.9x on a policy
[17:34] audit. That is roughly half the time,
[17:36] which is the difference between
[17:37] finishing at 3:00 p.m. and finishing at
[17:39] 5:00 p.m. And that is real. Now, in full
[17:43] transparency, the two setups we were
[17:45] comparing weren't perfectly identical.
[17:48] The model file changed between runs from
[17:50] a 12 GB 3.4 bit copy in the first run to
[17:53] an 18.7 GB 4.8 bit copy in the second.
[17:58] And the larger model is higher quality,
[18:00] which probably explains why the Radiance
[18:02] run generated more output, 306,666
[18:06] tokens versus 258,541
[18:10] or about 19% more. And at 100 tokens per
[18:14] second, those extra tokens eat roughly
[18:16] eight of your 62 minutes. There's also
[18:19] the fact that an agent's actual work,
[18:21] like running test suites, opening files,
[18:24] and clicking through interfaces, doesn't
[18:26] speed up with a faster engine because
[18:28] that time is fixed. So even if the model
[18:31] runs 3x faster, the total job might only
[18:33] be 2x faster because of the overhead
[18:36] around the model work, which means 2x on
[18:38] a full job with better model quality for
[18:41] free is a genuinely good result.
[18:44] It isn't a 4x number, but cutting your
[18:46] AI work in half on a 12-hour workday is
[18:49] not nothing.
[18:50] And once people see a number like that,
[18:52] the very next thing they ask in the
[18:54] comments is whether a second card would
[18:56] double it again. So do we actually need
[18:58] two of these? The level one text guide,
[19:01] which is the most viewed setup tutorial
[19:03] for Radiance, ran 2R 9700s with the
[19:06] 8-bit model and got a single request
[19:09] sustained throughput of 130 tokens per
[19:12] second. On Soldier's single card, short
[19:15] code prompts on Radiance hit 124.6.
[19:18] That means in a single user scenario,
[19:21] the second card buys you almost nothing
[19:23] in speed. What it really buys you is
[19:25] users. On the two card setup, eight
[19:28] concurrent requests added up to 596
[19:31] tokens per second in total, which is
[19:33] about 75 per request. So if you're
[19:36] running four coding agents in parallel
[19:38] or sharing the machine with a small
[19:40] team, the second $2,000 makes sense. But
[19:43] for one person doing their own work, the
[19:45] extra card is mostly just headroom for a
[19:47] bigger context, like a bigger file or a
[19:50] longer conversation history.
[19:52] And it is worth knowing that we don't
[19:54] need an expensive workstation
[19:55] motherboard to run two of these. One
[19:57] owner tested the second card in a PCIe
[20:00] 4.0x4 slot and measured the inter card
[20:04] link at about 5% utilization. The two
[20:06] cards only need to pass small
[20:08] intermediate results between layers, and
[20:11] the model weights never cross the slot.
[20:13] So a regular consumer board with 2x16
[20:15] slots that share lanes works fine.
[20:18] So my honest sizing advice is one card
[20:20] for one person and two cards for a small
[20:23] team. But whichever one we pick, if we
[20:25] set it up today by following the most
[20:27] popular guide, there's a problem waiting
[20:30] because a recent release broke that
[20:32] guide.
[20:33] Now, this one burned some people.
[20:35] The most viewed Radiant setup guide is a
[20:37] level one text forum post from early
[20:40] October. It walks through the two card
[20:42] setup, the specific model files to
[20:44] download in block FP8 and MXFP4 format,
[20:48] and a Docker run command full of flags
[20:50] like TP2. Then on November 14th, Radiant
[20:53] version 2 shipped, and the release notes
[20:56] said the command line flags are gone and
[20:58] the engine now reads a YAML config file
[21:00] instead. But the painful part is that
[21:02] model files in the block FP8 and MXFP4
[21:06] formats are now refused at startup, so
[21:08] the engine won't load them. So if you
[21:10] followed that guide exactly and then
[21:12] updated to version 2 or later, your
[21:14] setup just stopped working. If you're in
[21:16] that situation, there are two options.
[21:18] One is to pin to version 1.17, which the
[21:22] release notes say still supports all the
[21:24] old file formats, and the other is to
[21:26] download the new container formats
[21:28] called IQ8R and IQRV4, which the new
[21:32] engine supports. And according to
[21:34] Radiant's own measurements, the IQRV4
[21:37] format is about 24% closer to the full
[21:40] precision model than Quen's official FP8
[21:42] release at 55% of the size. So the new
[21:45] format is arguably better, but it is
[21:48] still a migration you have to sit down
[21:49] and do. The deeper lesson here is that
[21:52] this project ships a version every day
[21:54] or two, which is incredible momentum and
[21:56] also a real stability risk. So write
[21:58] down the version that works for you,
[22:00] update deliberately rather than
[22:01] automatically, and always check the
[22:04] release notes before you pull a new
[22:05] image.
[22:06] And that pace of change didn't only show
[22:08] up in the release notes because over the
[22:10] same few weeks, it also showed up in
[22:11] what this card costs. So we need to talk
[22:14] about money because the price changed
[22:16] significantly over the past few months.
[22:18] The R9700 launched at $1,299
[22:22] in October of last year, and by late
[22:24] September, price trackers were showing
[22:26] $1,700 to $1,810
[22:29] and then Radiance 1.0 shipped on October
[22:32] 4th with the level one text guide going
[22:34] up two days later. By October 28th, one
[22:37] owner noted the price had moved from
[22:39] $1,699
[22:41] to $1,999.
[22:44] And by November 9th, Newegg's cheapest
[22:46] in stock listing was $2,307,
[22:49] while Micro Center had one for $1,999.99
[22:54] on November 15th. Now, nobody can say
[22:57] the engine caused all of that. The RTX
[22:59] 5090 shortage was happening at the same
[23:01] time and pushing people toward AMD
[23:03] alternatives and memory prices have been
[23:05] climbing too. So there are multiple
[23:07] forces here, but the timing is what it
[23:09] is. If you bought this card at launch
[23:11] for $1,299,
[23:14] the engine essentially doubled your
[23:16] performance for free, which is a
[23:18] genuinely amazing outcome. But if you're
[23:20] buying today at $1,999
[23:23] to $2,300,
[23:26] the math is different. You're paying
[23:28] anywhere from $700 to $1,000 over launch
[23:32] price, which is a 54% to 77% premium.
[23:36] And the speed gains are already baked
[23:38] into what you're paying.
[23:39] It is still dramatically cheaper than
[23:41] the competition. At $2,000, you can buy
[23:44] four of these for the price of one RTX
[23:46] 5090 at current market prices. And the
[23:49] 5090 has three times the memory
[23:51] bandwidth and runs everything on
[23:53] Windows. But if you're on Linux and you
[23:55] want 32 gigs of VRAM at something
[23:57] approaching a sane price, there really
[24:00] isn't another option right now. So the
[24:01] honest framing is that this is a $2,000
[24:04] card at current prices and the speed is
[24:06] already in the price. We shouldn't
[24:08] evaluate it at the $1,299
[24:10] launch price, but at what it costs when
[24:13] you check out. And that leaves the
[24:15] question that actually decides whether
[24:16] you should be checking out at all, which
[24:18] is whether your setup is the one this
[24:20] card is good at.
[24:22] I want to be direct about who this works
[24:23] for and who it doesn't because I've seen
[24:25] too many people buy things based on
[24:27] YouTube benchmarks and end up
[24:28] frustrated. It is a genuinely great
[24:31] option if you're on Linux and
[24:32] comfortable staying there because
[24:34] Radiance is Linux only and the build
[24:36] instructions start with that assumption.
[24:38] And while there are WSL2 patches in the
[24:40] comments section of various threads,
[24:42] none of them come from the main Radiance
[24:44] repository, so I wouldn't stake my
[24:46] workflow on them right now. It's also a
[24:48] great fit if you're running a coding
[24:49] agent that works with large amounts of
[24:51] structured output like JSON, code, and
[24:54] structured data formats. That is where
[24:56] the 2.5x to 2.9x writing speed lives. It
[25:00] is where the prefix cache does the most
[25:02] work and it's the use case this was
[25:05] optimized for. And it works if you're
[25:07] okay managing software that moves fast
[25:09] since 41 versions in 46 days is an
[25:12] incredible development pace.
[25:14] But it is also real operational
[25:16] overhead, so if you need a stable set it
[25:19] and forget it setup, this is not that,
[25:22] at least not yet. Now it is not a great
[25:24] option if you're on Windows and need it
[25:26] to work today. Strata, which is another
[25:29] inference engine, released a Windows
[25:31] package for this card on November 21st
[25:33] and shows about 62 tokens per second.
[25:36] That is the real option that exists on
[25:38] Windows right now. It's also not worth
[25:41] it if you mostly chat and write prose
[25:43] because the 1.4x on prose is real, but
[25:46] it is not worth $2,000 on its own. And
[25:49] if you want to run Quen 3.8 Flash Next,
[25:53] the 125 billion parameter version on a
[25:55] single card, the model experts spill
[25:58] into system RAM. It still works, but
[26:00] you're not getting the full VRAM
[26:01] performance story anymore. And if you
[26:04] own an RX 7900 XTX and we're hoping for
[26:07] the same gains, RDNA 3 kernel support in
[26:10] Radiance only started on October 31st
[26:13] and owners describe it as early. The
[26:15] story just isn't there yet. So when we
[26:17] put all of this together, the 4x is
[26:20] real. It's just not everywhere you'd
[26:21] want it to be. It lives on the cold read
[26:24] of a large prompt and on the moment your
[26:26] session starts or resets or grows beyond
[26:30] what the cache can hold. And even then
[26:32] it fades from 4x at short prompts to
[26:34] about 3x at very long ones. On a full
[26:37] job with real tasks, the same card
[26:39] before and after tests showed about 2x
[26:42] where total time was cut in half,
[26:45] quality held, and all 12 jobs finished
[26:47] faster. And that is the number I use to
[26:49] set your expectations, which is about 2x
[26:52] on real work. Not four and not
[26:54] everywhere, but consistently and
[26:56] measurably two. And two is good because
[26:59] two is the point where your workflow
[27:01] actually works and where you've bought
[27:02] an expensive card and you're finally
[27:04] using what you paid for, which is really
[27:06] the difference between a tool you open
[27:08] reluctantly and one you actually reach
[27:10] for. So if you already own an R 9700 and
[27:13] you're on Linux, install Radiance this
[27:15] week and write down the version number
[27:17] because it is the best free upgrade your
[27:19] money has already bought. And if you're
[27:20] considering buying one, price it at
[27:22] current market rates rather than launch.
[27:24] Expect about two times the speed on
[27:26] whole jobs and make sure you're on Linux
[27:28] or willing to get there. And if you can,
[27:30] time one real task you do every day
[27:33] before and after so you know what you
[27:35] actually gained because the engine got
[27:37] faster on a benchmark number, but your
[27:39] week runs on a stopwatch.
[27:41] If you're running this setup yourself,
[27:43] I'd really like to see what your own
[27:44] before and after looks like. So drop
[27:46] your stopwatch numbers in the comments
[27:48] because I read every one of them.