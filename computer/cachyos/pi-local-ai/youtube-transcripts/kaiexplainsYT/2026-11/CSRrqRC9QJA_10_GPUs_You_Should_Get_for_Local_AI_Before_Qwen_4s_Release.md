[00:00] If you've spent the last few weeks going
[00:01] down the same rabbit hole I did, you've
[00:04] probably opened Reddit and YouTube and
[00:06] seen someone say, "The RTX3090 does 63
[00:09] tokens a second on Quinn 4." And you
[00:11] thought, "Finally, someone has done the
[00:14] math, so I can just buy the card and
[00:15] move on with my life." And then you buy
[00:17] it, or you're about to, and something
[00:19] feels off, which is exactly what
[00:22] happened to me when I sat in front of my
[00:23] own rig and could not work out why my
[00:25] numbers looked nothing like what I had
[00:27] seen on YouTube. Because the thing
[00:29] nobody says out loud in these GPU
[00:31] recommendation videos is that the speeds
[00:33] they quote all come from the same GitHub
[00:36] table. That is the 63 tokens a second on
[00:39] the 3090, the 76 on 2560 Ti, and the 155
[00:44] on the 5090. And that table has two
[00:47] columns. And every list you've been
[00:49] reading, including some of my own
[00:51] earlier thinking on this, has been
[00:53] reading from the wrong one. It's the
[00:54] right hand column, the fast one. and it
[00:57] needs a trick that as of today, November
[00:59] 25th, 2026, has been sitting in an
[01:02] unmmerged pull request for 90 days. Now,
[01:06] that is not even the strangest part
[01:08] because all of these numbers were
[01:10] measured on Quinn 3.827b
[01:13] and not on Quinn 4. And as of this
[01:15] morning, Quinn 4's small open- source
[01:17] models still have no weights, no
[01:19] confirmed size, and no release date. So,
[01:22] what happens when Quinn 4 actually drops
[01:25] and the trick does not work yet? We're
[01:27] left staring at the left column, which
[01:29] is the real boring honest number, and
[01:32] wondering why a 5090 writes slower than
[01:35] a 3090. And that is what this video is
[01:38] really about. I went through all of this
[01:40] confusion myself. I read everything and
[01:43] I watched the GitHub pull requests sit
[01:45] there collecting dust. So, what I want
[01:48] to do is go card by card with honest
[01:50] numbers only so that when Quen 4 lands,
[01:53] your GPU earns its price on day one
[01:56] instead of leaving you waiting for a
[01:57] pull request to merge. But before we
[02:00] touch a single GPU, we need to agree on
[02:02] what we're actually measuring because
[02:04] without that context, the rest of this
[02:06] list is just numbers. When we look at a
[02:08] model like Quinn 3.827B A27B running
[02:11] locally, which is what we are
[02:12] benchmarking everything against because
[02:14] Quen 4 small models are not out yet.
[02:16] There are two speeds that matter to us
[02:18] as users. The first one is decode speed,
[02:21] which is how fast the GPU writes tokens,
[02:24] the words you actually see appearing on
[02:26] your screen, and it is the number
[02:28] everyone obsesses over and the one all
[02:30] those tokens per second benchmarks are
[02:32] measuring. The second one is prefill
[02:34] speed, also called prompt processing,
[02:37] which is how fast the GPU reads your
[02:39] prompt before it starts writing
[02:41] anything. And if you use an AI coding
[02:43] assistant and paste files, context, or
[02:45] whole code bases into the prompt, this
[02:48] number matters enormously because it is
[02:50] the time we spend staring at a loading
[02:52] spinner before the model says a single
[02:54] word. Now decode speed on a GPU is
[02:57] limited by one thing and that is memory
[03:00] bandwidth or how fast the GPU can move
[03:02] data from VRAMm into the compute cores.
[03:04] When we look at the 3090, it has 936 GB
[03:08] per second and at 4bit quantization Quen
[03:12] 3.827B
[03:13] is a 16.56 GB file. So if we divide one
[03:17] by the other, the theoretical ceiling is
[03:20] about 57 tokens per second and vanilla
[03:23] llama CPP gets 41 of them, which is
[03:25] about 73% of the ceiling and really good
[03:28] for a plane implementation. So if 57 is
[03:31] the ceiling, how does anyone get 63 out
[03:33] of that same card? The answer is the
[03:35] trick sitting in that right hand column.
[03:38] Quinn 3.8 ships with something called a
[03:40] multi-token prediction head. It's a
[03:42] small extra piece of the model that
[03:44] cheaply guesses the next two or three
[03:46] tokens so that the big model can check
[03:48] all of them in one pass through the
[03:50] weights. And because one pass now
[03:52] produces several tokens, a 3090 jumps
[03:54] from 41 tokens per second to 63, which
[03:58] is above its own theoretical ceiling,
[04:00] that one giant read just gets spread
[04:02] across more than one token. So it's
[04:04] essentially speculative decoding baked
[04:06] into the model itself. And it's a
[04:08] brilliant trick that works on Quinn
[04:10] 3.827b 827B. Right now, if you run Quinn
[04:13] 3.8 today, the fast column is your real
[04:16] speed. And I'm not here to tell you
[04:17] those numbers are fake. The problem only
[04:19] shows up when the model changes, which
[04:21] is exactly what Quinn 4 is about to do.
[04:24] Alibaba previewed Quen 4's architecture
[04:26] on August 24th with something called
[04:28] Quinn 3.8 Flash Next, and Llama CPP
[04:31] added basic support 3 days later. The
[04:34] MTP head for the new architecture went
[04:36] up as a draft pull request that same
[04:38] night. It is still a draft with its last
[04:41] update on October 2nd and a second
[04:43] attempt was closed without merging on
[04:45] October 1st. So why is it stuck? The new
[04:48] architecture runs several parallel
[04:50] residual streams, four of them according
[04:52] to Intel's kernel code that was briefly
[04:54] public in October. And the prediction
[04:56] head has to run separately for each
[04:58] stream. If you try to average the
[05:00] streams and then draft, then in the
[05:02] words of the PR author, the acceptance
[05:05] rate drops catastrophically. And that is
[05:07] the technical wall that has kept us
[05:09] unmerged for 90 days in counting. Now
[05:12] big serving frameworks like VLM have
[05:15] already sorted out MTP for flash next on
[05:17] Nvidia cards. So the story is not that
[05:19] the trick is dead. It's that the trick
[05:22] works on some paths and not on others on
[05:24] day one. And that is why we're ranking
[05:26] on the left column. It's the number
[05:28] you'll see when you first plug in your
[05:30] card and try to run Quen 4 before any
[05:32] pull requests land. If that pull request
[05:35] merges tomorrow, every card on this list
[05:37] gets a free speed upgrade, which would
[05:39] be great. But we buy for the worst case
[05:41] and celebrate the best case because that
[05:43] is how we avoid buyer remorse. So, with
[05:46] that rule in place, we can finally talk
[05:48] GPUs. And I want to start with the one
[05:50] you've probably already considered,
[05:52] which is the RTX3090.
[05:54] It has 24 GB of GDDR6X,
[05:57] 936 GB per second of bandwidth, and a
[06:00] 350 W power draw. It launched in 2020 at
[06:04] $1,499,
[06:06] which feels like ancient history now.
[06:09] And today, the three cheapest listings
[06:10] average $1,445,
[06:13] up 10% from its August through October
[06:16] average. And I'll be honest, the cheap
[06:18] ones go fast because the median eBay
[06:21] asking price hit nearly $2,000 on
[06:23] November 11th and sold prices climbed
[06:26] from $1,23
[06:28] to $1,415
[06:31] in just 2 weeks. On a current Llama CPP
[06:35] build, the left column decode is $41.3
[06:38] tokens per second. And the repo notes
[06:41] point out something really interesting
[06:42] here, which is that this 41.3, the plain
[06:46] number with no tricks on today's build,
[06:48] equals what the same card was hitting on
[06:50] launch day with the trick turned on. So,
[06:52] the software alone has gotten that much
[06:54] better. Prompt reading at 64k context
[06:57] runs at 767 tokens per second. So, a
[07:00] full 64k prompt takes about 85 seconds,
[07:03] which is actually the fastest prefill of
[07:05] any single card on this list. And $1,445
[07:10] divided by 41.3 is about $35 per plane
[07:14] token per second, which is the benchmark
[07:16] every other card here has to justify
[07:18] itself against. Now, the natural
[07:20] follow-up is the 4090 with the same 24
[07:23] GB and 47.7 plane tokens per second.
[07:27] That sounds tempting until we see it
[07:29] costs $3,166,
[07:32] which is 2.2 times the price for 15%
[07:36] more speed. And since it's still 24 GB,
[07:39] the same context window limits apply. So
[07:41] the 3090 is not the most exciting
[07:43] answer, but it might be the right one.
[07:45] It runs every engine, Llama, CPP, VLM,
[07:49] and everything else. So if you already
[07:51] own one, there is a strong case for
[07:53] keeping it, upgrading your software, and
[07:55] waiting for that pull request to merge.
[07:57] And if you don't own anything yet, this
[07:59] is your yard stick. So, keep $35 per
[08:02] token per second in your head as we go
[08:03] through the rest of the list because the
[08:05] very next card is the first one that
[08:07] beats that yard stick. And it surprised
[08:09] me enough that I think it might be the
[08:11] most underrated option on this list
[08:12] right now. It's the RTX 3060 12 GB. And
[08:16] I do mean the 12 GB version, not the 8
[08:19] GB one, which will not do this job. Each
[08:22] card has 360 GB per second of memory
[08:25] bandwidth and draws 170 W. They cost $38
[08:29] each. So, $616 for the pair, and they're
[08:33] up only 6% in 3 months, which is the
[08:35] smallest price movement on this entire
[08:37] list. Now, does two cards sound
[08:40] complicated? It's actually less
[08:42] complicated than it sounds. We run them
[08:44] in tensor split mode, where the model is
[08:47] spread across both GPUs at the same time
[08:49] instead of one after the other on a
[08:51] motherboard with two PCIe 3x8 slots. One
[08:55] owner ran this setup at 131,000 tokens
[08:58] of context with a 4-bit KV cache and got
[09:01] 34.2 tokens per second of plane decode,
[09:04] which is decent. Not the fastest, but
[09:06] not embarrassing either. And $616
[09:09] divided by 34.2 is about $18 per plane
[09:13] token per second. The cheapest on this
[09:15] entire list by a meaningful margin. But
[09:18] the trade-off is real and it's
[09:19] prefilled. Each 3060 has about a third
[09:22] of a 3090s compute and one owner's real
[09:25] world test put a 129,000 token prompt at
[09:29] roughly 4 and a half minutes. So if you
[09:31] paste large code bases or documents at
[09:33] the start of every session, that weight
[09:35] adds up fast. And the memory picture is
[09:37] solid though because the combined 24 GB
[09:40] gives us the same 64,000 token context
[09:43] window at full precision as the 3090.
[09:46] And with a 4-bit cache, we can push
[09:47] further. So, if your workload is
[09:50] conversational, things like back and
[09:51] forth chat, shorter context, and writing
[09:54] help, this is the cheapest credible
[09:57] entry point for Quen 4. And the price
[09:59] per token number makes me a little
[10:00] suspicious that the market has not
[10:02] figured this out yet because the fact
[10:04] that has only moved 6% while everything
[10:06] around it jumped tells us something. The
[10:09] one caveat is that you need a compatible
[10:11] motherboard and you need to remember to
[10:13] set tensor split, not layer split, as
[10:16] your split mode. And that one setting is
[10:18] the whole story behind the next card.
[10:20] The next card is the RTX 5060 Ti, the 16
[10:24] GB version. And this is where I want to
[10:26] tell you a story about a flag. Each card
[10:29] has GDDR7 memory at 448 GB per second,
[10:33] draws 180 W, and connects over PCIe 5X8.
[10:37] It launched at $429,
[10:39] while today GPU Poet's three cheapest
[10:41] average is $793 per card. And you can
[10:45] find an Asus Prime for $829.99
[10:49] on Amazon. So that is $1,586
[10:52] for the pair new with a warranty and 32
[10:55] GB total. And that 32 GB matters, which
[10:59] we'll get to in a minute. Now, the story
[11:01] I promised is about what Llama CPP does
[11:04] by default when you install it and run
[11:06] two GPUs. It splits the model by layers.
[11:09] So in practice, one card does its part
[11:11] and passes the baton to the other. And
[11:14] while one works, the other waits. On
[11:16] this pair, the default layer split gives
[11:19] us 22.1 tokens per second. And if we
[11:22] switch to tensor split, which spreads
[11:24] the work across both GPUs at the same
[11:26] time, like a proper parallel job, the
[11:29] same two cards hit 37 to 38.3 tokens per
[11:33] second. That is 68% faster for free from
[11:37] a single flag in your command. And I
[11:39] really cannot stress this enough because
[11:41] if you have ever run two GPUs and
[11:43] thought they felt slower than you
[11:45] expected, the split mode is the first
[11:47] thing to check since this one mistake
[11:49] eats nearly 40% of your performance and
[11:52] nobody talks about it enough. At 38.3
[11:55] tokens per second, the pair costs $41
[11:58] per plane token per second and the 64k
[12:01] prefill takes 91 seconds, the same as a
[12:04] 5090 on Llama CPP. And the 32 GB total
[12:08] lets us hold 128,000 tokens of context
[12:12] at full KV cache precision. That is the
[12:15] professional tier for context. Enough
[12:17] for a full coding session, a long
[12:19] document, or a lengthy research thread
[12:21] without compression. One more thing
[12:22] worth mentioning is Basalt, the fast
[12:25] engine built specifically for RTX50
[12:27] series cards. Based on what people on
[12:29] Local Lama have been tracking, it has
[12:32] been shipping support for major model
[12:33] launches within about 2 days of release.
[12:36] And that is a good sign for day one
[12:38] Quinn 4 support on this hardware. So the
[12:40] 5060Ti pair is a modern option at a
[12:43] price that is not completely unhinged.
[12:45] And the 32 GB future proves you in a way
[12:48] that 24 GB cards can't. And if you like
[12:51] the idea of two cards in Tensor Split
[12:53] but want more speed, the obvious next
[12:55] step up is the card a lot of you have
[12:57] been asking about in the comments. So
[12:59] let me address it directly. The RTX
[13:01] 5070Ti has 16 GB per card of GDDDR7 at
[13:06] 896 GB per second, which is double the
[13:09] 5060Ti and draws 300 W each. It's 1,313
[13:14] each on GPU poets average, up 24% in 3
[13:18] months, with the lowest new Amazon
[13:20] listing at $1,449.99.
[13:24] So that is $2,626
[13:27] for the pair, which is real money. One
[13:30] owner ran two of them in tensor split at
[13:32] 32,000 tokens of context with a full
[13:35] precision KV cache and got 69.7 tokens
[13:38] per second of plain decode. They
[13:40] measured with their own method rather
[13:42] than the standard benchmark script. So I
[13:44] would treat it as one careful data point
[13:46] rather than a cross validated number,
[13:48] but it's a credible one. And to put 69.7
[13:51] in perspective, it's 91% of a 5090s
[13:55] plane speed for 43% of a 5090s market
[13:58] price.
[13:59] $2,626
[14:02] divided by 69.7 is $38 per plane token
[14:06] per second, which is cheaper than a 5090
[14:08] by a mile. The constraints are 600 W
[14:11] total for the cards alone. So, your
[14:13] power situation has to handle that, plus
[14:15] a board with 2x8 PCIe slots. And just
[14:18] like the 5060Ti pair, we're at 32 GB
[14:21] combined. So, 128K context in full
[14:25] precision. So, if you have the desk
[14:27] space and the power budget, this is a
[14:29] compelling answer. The gap between this
[14:30] pair and a 5090 at more than twice the
[14:33] price is really hard to justify unless
[14:35] you have specific serving needs that
[14:37] require a single card. Now, everything
[14:39] so far has been Nvidia, so it's time to
[14:42] talk about AMD. And I want to be
[14:43] straight with you about where things
[14:44] stand because the AMD story on Local AI
[14:47] is more complicated than the Nvidia one.
[14:50] The Radeon RX7900 XTX has 24 GB of GDDR6
[14:55] at 960 GB per second, just a hair more
[14:59] than the 3090s 936. It draws 355 watts
[15:03] and launched at $999
[15:06] back in the day. And today it is $1,291,
[15:11] up 39% in 3 months, which is the biggest
[15:14] price jump of any consumer card on this
[15:17] list. So something is clearly happening
[15:19] in the used market here. When we look at
[15:21] Quinn 3.827B
[15:23] on this card, three different owners
[15:25] posted plain decode numbers with 41
[15:27] tokens per second on Windows with
[15:29] Vulcan, 36.3 on Linux with RoroxM, and
[15:32] 28.8 on a different Vulcan setup. So the
[15:35] same card on the same model lends
[15:37] anywhere from 29 to 41 tokens per
[15:40] second. And that 12 token per second
[15:42] spread is not a hardware difference.
[15:44] It's the software. AMD's ecosystem for
[15:47] local AI really is more variable than
[15:49] Nvidia's. And the gap between getting
[15:51] your backend configuration right and
[15:53] getting it wrong is enormous. If you're
[15:56] comfortable with that kind of
[15:57] troubleshooting, fine. But if you want
[15:59] to plug it in and have it work, that is
[16:01] a real consideration. At its best run,
[16:04] it's $31 per plane token per second, and
[16:07] it's the cheapest single card 24 GB
[16:10] option on this list. The prompt reading
[16:12] number is unknown because nobody has
[16:14] posted a clean Quinn 3.8 prefilled
[16:17] benchmark for this card and that is a
[16:20] data gap I want to be upfront about. So,
[16:22] if you're already in the AMD ecosystem,
[16:24] comfortable with ROCM or Vulcan tuning
[16:27] and can hit that 41 consistently, it's
[16:29] good value. But if you're starting fresh
[16:31] and you're not sure, the 3090 is the
[16:33] more predictable choice at a similar
[16:35] price. And if software decides how good
[16:37] the 7900 XTX is, the next AMD card takes
[16:41] that idea much further. It's expensive
[16:44] on paper, but it might be worth it for
[16:46] the right use case and very wrong for
[16:48] another. It's the AMD Radeon AI Pro
[16:51] R9700 with 32 GB of GDDR6 at 640 GB per
[16:57] second, 300 W, and the RDNA4
[17:00] architecture. And we shouldn't confuse
[17:01] it with the RX970 XT, which is the same
[17:05] chip with only 16 GB. It launched at
[17:08] $1,299.
[17:10] And today, Sapphire's version is $1,943
[17:14] on Amazon, while GPU Poet's three
[17:17] cheapest average across only nine
[17:19] listings is $2,24.
[17:22] So, this card is not being sold in
[17:23] volume yet. Plain decode on Vulcan on
[17:26] Windows is 29.7 tokens per second and
[17:30] another owner got 27. At Sapphire's
[17:32] $1,943,
[17:35] that works out to about $65 per plane
[17:37] token per second. That is high when we
[17:40] compare it to a 3090 doing 41.3 tokens
[17:43] per second for $1,445.
[17:47] So, why is this card on the list at all?
[17:49] It comes down to one engine, and that
[17:51] engine is called Radiance. Radiance is
[17:54] an inference engine built specifically
[17:56] for AMD's RDNA4 architecture on Linux
[17:59] and Oliver Szer tested it against the
[18:01] standard Vulcan path on the same R9700
[18:04] on November 18th for cold prompt reads
[18:07] meaning fresh context model loading from
[18:10] scratch. Radiance was 3 to 4.2 times
[18:13] faster. But when it read a prompt the
[18:15] engine had already cached, both paths
[18:18] were essentially tied. For certain
[18:19] workflows, that speed up is significant,
[18:22] especially ones where a fast cold start
[18:24] matters, like a model server where every
[18:27] session starts fresh. So if Radiance
[18:29] ships Quen 4 support quickly and your
[18:31] workload fits its strengths, this
[18:33] becomes a compelling 32 GB single card
[18:36] option. But if Radiance does not ship
[18:38] Quen 4 quickly, we're on the left
[18:41] column, which is not competitive at this
[18:43] price. And that is the gamble. And if
[18:46] the R9700 is a gamble on one engine, the
[18:49] next card is the real wild card. It has
[18:52] the most dramatic spread between the two
[18:54] columns on this entire list. The Intel
[18:57] Arc Pro B70 has 32 GB of GDDR6 at 68 GB
[19:02] per second and 32Z cores. And it
[19:04] launched in March at $949.
[19:07] Today it's $1,793,
[19:11] up 89% from launch and 24% in just 3
[19:15] months. So this thing has gotten
[19:16] expensive. Jonathan man ran thorough
[19:19] tests on Quen 3.827B
[19:21] and on plain Lama CPP with SYCL decode
[19:25] was 21.41 tokens per second while with
[19:28] Vulcan it was 16.02. Those are the
[19:31] numbers you get when you just plug it
[19:33] in. But with Intel's VLLM, a 4-bit
[19:36] checkpoint, MTP at four tokens, and a
[19:38] community patch, it hit 84.56
[19:42] tokens per second, which is 3.9 times
[19:45] the plane speed and the widest gap
[19:47] between columns on this entire list. So,
[19:50] if you can get the patched VLM setup
[19:52] working perfectly on day one, the B70 is
[19:54] fast. And if you can't because the patch
[19:57] hasn't been updated for Quinn 4 yet or
[19:59] the setup will not work on your system,
[20:01] you're paying $84 per plane token per
[20:05] second. That is the worst value for
[20:07] money on this list. Man also flagged
[20:09] that two overlapping requests with MTP
[20:12] on can crash that engine. So even at its
[20:14] best, the high number is a single user
[20:17] number on a carefully configured setup.
[20:19] The B70s twin, the ARC Pro B65, has the
[20:23] same 32 GB and the same bandwidth with
[20:26] fewer compute cores, and ASRock's
[20:28] version was about $1,450
[20:31] on November 23rd. Write speed should be
[20:34] similar since the bandwidth is the same,
[20:36] while prefill will be slower, but nobody
[20:38] has posted Quinn 3.8 numbers on it yet.
[20:41] So, the B70 is a card for experimenters.
[20:44] And if you enjoy getting into the weeds
[20:46] on engine configuration and community
[20:48] patches, there is an impressive ceiling
[20:51] here. But if you want something that
[20:52] reliably works on day one, I'd look
[20:54] elsewhere on this list. Now, if the B70
[20:57] is a bet on software catching up, the
[21:00] next two cards are a bet on software not
[21:02] leaving them behind. We're getting into
[21:04] the professional data center cards that
[21:06] have drifted into the used consumer
[21:08] market. The first one is the Nvidia
[21:10] Tesla V100, the 32 GB PCIe version with
[21:15] HBM2 memory at 900 GB per second, a 250
[21:19] watt draw, no fans, and no display
[21:22] output. And if you get the SXM2 version,
[21:25] it will not even fit a standard PCIe
[21:27] slot without an adapter board. So, make
[21:29] sure you're buying the PCIe version.
[21:31] It's $981 today, up 48% in 3 months. And
[21:36] that price jump tells us people are
[21:37] noticing the value here. One owner ran
[21:39] it in a Dell Power Edge server at 4,000
[21:42] tokens of context and got 33.3 tokens
[21:45] per second of plain decode. That is $29
[21:48] per plain token per second with 32 GB on
[21:51] a single card. And it's good value for a
[21:54] card that gives you the full 128k
[21:56] context window without needing two GPUs.
[21:59] But the catch here is real and it's
[22:01] time. CUDA 13 dropped Volta support and
[22:04] the R580 driver branch is the last one
[22:07] that supports the V100. So every new
[22:10] engine release that targets CQ 13 moves
[22:13] a little further away from this card and
[22:15] Quinn 4 is going to need new engine
[22:17] releases because that is just how it
[22:18] works with new architectures. So if
[22:20] those releases require QA 13, the V100
[22:23] is left out. So, if you buy this card
[22:26] today, you're betting that software
[22:28] support holds long enough to matter and
[22:30] that bet gets harder to win every month,
[22:32] which is worth knowing going in. And if
[22:34] the V100 is on borrowed time, the next
[22:36] card is even older. I want to be careful
[22:39] with this one because it's complicated.
[22:41] It's two Nvidia Tesla P 116 GB PCIe
[22:45] cards from 2016, each with HBM2 at 732
[22:49] GB per second and a 250 watt draw. They
[22:52] have no tensor cores since they predate
[22:54] the voltage generation. They're $176
[22:58] each, so $352 for the pair. And they
[23:01] were $87 each, which is a 102% jump in 3
[23:05] months and the biggest price movement on
[23:07] this entire list. So, the market found
[23:10] this deal, and it's getting less of a
[23:11] deal by the week. On paper, two cards
[23:14] with 1,464
[23:16] GB per second of combined bandwidth
[23:19] should hit around 88 tokens per second.
[23:22] But stock llama CPP gets 17.5 which is
[23:25] 20% of the ceiling and really terrible.
[23:28] And most of the problem is that these
[23:30] old cards don't have the hardware
[23:32] primitives that modern kernels are
[23:34] optimized for. Now the interesting part
[23:36] is a developer named KMAC reportedly 17
[23:39] years old and I say that with nothing
[23:41] but respect who has built and maintains
[23:43] a fork of LMA CPP with kernels optimized
[23:47] specifically for P100S.
[23:49] And that fork gets 32.6 plane tokens per
[23:53] second or about 54 with MTP. They've
[23:56] said they'll update it for Quinn 4. The
[23:57] kernels assume a head size of 256
[24:00] which matches what Intel's deleted code
[24:02] says Quinn 4 keeps. So there is reason
[24:05] to believe the fork will stay relevant.
[24:07] And on stock Llama CPP, $352 divided by
[24:11] 17.5 is $20 per plane token per second.
[24:14] While on the fork, $352 divided by 32.6
[24:18] six is $11. But before you get excited,
[24:21] I want you to sit with the prefilled
[24:22] number. At 65,000 tokens, which is a
[24:25] normal coding agent context, these cards
[24:28] process 101 to 119 tokens per second. So
[24:33] you wait 9 to 11 minutes before your
[24:35] model writes its first word. And you
[24:37] wait that long on every session and
[24:39] every large prompt. For short chat, that
[24:41] is acceptable. But if you're doing
[24:43] anything that injects large code bases
[24:45] or documents, which covers most of the
[24:47] interesting use cases for Quinn 4, that
[24:50] weight is painful in a way the price per
[24:52] token number does not capture. And VLM
[24:55] will not run on these at all because
[24:56] they're below its minimum requirements.
[24:58] So the P100 pair is a hardware
[25:01] enthusiasts card, and if you understand
[25:03] what you're getting into and the
[25:04] workload fits, it's the cheapest path
[25:06] in. But if you're buying because the
[25:08] number looked good in a Reddit thread,
[25:10] you'll be frustrated within a week. And
[25:12] that takes us from the cheapest card on
[25:14] the list to the one everyone actually
[25:15] wants to talk about, which is the Nvidia
[25:17] GeForce RTX 5090 desktop. It has 32 GB
[25:22] of GDDR7 at $1,792
[25:25] GB per second and draws 575 W. The
[25:29] Founders Edition is priced at $1,999
[25:33] when you can actually find one. GPU
[25:35] Poet's three cheapest average is $6,133,
[25:39] which is 3.1 times MSRP. And the
[25:42] cheapest new listing on Amazon on
[25:43] November 23rd was an ASUS tough at
[25:46] $7,280.
[25:48] Short prompt plane decode is 76.9 tokens
[25:51] per second. So, at the market rate,
[25:53] we're paying $80 per plane token per
[25:56] second, the second most expensive on
[25:58] this list behind only the B70s left
[26:01] column. Now, the measurement that
[26:03] completely changes how I see this card
[26:05] is the one nobody mentions in the hype
[26:07] videos. Hardware Corner ran it on Llama
[26:09] CPP at real context lengths, and they
[26:12] got 74.83 tokens per second at 4,000
[26:16] tokens, 26.22 at 64,000 tokens, and
[26:21] 22.79
[26:22] at 128,000. So, at 64K context, which is
[26:27] a normal day for a coding agent session,
[26:30] a $1,445
[26:32] RTX3090
[26:34] writes 29% faster than the 590, which
[26:38] means a card costing more than four
[26:40] times as much is writing slower on the
[26:43] workload most people actually use it
[26:45] for. So, what's going on? At long
[26:47] context, the KV cache starts competing
[26:50] with the model weights for memory
[26:51] bandwidth. So, the 5090s raw bandwidth
[26:54] advantage gets partly eaten by the extra
[26:57] data it has to move for the larger
[26:58] cache, while the 3090s tighter memory
[27:01] footprint handles it more gracefully at
[27:03] these context sizes. The picture changes
[27:05] completely though if you're serving
[27:07] several users at once because VLM and SG
[27:10] lang with MTP switched on is where this
[27:12] card shines. One owner posted 76 tokens
[27:16] per second for a single user on SG Lang
[27:19] and about 970 tokens per second total.
[27:22] across 32 simultaneous agents. So, if
[27:24] you're running a small team server, the
[27:26] math works out. But if you're one person
[27:29] running local AI for yourself, the 5090
[27:31] at market prices is very hard to
[27:33] recommend on the left column alone. So,
[27:35] now that we've been through all 10, we
[27:37] can put them side by side and rank the
[27:39] whole list by one number. That is
[27:41] today's price divided by plain tokens
[27:44] per second, which is what you're
[27:46] actually paying for real performance on
[27:48] day one. At the cheap end, 2360s cost
[27:51] $18 per token per second and 2P100 cost
[27:54] $20 on stock Lama CPP or $11 on the
[27:58] fork. Then the Tesla V100 sits at $29,
[28:01] the RX7900 XTX at $31 on its best run
[28:06] and the RTX3090 at $35. And after that
[28:10] come two 5070 TS at $38, 2560 Ti at $41,
[28:15] and the R9700 at $65. And at the top,
[28:19] the RTX5090
[28:21] costs $80 at market price on short
[28:24] context, while the ARK Pro B70 costs $84
[28:28] on its left column. But there are two
[28:30] filters that change that ranking in
[28:32] practice. The first filter is prompts.
[28:35] The P100 pair loses 9 to 11 minutes on
[28:38] every large prompt, which is not a
[28:40] footnote, but a workflow problem. So, if
[28:42] your use case puts anything close to a
[28:44] full context window into each session,
[28:46] those cards aren't for you. The second
[28:48] filter is the software calendar. The
[28:50] V100 is on its last driver branch, and
[28:53] the B70 and R9700 have promising high
[28:56] numbers that depend on engines staying
[28:58] current. Meanwhile, the 3090, the 4090,
[29:02] and the 50 series Nvidia cards have no
[29:04] software timeline concerns. Now, the
[29:06] thing that is easy to miss when we watch
[29:08] GPU recommendation videos is that three
[29:11] of the four cheapest cards by token per
[29:13] dollar got expensive first since August.
[29:16] The P100 doubled in price. The V100 is
[29:19] up 48% and the 7900 XTX is up 39% while
[29:24] only the 3060 pair has barely moved. And
[29:27] to me, that says the market is pricing
[29:29] these cards for the right column, the
[29:31] trick number, and not the left column
[29:33] that'll actually deliver on Quen 4's day
[29:35] one. So, the most honest advice I can
[29:37] give you right now is to buy for the
[29:39] left column and celebrate the right one
[29:41] when it arrives as a free upgrade. If
[29:43] you're a single user who wants the best
[29:45] playing performance per dollar today,
[29:47] and your workload is conversational, two
[29:49] 3060s are hard to argue with. If you
[29:52] want a single card with room to grow
[29:53] into longer context, the 3090 is the
[29:56] proven choice. And if you want 32 GB of
[29:59] future proofing on a modern
[30:00] architecture, the 5060 Ti pair is
[30:03] compelling. And if you're on a pure
[30:05] budget and understand the trade-offs,
[30:07] including that weight, the P100 pair on
[30:10] KMIX fork is wild in the best and worst
[30:12] ways. Whatever you decide, check the
[30:15] split mode before you blame the card.
[30:17] run tensor split rather than layer split
[30:19] because that one flag could be hiding
[30:21] 40% of your performance right now. And
[30:24] one last thing, when quen four small
[30:26] models actually land with weights we can
[30:28] download and run ourselves, the
[30:30] benchmark table will update and the
[30:32] community will post real numbers and
[30:34] then we'll see which cards moved up and
[30:36] which stayed where they are. And that is
[30:38] the moment this whole conversation gets
[30:40] resolved. Until then, buy something
[30:43] you'd still be happy with if Quen 4's
[30:45] small models arrive late or if the
[30:47] architecture changes enough that the MTP
[30:49] trick needs another few months in a
[30:51] draft pull request because the left
[30:53] column is the one that is real. If this
[30:56] breakdown helped you, the subscribe
[30:57] button is right there. I'm going to
[30:59] cover the actual Quinn 4 small model
[31:01] benchmarks the moment the weights drop.
[31:03] And that video is going to look very
[31:05] different from what everyone else posts
[31:06] since we'll be looking at both columns
[31:08] and we'll know what we're seeing. and
[31:10] drop your current GPU in the comments
[31:12] because I'm curious what everyone's
[31:13] running and what your plane tokens per
[31:15] second number looks like. I'll see you
[31:17] in the next one.