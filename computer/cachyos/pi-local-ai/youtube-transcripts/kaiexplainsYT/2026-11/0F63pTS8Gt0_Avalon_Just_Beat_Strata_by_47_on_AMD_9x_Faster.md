[00:00] Okay, so comment yes if you've ever done
[00:02] this. You bought an AMD card, maybe a
[00:04] 7900 XT or maybe an RX 7800, and you
[00:08] spent real money on it because the specs
[00:10] looked insane with 20 GB of VRAM and
[00:14] hundreds of GB of bandwidth. And then
[00:16] you went to run a local LLM and watch
[00:18] the tokens crawl out at nine tokens per
[00:20] second while your friend with a 3060 Ti
[00:23] laughed at you over Discord. That was
[00:25] me, and I think it's been a lot of us.
[00:27] And the worst part is that it's not even
[00:28] the card's fault. Because the card is
[00:30] fine, and if anything, the card is
[00:32] actually a beast. The problem has been
[00:34] the software, and by that I mean the
[00:36] ROCm support and the kernel tuning, and
[00:39] really the whole ecosystem lagging
[00:41] behind CUDA in a way that makes you
[00:43] question every life choice that led you
[00:45] to the AMD aisle. So when I saw this
[00:48] headline, a Llama.cpp fork beating
[00:50] Strata, the current fastest AMD
[00:52] optimized inference engine by 47%,
[00:56] I didn't believe it. My first reaction
[00:58] was, okay, what did they cheat? Because
[01:00] we've been here before, and we've all
[01:01] seen the fastest ever benchmarks that
[01:04] turn out to be comparing a Ferrari to a
[01:05] bicycle tied to a tree.
[01:07] But I kept reading, and the more I read,
[01:10] the more complicated the story got,
[01:12] until it turned into kind of a lesson in
[01:14] how to read any benchmark we ever see on
[01:16] the internet. So in this one, we're
[01:18] going deep on Avalon, the Llama.cpp fork
[01:21] that posted 91 tokens per second on a
[01:23] used 500 euros AMD card on a B450
[01:27] motherboard from 2020. And the thing I
[01:29] really want to get to is not just how
[01:31] fast it is, but what the number is
[01:33] actually measuring. The 47% is real, but
[01:37] 47% of what? Now, the story starts on
[01:40] October 22nd, 2026, when a developer on
[01:44] GitHub who goes by Frieren Duck posts
[01:46] one single table in their readme. In the
[01:49] left column is Strata version 0.1.43
[01:54] running Qwen 38B flash next on a Radeon
[01:57] RX 7900 XT at 61.9 tokens per second.
[02:02] And in the right column is Avalon on the
[02:04] same card with the same model at 91
[02:06] tokens per second. And that was the
[02:08] whole post with no blog and no YouTube
[02:11] video, just a table in a read me that
[02:13] then proceeded to absolutely blow up
[02:15] across every AI forum and subreddit I
[02:18] lurk in.
[02:19] That 91 tokens per second on a 7900 XT
[02:23] for a model this size is legitimately a
[02:26] headline number. When I first saw it, I
[02:28] felt the same thing I feel when I see a
[02:29] sale on SSDs. That kind of dangerous
[02:32] excitement where your brain is already
[02:34] justifying a purchase your wallet hasn't
[02:36] agreed to yet.
[02:37] But at this point, I start to pump the
[02:39] brakes because the story gets
[02:40] interesting here rather than just
[02:42] exciting. To understand why this
[02:43] benchmark felt so emotionally satisfying
[02:46] to the AMD community, we have to go back
[02:48] about 2 weeks earlier to October 6th.
[02:51] That's when Strata, the specialist
[02:53] inference engine built specifically for
[02:55] mixture of experts models with a heavy
[02:56] focus on AMD hardware, published their
[02:59] own benchmark. They ran the same coin
[03:01] model on a 12 GB RTX 3060 comparing
[03:04] Strata against a tuned version of stock
[03:07] llama.cpp and Strata wrote 41.6 tokens
[03:10] per second while the tuned llama.cpp
[03:12] wrote 9.1. That is four and a half times
[03:15] slower on the same card. And the
[03:17] benchmark was almost embarrassing for
[03:19] the llama.cpp side of things because it
[03:22] made Strata look like the obvious choice
[03:24] if you wanted serious local inference on
[03:26] this kind of model.
[03:28] So 2 weeks later, a fork of that same
[03:30] general purpose engine, the same
[03:32] llama.cpp that got destroyed, comes back
[03:35] and posts a 47% win. Of course, it feels
[03:38] like a revenge story where the narrative
[03:41] writes itself and the underdog comes
[03:42] back as the little engine that could.
[03:44] And the methodology here is actually
[03:46] solid. Both engines ran on the same
[03:48] night on the same physical machine using
[03:51] greedy decoding with 512 tokens per
[03:54] answer and the median of three runs.
[03:57] Strata had its own speculative drafting
[03:59] turned on, so it wasn't running in some
[04:01] crippled mode, which means this was not
[04:03] a drive-by screenshot, and the protocol
[04:06] was careful. But, I want you to hold on
[04:08] to one detail because we're going to
[04:10] come back to it. The comparison is two
[04:12] engines, and also two different model
[04:14] files, and that detail is going to
[04:17] matter a lot. Now, before we get into
[04:19] the numbers, I need to actually explain
[04:22] what Avalon is because the framing of
[04:24] llama.cpp fork beats strata is
[04:27] technically accurate and kind of
[04:29] misleading at the same time. Avalon is
[04:31] not really llama.cpp, or rather it
[04:34] started as llama.cpp from early October
[04:37] and then got a lot added on top of it.
[04:39] Its repository went live on October 9th
[04:41] under an MIT license, and it started
[04:43] life as a branch of another fork called
[04:46] boon llama.cpp, which contributed the
[04:48] first version of its expert cache. The
[04:51] compression types it uses came from
[04:53] ikllama.cpp, and the readme even credits
[04:55] strata itself for two ideas, the expert
[04:58] ranking file and the cache reloading
[05:00] mechanism. So, strata borrowed ideas
[05:02] from llama.cpp, and then Avalon, a
[05:05] llama.cpp fork, borrows ideas back from
[05:07] strata, which means there are no clean
[05:10] underdogs in this story. It's a remix
[05:12] all the way down, and I actually think
[05:13] that's kind of beautiful because that's
[05:15] just how open source works.
[05:17] But, the part that stopped me cold was
[05:19] further down. The readme explains that
[05:21] Avalon's architecture was shaped by 30
[05:24] years of its author's optimization work,
[05:26] which is impressive on its own.
[05:28] And then it says that every
[05:29] micro-optimization, the GPU and CPU
[05:32] kernels and all the rest of it, was
[05:34] written by Claude Opus 5.5 with the
[05:37] author steering.
[05:38] The readme literally says, "I am only
[05:41] the driver. The AI is the engine." And I
[05:44] just want to sit with that for a second
[05:46] because we are in a moment now where the
[05:48] AI that is helping us run AI locally is
[05:50] itself an AI.
[05:52] That is not a criticism since the
[05:54] results speak for themselves, but it is
[05:56] one of those facts that makes you stop
[05:58] and stare at your ceiling for a while.
[06:00] Now, the other thing about Avalon we
[06:01] need to understand before going in
[06:03] further is that it does exactly one
[06:05] thing. It's tuned entirely for
[06:08] quantriate B flash next, and the model
[06:10] files it runs use custom data types and
[06:13] a layout that stock llama.cpp can't even
[06:15] load. And every other model you try to
[06:17] run on it behaves exactly like plain
[06:19] llama.cpp would, so there is no magic
[06:22] for anything else. This matters
[06:24] enormously, and we'll get to why.
[06:26] If we want to understand the benchmark,
[06:28] we have to copy the machine. So, let's
[06:30] go through what this system actually is,
[06:32] spec by spec.
[06:34] The graphics card is a Radeon RX 7900
[06:37] XT,
[06:39] and not the XTX, but the XT, which is
[06:42] the 20 GB version that launched in late
[06:44] 2022 at $899 with 800 GB per second of
[06:49] memory bandwidth. The author picked
[06:51] theirs up second hand for 500 euros, and
[06:54] used prices in Europe were sitting
[06:55] around 590 euros at the time of the
[06:57] test. The CPU is a Ryzen 7 3800 XT with
[07:02] eight Zen two cores from 2020. One quick
[07:05] note here, because the readme and at
[07:07] least one video about it call it a 2019
[07:09] chip, and that's technically a family
[07:11] thing, since the broader Ryzen 3000 line
[07:14] is from 2019, but this specific model,
[07:17] the 3800 XT, came out in July 2020.
[07:21] It's a small detail, but I appreciate
[07:23] accuracy in these things. It sits on a
[07:25] B450 motherboard. While the processor is
[07:28] technically capable of PCIe 4, the board
[07:31] is not, so the graphics card runs at
[07:33] PCIe 3 speeds, which is about 14 GB per
[07:36] second in practice. And then there's the
[07:38] RAM, which is 64 GB of DDR4 3200 in two
[07:43] channels. On paper, that is 51.2 GB per
[07:46] second of bandwidth, but the author
[07:48] measured real-world throughput at 33 to
[07:51] 35 GB per second. So, this is not a
[07:53] flagship system or a workstation, but a
[07:56] desktop from 2020 with a used GPU and a
[07:59] mid-range motherboard, and the headline
[08:01] numbers come from exactly this box. The
[08:04] reason I'm being so specific about it is
[08:06] that every number and every trick that
[08:08] follows is anchored to these
[08:10] constraints. The innovations in Avalon
[08:12] are innovations for this machine. So,
[08:14] when we change the machine, the story
[08:16] starts to change, too. Now, let's talk
[08:18] about the model because Qwen 38B Flash
[08:21] Next is not what it sounds like. The 8B
[08:24] in the name is really misleading, and
[08:27] understanding the real size is the key
[08:29] to understanding why the speed tricks
[08:31] work at all. This is a mixture of
[08:33] experts architecture with 125 billion
[08:36] parameters, which is the active model
[08:38] size.
[08:40] But, sitting alongside those is a 51
[08:42] billion parameter lookup table that
[08:44] lives outside the graphics card
[08:46] entirely. So, if you download both of
[08:48] them together, you're looking at what
[08:50] the author called a 177
[08:53] billion parameter model in their own
[08:55] Reddit post. And the Avalon file on disk
[08:58] is about 89 GB. Now, when we look at how
[09:01] the routing works at inference time,
[09:03] there are 48 layers in this model, and
[09:05] each layer holds 512 experts, which is
[09:09] 24,576
[09:11] experts in total. For every single token
[09:14] you generate, a router inside the model
[09:16] picks 10 experts per layer. So, 480
[09:20] experts do the actual work on each
[09:22] token. And if we do some rough math, at
[09:24] the roughly 3.4 bits per parameter that
[09:27] Avalon stores its experts at, every
[09:29] single token touches about 1 GB of
[09:32] expert weights. And all of that needs to
[09:35] be read from somewhere, on every token,
[09:37] every time. The graphics card can do
[09:39] trillions of floating-point operations
[09:41] per second, so it isn't a bottleneck.
[09:44] The bottleneck is essentially reading
[09:46] that gigabyte of expert weights fast
[09:48] enough to keep up with the compute. And
[09:50] when we follow that 1 GB of experts
[09:53] through this system, we start to
[09:54] understand why the DDR4 spec matters so
[09:57] much. So, if every expert lived in
[09:59] system RAM being fed at 34 GB per
[10:02] second, the read time alone would be
[10:04] about 29 ms per token, which is a hard
[10:07] ceiling of roughly 34 tokens per second
[10:10] before the GPU does a single thing.
[10:13] And if the experts instead had to cross
[10:14] the PCIe 3 slot, 1 GB at 14 GB/s is
[10:19] about 71 ms per token. That drops the
[10:22] ceiling to roughly 14 tokens per second
[10:25] on a fast card that is just sitting
[10:26] there waiting.
[10:27] Now, Avalon writes 62.4 tokens per
[10:31] second without any speculative drafting,
[10:33] which works out to about 16 ms per
[10:35] token. And in 16 ms at 34 GB/s of RAM
[10:40] throughput, we can supply about half a
[10:42] gigabyte. So, roughly half of every
[10:44] token's experts, or more, have to come
[10:47] from the VRAM on the card itself,
[10:49] because there is no way to feed this
[10:50] model fast enough from RAM alone.
[10:53] But the card can't hold all the experts,
[10:54] either, since there are about 47 GB of
[10:57] them, and the 7900 XT has 20. And even
[11:00] after the model's other weights take
[11:02] their share, we can keep somewhere
[11:04] between 9 and 14 GB of experts on the
[11:07] card, which is somewhere between a fifth
[11:09] and percent of the total. And the reason
[11:11] this works at all is that experts are
[11:13] not used evenly. A relatively small set
[11:16] of them handles a disproportionate share
[11:17] of all the lookups across all kinds of
[11:19] text. So, if we keep the right ones
[11:21] cached on the card, most lookups never
[11:23] have to touch RAM. So, that is the
[11:25] expert cache, and the percentage of
[11:27] lookups it serves from the card is
[11:29] called the hit rate. Your DDR4 bandwidth
[11:32] sets the floor, and the expert cache
[11:34] decides how high you can climb off that
[11:36] floor. Now, the first thing Avalon does
[11:38] differently is extremely simple in
[11:40] principle and really clever in
[11:42] execution, because it treats every byte
[11:45] of VRAM that isn't actively being used
[11:47] for compute as cache space for experts.
[11:50] Compute buffers get lent to the cache
[11:52] between phases, so they come back when a
[11:54] pipeline step needs them and hold
[11:56] experts in between. The portion of the
[11:58] KV cache your conversation hasn't grown
[12:00] into yet holds experts, too.
[12:02] And for the safety memory reserve,
[12:04] rather than guessing at a fixed number,
[12:06] Avalon calculates it precisely at 400 MB
[12:10] and caches experts in the rest. On top
[12:12] of that, the work gets split where the
[12:15] graphics card computes the experts it
[12:16] currently holds while the eight CPU
[12:18] cores handle the cache misses coming
[12:20] from RAM in parallel.
[12:22] And when the math says it's faster to
[12:24] move a missed expert onto the card than
[12:26] to compute it on the CPU, the engine
[12:28] makes that call dynamically. And that
[12:30] alone accounts for the first part of the
[12:32] speed improvement. In a direct
[12:34] comparison without speculative drafting,
[12:36] Strat wrote 49 tokens per second on this
[12:39] specific machine and Avalon wrote 62.4,
[12:43] which is a 27% improvement. And it comes
[12:46] entirely from keeping the GPU, the CPU
[12:49] cores, and the PCIe slot busy at the
[12:51] same time rather than having them wait
[12:53] on each other. It works out to about 4
[12:55] milliseconds saved on every single token
[12:57] and that adds up fast. So, the cache
[12:59] gets us from 49 to 62.4, but the
[13:02] headline number is 91. Where do the
[13:05] other 28 tokens per second come from?
[13:07] The answer is speculative drafting,
[13:09] which on a mixture of experts model is
[13:11] much harder to do efficiently than on a
[13:13] standard dense model. The concept is
[13:15] that a small draft head guesses the next
[13:18] couple of tokens before the main model
[13:19] confirms them and then we check all the
[13:22] guesses in one pass. So, if the guesses
[13:24] were right, we got multiple tokens for
[13:26] roughly the cost of one, which makes it
[13:29] a bit like auto complete for inference.
[13:31] On a dense transformer, this is fairly
[13:33] clean because when we check three
[13:35] guessed tokens, each weight gets read
[13:37] once and reused across all three checks.
[13:40] So, the verification costs only slightly
[13:42] more than writing a single token.
[13:44] But on a mixture of experts, this falls
[13:46] apart. Every guessed token picks its own
[13:49] 10 experts per layer independently. So,
[13:51] checking three guesses might touch up to
[13:53] three times as many distinct experts as
[13:56] a single token would and the memory bill
[13:58] explodes.
[14:00] Avalon's draft head agreed with the main
[14:02] model on 80.7% of positions on a fixed
[14:05] test. And with two guesses per pass, the
[14:08] theoretical maximum if the guesses were
[14:10] independent is about 2.46 tokens per
[14:13] pass. But the measured gain is 1.46
[14:17] times, so each verification pass costs
[14:20] roughly the equivalent of 1.7 normal
[14:23] token generation steps, and that is the
[14:25] MoE tax. Now, the key thing Avalon does
[14:29] about this is make the draft head cheap.
[14:31] The head is about 1.5 GB,
[14:34] while Strata's separate draft head took
[14:36] 3.4 GB on a 12 GB card, and actually
[14:39] pushed so many experts back to the CPU
[14:42] that it dragged decoding speed down in
[14:44] Strata's own earlier benchmarks. And
[14:46] Avalon's head cuts the vocabulary to the
[14:49] 65,000 most common tokens, and shares
[14:52] the main model's expert cache instead of
[14:54] competing with it for VRAM. So the
[14:56] guesser lives inside the cache budget
[14:59] rather than at the expense of it. So
[15:01] when we do the math, 1.27 times from the
[15:04] cache and the parallel compute,
[15:06] multiplied by 1.15 times from the more
[15:09] efficient drafting, lands at 1.47,
[15:12] and that is the whole 47%. Now, there is
[15:16] one thing I want to address head on,
[15:18] because it's the first thing a skeptical
[15:20] person should think. Is Avalon just
[15:22] faster because it uses a worse model
[15:24] file? And did they compress more
[15:26] aggressively and just call it a win?
[15:28] The answer is no, and it's actually
[15:30] pretty surprising. Avalon's main file is
[15:32] about 88 GB,
[15:34] and the Esta file that Strata serves,
[15:36] which is the quantization format Strata
[15:38] uses, is about 78 GB.
[15:41] So Avalon is reading 13% more bytes per
[15:44] token, and still runs faster. For
[15:47] quality, the author ran perplexity
[15:49] tests, where a lower score means better
[15:52] model quality. In English, Avalon's file
[15:55] scored 1.443 against Strata's 1.469,
[15:59] and in code generation it was 1.331
[16:02] against 1.338.
[16:04] And for reference, Unsloth's popular IQ4
[16:08] quantization sits at 1.401 in English,
[16:11] and Avalon's file beats that, too. So
[16:14] this is not fast slop, but a better
[16:16] quality file running faster on the
[16:18] target hardware. The caveat here is that
[16:20] perplexity is not the same as task
[16:22] performance, since it measures how well
[16:25] the model predicts text and not how well
[16:27] it answers your actual questions. And no
[16:29] downstream benchmark results for
[16:31] Avalon's file have been published yet,
[16:33] so there is still an asterisk there.
[16:35] And the other admission is the one I
[16:36] asked you to hold on to, which is that
[16:38] the head-to-head comparison is two
[16:40] engines and two files. So, the 27% base
[16:43] speed gain is still partly file versus
[16:46] file and not just engine and we can't
[16:49] fully isolate the two. Now, this next
[16:51] part is the one most coverage completely
[16:53] glosses over, so I want to be thorough
[16:55] with it. When we look at the version
[16:57] number on the Strata row in Avalon's
[16:59] table, it says 0.1.43,
[17:02] which was released October 11th. And
[17:05] Avalon's table went into the readme late
[17:07] on October 22nd, when Strata was already
[17:09] on version 0.2.2.
[17:12] Today it's at 0.2.8,
[17:14] which is the 14th release since the one
[17:17] in the table, so 14 releases in 18 days.
[17:20] And 14 releases sounds like it should
[17:21] erase any gap, since if they're shipping
[17:23] that fast, surely they've caught up. But
[17:26] it's worth reading the actual change log
[17:28] entries for those releases, specifically
[17:30] for AMD. Strata 0.2.7
[17:33] improved Qwen performance on a Radeon AI
[17:35] Pro R9 700, where decoding went from
[17:39] 82.9 to 94.6 tokens per second at 8,000
[17:43] tokens of context. And Strata 0.2.8
[17:46] took the same R9 700 from 73.7 to 79.7
[17:51] on a story prompt. But an R9 700 is an
[17:54] RDNA 4 card and a 7900 XT is RDNA 3 and
[17:59] those are different GPU generations, so
[18:01] the AMD improvements that Strata shipped
[18:03] in the two weeks after the benchmark
[18:05] landed on a different family of
[18:06] hardware.
[18:07] And this isn't accidental. The Strata
[18:10] release notes for 0.2, published October
[18:12] 19th, say explicitly that while the RX
[18:15] 7000 packages were built and scanned,
[18:18] quote, "The maintainers have not run
[18:20] them on an RX 7000 or a Strix Halo
[18:23] card." Now, Strata's own support table
[18:25] still lists the 7900 XT and XTX as
[18:29] maintainer tested, but the release notes
[18:31] are more specific about where the actual
[18:33] optimization work is happening. The
[18:35] maintainers are running R9 700s with 32
[18:39] GB of VRAM and 125 GB of system RAM. And
[18:43] that is a fundamentally different
[18:45] machine for this workload. And on that
[18:47] home card, by the way, Strata posts 94.6
[18:51] tokens per second, which is above
[18:53] Avalon's 91. So, each engine looks best
[18:56] on the desk it was built at. Now, a fair
[18:58] question is whether the 61.9 in the
[19:00] benchmark is actually representative of
[19:02] Strata on the 7900 XT. Maybe the Avalon
[19:06] author didn't configure Strata properly
[19:08] and handed it a handicap. The community
[19:10] benchmarks answer this pretty
[19:12] definitively. Strata maintains a table
[19:14] of user reported results, where one 7900
[19:17] XTX owner on the bigger card got 62.0
[19:21] and 62.3 tokens per second. And a 7900
[19:25] GRE owner got 59.1 on a slightly smaller
[19:28] file, while four 7900 XT owners together
[19:32] reported 59 to 60 tokens per second on
[19:35] the standard IQ 3 file. So, across
[19:37] different cards and different
[19:38] configurations, it lands in the same
[19:40] ballpark, where roughly 60 tokens per
[19:43] second is just where RDNA 3 owners land
[19:46] with Strata right now, and the 61.9 in
[19:48] the table is honest. And if you own a
[19:50] 7900 XT or an XTX and you're on Linux,
[19:54] Avalon's 91 tokens per second is a real
[19:57] improvement over what you're currently
[19:59] getting.
[20:00] That's the strongest form of the
[20:01] argument for trying it, and I want to
[20:03] give it to you as clearly as I can. But
[20:05] this is where the story gets more
[20:06] complicated, and what I think honest
[20:08] coverage needs to go. Because when we
[20:10] move Avalon off the 7900 XT, the lead
[20:14] starts to shrink, and in some cases
[20:16] dramatically. The author rented an RTX
[20:18] 4090 for one run on October 26th, and
[20:21] got 120.5
[20:23] tokens per second on a short prompt. And
[20:25] that sounds impressive, but the author's
[20:27] own words on Reddit were "The same speed
[20:30] as Strata for now." And a few days
[20:32] later, they called it a very little
[20:34] advance with the GPU kernel still tuned
[20:36] for RDNA 3. Then one user tested Avalon
[20:39] on Radeon Pro W7800s,
[20:42] which are the 48 GB professional version
[20:45] of the same RDNA 3 chip family, with
[20:47] more memory and 864 GB per second of
[20:50] bandwidth.
[20:51] And one W7800 got 58 tokens per second
[20:55] without drafting, and 87 with it, which
[20:58] is below the 7900XT's 62.4 and 91. Two
[21:02] W7800s,
[21:04] with all the experts fitting comfortably
[21:06] in VRAM, got 46 and 70, which is about
[21:09] 20% slower than one card. And with two
[21:11] W7800s,
[21:13] all 47 GB of experts fit in VRAM, so the
[21:17] RAM bandwidth floor is completely gone.
[21:19] It still got slower. The user's own
[21:21] analysis is that it became compute
[21:23] limited, because once the experts are
[21:25] all on the card, the bottleneck shifts
[21:28] from memory bandwidth to raw compute
[21:30] throughput, and the W7800 has 70 compute
[21:34] units against the 7900XT's
[21:36] 84. So once we solve the memory problem,
[21:39] we expose the compute problem, and the
[21:41] optimization that works on the 7900XT is
[21:44] specific to the 7900XT's
[21:47] particular balance of bandwidth and
[21:49] compute.
[21:50] Now, Avalon's readme claims you can run
[21:53] on 32 GB of RAM, and on paper, this
[21:55] makes no sense. The file is 89 GB, and
[21:59] the card is 20, so you'd have 48 in
[22:01] total, and still be 41 GB short of
[22:03] fitting everything. It works through
[22:05] memory mapping, where the OS maps the
[22:07] file into virtual memory, and whatever
[22:09] doesn't fit in physical RAM gets read
[22:11] back from the SSD when needed. When
[22:13] you're just writing tokens, the overhead
[22:15] is minimal. Capping RAM to 28 GB, which
[22:18] is what a 32 GB machine leaves
[22:20] available, dropped the best-case speed
[22:22] from 91.2 to 89 tokens per second, so
[22:26] about 2% slower, which is fine. But,
[22:28] when you feed it a new prompt, like a
[22:30] fresh document or an agent turn with
[22:32] 19,000 tokens of context, you pay for
[22:35] every cash miss. And a 19,000 token
[22:38] prompt went from processing in about 15
[22:40] seconds to about 21 seconds, which is a
[22:43] 40% slowdown on prompt ingestion. So, on
[22:46] 32 GB, you pay a real tax every time you
[22:49] start a new task. And the readme doesn't
[22:52] mention which SSD was being tested,
[22:54] which matters a lot, since an NVMe at 7
[22:57] GB per second is a very different beast
[22:59] from a SATA SSD at 500 MB per second.
[23:04] Now, let me be direct, because I think
[23:05] the useful information in this whole
[23:07] story lives right here. If you have a
[23:09] Radeon 7900 XT or 7900 XTX, you're
[23:13] running Linux, you have at least 32 GB
[23:16] of RAM, and ideally 64, and you
[23:18] specifically want to run Qwen 3 8B Flash
[23:21] Next fast, then Avalon is the answer
[23:24] right now. With a one-command install
[23:26] and about 98 GB of disk. So, try it. If
[23:29] you're on an Nvidia card, the author's
[23:31] own assessment is that it's currently
[23:33] running at about the same speed as
[23:34] Strata, because the kernels aren't tuned
[23:36] for CUDA yet. So, try Strata.
[23:39] And if you have an RDNA 4 card, an R9
[23:41] 700 or newer, Strata is being actively
[23:44] benchmarked and improved on that
[23:45] hardware almost every release. And it's
[23:48] already running above Avalon's numbers
[23:50] on those cards. If you're on Windows,
[23:52] Avalon simply doesn't run there yet,
[23:54] since there is no Vulcan back end, and
[23:56] the installer actively checks for an
[23:58] RDNA 3 card. And if you want multiple
[24:00] users, a desktop app, image support, or
[24:04] any model other than Qwen 3 8B Flash
[24:07] Next, Strata is the more complete
[24:09] project today. This is also a
[24:11] one-developer project, and the first
[24:13] person to try running it with two cards
[24:15] found it hanging, and then found that
[24:17] Avalon was counting the experts' file
[24:19] size three times, calculating about 150
[24:22] GB instead of the correct 53. Both
[24:25] issues were found and fixed within days,
[24:28] which is impressively fast. But, it's
[24:30] also the kind of bug that happens when
[24:32] one person is moving fast, and a
[24:34] reminder that this is early stage
[24:36] software. And the part of this story I
[24:38] find really fascinating from a software
[24:40] perspective is that Avalon is not a pull
[24:42] request or a proposal, but a fork that
[24:45] went off and did the thing while the
[24:47] main project figured out what it wanted
[24:49] to be. There is currently a pull request
[24:52] from developer Piotr Wilken to beat
[24:54] Strata inside llama.cpp itself, not in a
[24:57] fork, but in the actual main project.
[24:59] It's still a draft, and it's asking the
[25:02] maintainers a real question about how
[25:03] much specialized code they're willing to
[25:05] accept to be competitive with specialist
[25:07] engines. And Avalon is one answer to
[25:10] that question, which is to not wait for
[25:12] consensus, but to fork it and tune it
[25:15] for one box and ship it, and the answer
[25:17] you get is 47% faster on that box and
[25:20] not much on any other. There is also a
[25:22] second pull request, still open, for
[25:24] running mistral experts on the CPU in
[25:26] parallel, which is similar in spirit to
[25:29] what Avalon does. And until those land,
[25:31] the stock llama.cpp you might be running
[25:34] is not the thing that beats Strata. So,
[25:36] beyond the specific numbers, what I want
[25:38] you to take away is that every speed
[25:40] table you see is a photo of one machine,
[25:43] and I think that is the single most
[25:45] important sentence in this whole video.
[25:47] When we see a benchmark, there are four
[25:49] questions to ask. What exact version of
[25:52] each engine was run? Were the model
[25:54] files the same files or different ones?
[25:57] What was the hardware, specifically,
[25:59] including the motherboard and RAM? And
[26:01] then the one people forget, which is who
[26:03] owns that hardware. The 47% in that
[26:06] table is real, and it isn't fabricated,
[26:08] and the protocol was honest.
[26:10] But, what it measures is the distance
[26:12] between Avalon's desk and Strata's desk,
[26:15] not a universal truth about two engines.
[26:17] So, on the 7900 XT, Avalon is the
[26:20] fastest thing running right now, while
[26:23] on the R9 700, Strata is faster and
[26:25] getting better every week, and on
[26:27] Nvidia, it's basically a tie for the
[26:29] moment.
[26:30] And the interesting thing about Avalon
[26:31] to me is not actually the number, but
[26:33] the philosophy. The author decided that
[26:36] if the general purpose engine wasn't
[26:37] going to be tuned for that exact box,
[26:40] they would do it themselves. Borrowing
[26:42] from every project that had figured out
[26:43] a piece of the puzzle and feeding the
[26:45] kernels to an AI co-author and shipping
[26:47] it. And they got 91 tokens per second
[26:50] out of a 500 euros card on a B450 board,
[26:54] which is a really impressive thing. The
[26:56] author says they're reaching 100 tokens
[26:58] per second now. And Strata has shipped
[27:00] 14 releases since the benchmark table
[27:02] went up, so both of them are still
[27:04] moving. So, run the engine whose author
[27:06] owns your card, and the next time you
[27:08] see a 47% headline, you'll know exactly
[27:11] which four questions to ask. If you made
[27:13] it this far, thank you, because this one
[27:15] went deep. And if you're an RDNA 3 owner
[27:17] who tried Avalon, let me know in the
[27:19] comments what numbers you're seeing,
[27:21] since I'm curious whether the community
[27:23] is landing at 91 or somewhere different
[27:25] in practice. And drop a like if this
[27:27] helped you understand what is actually
[27:29] going on with these benchmarks, because
[27:31] there are going to be a hundred more of
[27:33] them, and being able to read them
[27:34] clearly is worth more than any single
[27:37] number. I'll see you in the next