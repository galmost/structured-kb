[00:00] A few months ago, I actually lost sleep
[00:02] over a shopping cart, and I mean real
[00:04] stare at the ceiling sleep. It wasn' a
[00:06] Black Friday TV deal or a graphics card.
[00:09] It was a cart with two Mac Studios in it
[00:11] that came to $44,598
[00:15] and I was hovering over the checkout
[00:16] button telling myself this was a
[00:18] reasonable decision. My reasoning
[00:20] sounded airtight at the time. And these
[00:22] new 1 TB AI models are out, they're open
[00:25] source, and they're some of the most
[00:27] powerful things in the world right now.
[00:29] So if I just own the hardware to run
[00:31] them myself with no subscriptions, no
[00:33] API bills, and no company randomly
[00:36] changing the model on me, I'd be free
[00:38] both financially and creatively, like a
[00:40] digital homesteader with a TB of raw
[00:42] intelligence living on my desk. I had
[00:44] convinced myself because the math felt
[00:46] right and the vibe felt right. And then
[00:49] I sat down and did the actual math. Now,
[00:52] if you've been anywhere near the AI
[00:53] space lately, you've seen the headlines
[00:55] about Meta's new Spark Open, Mistral's
[00:58] Large 4, and Moonshot's Kimi K 3.1 Pro.
[01:01] And these are the models people mean
[01:03] when they say a 1 TB AI model, and
[01:06] you've definitely been tempted by the
[01:08] idea of running one of these monsters
[01:09] locally. The hardware vendors, the
[01:11] YouTube reviews, and the Reddit threads
[01:14] will all happily tell you which box to
[01:15] buy. But what they won't tell you is
[01:17] what that box charges you every single
[01:20] time it writes a word, and that number
[01:22] really changes everything. So that's
[01:24] what we're going to price out today,
[01:26] which isn't the specs or the vibes, but
[01:28] the actual receipt. We'll go through
[01:30] every path to running a TB at home as of
[01:33] today, November 16th, 2026, with the per
[01:36] token cost, the speed, and the real
[01:38] world wait times. And then we'll get an
[01:41] honest answer to the question everyone
[01:43] skips, which is, does any of this
[01:46] actually beat renting?
[01:48] That's the answer I wish I'd had before
[01:49] I almost dropped $44,000 on a Mac Stack.
[01:53] Now, before we price anything, we need
[01:55] to fix a naming problem that's caused
[01:57] me, and I'm guessing you too, a of
[02:00] confusion. When someone says one
[02:02] terabyte AI model, they're using TB in
[02:05] two different ways, and they almost
[02:07] never bother to explain which one they
[02:08] mean.
[02:09] The T in a model name refers to
[02:11] parameters, as in one trillion
[02:14] parameters. TB on a price tag refers to
[02:17] bytes, as in one terabyte of storage,
[02:20] and these two units only line up by
[02:22] accident, which the marketing around
[02:24] these models takes full advantage of.
[02:26] So let's meet the three models we're
[02:27] actually talking about. The first is
[02:29] Meta's Muse Spark Open, released October
[02:32] 15th with 816 billion parameters and
[02:36] about 42 billion of those used for each
[02:38] token it generates. And its full
[02:40] precision download is 1,644
[02:43] GB, and Meta also ships its own four-bit
[02:46] compressed version, which brings it down
[02:48] to 533 gigs. The second is Mistral Large
[02:52] 4, which went open on October 29th.
[02:55] Mistral calls it 1T, meaning roughly a
[02:57] trillion parameters with 52 billion
[03:00] active per token. And its official
[03:02] download is 1,060 GB, already compressed
[03:05] to eight-bit. That makes it the only one
[03:08] of the three that's actually a terabyte
[03:09] that shipped, while the others come out
[03:11] bigger or smaller depending on how you
[03:13] count.
[03:14] And the third is Kimi K 3.1 Pro from
[03:17] Moonshot AI, open since November 4th.
[03:20] This one is a beast with 2.78 trillion
[03:23] [snorts] parameters in total and 104
[03:26] billion active. And even after Moonshot
[03:28] already squeezed most of it down to four
[03:30] bits, the download is still 1,561
[03:34] GB.
[03:36] Now, there's one more unit trap I need
[03:37] to flag before we go further because
[03:39] this one burned me personally when I was
[03:41] planning my setup. When Apple sells you
[03:43] a Mac Studio with 512 gigs of memory,
[03:46] those are binary gigabytes. And in
[03:48] practice, that works out to about 550 of
[03:51] the decimal gigabytes hugging face uses
[03:53] when it lists file sizes. So there's
[03:55] actually about a 7% gap in your favor.
[03:58] It's not huge. But when you're staring
[03:59] at a model that's 533 gigs and a machine
[04:02] that holds 512, that 7% really matters
[04:07] and we'll come back to it. So 1 terabyte
[04:09] model is a marketing phrase rather than
[04:11] a precise technical spec. And the three
[04:13] models it refers to range from 533 gigs
[04:16] to 1,561
[04:18] gigs and the box that fits one of them
[04:20] might not fit any of the others.
[04:23] To be fair, the case for owning one of
[04:25] these is genuinely compelling and I
[04:27] spent weeks building this case in my
[04:29] head and it wasn't delusional, it was
[04:31] just incomplete. The pitch starts with
[04:34] the fact that a model running on your
[04:35] own hardware can't be quietly nerfed and
[04:38] this has happened with providers
[04:40] swapping out models, downgrading
[04:42] versions without announcement, changing
[04:44] pricing mid contract and retiring models
[04:46] people had built entire workflows
[04:48] around. When a model lives on your desk,
[04:50] none of that happens. So it runs the
[04:52] same way on day one as it does on day
[04:54] 1,000. Your data also never leaves the
[04:57] building. Your code, your documents and
[05:00] your prompts go to the model and stay
[05:02] there and for a lot of people in a lot
[05:04] of industries that isn't a nice to have
[05:06] but a legal requirement which we'll come
[05:08] back to later. And the licenses on some
[05:10] of these models are genuinely
[05:12] extraordinary. [snorts] Kimi K 3.1 Pro's
[05:15] license fully permits personal use which
[05:18] for a 2.78 trillion parameter model, the
[05:21] most powerful open model currently
[05:23] available is pretty striking and someone
[05:26] in the Reddit release thread called it
[05:27] absolutely wild and they were right. The
[05:30] hardware story feels urgent too because
[05:33] memory is already getting expensive and
[05:35] scarce
[05:36] and Nvidia raised the price of the 128
[05:38] gig DGX Spark from $3,999
[05:42] at launch to $6,950
[05:45] in October which is a 74% price hike in
[05:48] one product cycle.
[05:50] So if you're going to build, the
[05:51] argument goes, you should buy now before
[05:54] it costs even more. And underneath all
[05:56] of this is a very specific dream that I
[05:58] think a lot of us share.
[06:00] It's the idea that you could buy a box,
[06:02] pay once and be done with it with no
[06:04] monthly bills, no tokens, and no
[06:06] invoices, like it's 2010 and software
[06:08] was something you bought rather than
[06:10] something you rented in perpetuity.
[06:12] I totally understand why this feels
[06:14] right because I felt it, and I still
[06:16] feel it a little. But what they never
[06:18] put on the product page is that the box
[06:20] isn't free, and it charges you too on
[06:23] every single token it writes through the
[06:25] hardware cost and the electricity you're
[06:27] using to run it.
[06:29] And when we actually do that division,
[06:30] total cost divided by total tokens, then
[06:34] as we'll see, the number is not what
[06:36] you'd hope. Now, before we get to the
[06:38] actual price numbers, I need to explain
[06:40] one piece of technical reality because
[06:43] without it, the costs don't make
[06:44] intuitive sense.
[06:46] And I promise this won't hurt.
[06:48] You might reasonably think that a model
[06:49] like Mixtral open, which uses 42 billion
[06:53] parameters per token, would only need 42
[06:56] billion parameters worth of memory. If
[06:58] it uses 42 billion, it should need 42
[07:01] billions worth of space, which sounds
[07:03] like clean math, right? But that's not
[07:05] how these models actually work. All
[07:07] three of these models use an
[07:08] architecture called mixture of experts.
[07:11] Instead of one giant generalist network,
[07:14] the model is actually hundreds of small
[07:17] specialist networks called experts. And
[07:19] for every single token, a router picks a
[07:22] handful of those experts to handle the
[07:24] job, and only those experts do the
[07:26] actual computation.
[07:28] Mixtral open has 42 billion active
[07:31] parameters, but it's choosing those from
[07:33] a pool of 816 billion spread across
[07:36] hundreds of experts. And Kimi K3.1 Pro
[07:39] has 896 experts in total and uses 16 at
[07:43] a time. The catch is that the next token
[07:45] might pick a completely different set of
[07:47] experts, and the token after that a
[07:49] different set again. So every single
[07:51] expert, all 816 billion parameters
[07:54] worth, has to be sitting in fast memory
[07:57] the whole time waiting to be called,
[07:59] which is like keeping a whole warehouse
[08:00] stocked even if you're only pulling from
[08:02] a few shelves per order. Then for each
[08:04] token, the chip reads those chosen
[08:06] experts out of memory, does the
[08:07] computation and throws it away, and then
[08:09] it reads again thousands of times per
[08:11] answer.
[08:13] There's a name for this in computer
[08:14] engineering, which is memory-bound
[08:16] decoding. If your memory is the
[08:18] warehouse, then memory bandwidth,
[08:20] meaning how fast data moves from storage
[08:22] to the processor, is the width of the
[08:25] loading dock. And this is really why
[08:27] owning hardware loses to renting in a
[08:29] structural way that has nothing to do
[08:31] with margins. A cloud provider serving
[08:33] thousands of users simultaneously is
[08:36] paying for one warehouse and keeping the
[08:38] loading dock moving around the clock
[08:40] with requests coming in from all over
[08:42] the world. But you're paying for the
[08:43] same warehouse to serve one person,
[08:46] which is you, probably for a few hours a
[08:48] day. So the math is brutal before we
[08:50] even start counting dollars. The other
[08:52] thing this architecture means is that
[08:54] total parameter count decides how much
[08:56] memory you need to buy, but it's the
[08:58] active parameters divided by your memory
[09:01] bandwidth that decides how fast it runs.
[09:04] Those are independent variables, so a
[09:06] model with more total parameters might
[09:08] run faster than one with fewer if its
[09:10] active count is lower, which is why the
[09:12] scoreboard we'll get to later has some
[09:14] surprises.
[09:15] Now, this is where I actually have to
[09:17] show my work and also where my heart
[09:20] broke a little. We'll start with the
[09:21] setup that gets the most attention,
[09:23] which is two Mac Studio M5 Ultras with
[09:26] 512 gigs of RAM each. And this is
[09:29] literally what Meta recommends for
[09:31] running Muse Spark Open at home. Apple
[09:33] only sells 512 gigs on its top 80-core
[09:36] GPU model, which costs $22,299
[09:40] per machine, so two of them come to
[09:42] $44,598.
[09:45] When we look at speed, each Mac reads
[09:47] memory at 1.2 terabytes per second,
[09:50] which is fast, but the model is split
[09:52] across two separate boxes connected by a
[09:55] Thunderbolt 5 cable. And that cable is
[09:57] much slower than the memory inside
[09:59] either machine. So whenever the model
[10:01] needs to pass information between the
[10:03] two halves, which it does constantly,
[10:05] it's bottlenecked by the cable. And
[10:07] you've essentially paid for two Ferrari
[10:09] engines and connected them with a garden
[10:11] house. There's also a pricing trap
[10:13] inside the Mac itself, because going
[10:15] from 256 to 512 gigs of memory costs an
[10:20] extra $11,500.
[10:23] And that's why the top comment on the
[10:25] local Llama launch thread for this setup
[10:27] kept pointing out that two 256 gig Macs
[10:30] cost less than one 512 gig Mac, and the
[10:33] memory upgrade curve on these machines
[10:35] is steep.
[10:37] Now, if we go the Nvidia DGX Spark
[10:39] route, we get 128 gigs per Spark at
[10:43] $6,950.
[10:45] Nvidia officially supports clusters of
[10:47] eight, which gets you a terabyte in
[10:49] their units for $55,600.
[10:52] But each Spark reads memory at 273
[10:55] gigabytes per second, less than a
[10:57] quarter of the Mac speed, and eight of
[10:59] them pass work over network links that
[11:01] are slower still.
[11:03] The Spark cluster makes more sense if
[11:04] multiple people are using it at once,
[11:07] but for one person, you're paying for a
[11:08] lot of boxes to do a lot of waiting.
[11:10] Then home lab people know the server RAM
[11:13] route, which is a server board with 16
[11:15] memory slots and a 64 gig DDR5 stick in
[11:18] each one. And since the cheapest 64 gig
[11:21] DDR5 stick on the market right now is
[11:23] about $2,561,
[11:26] 16 of them come to $40,978
[11:29] before the server chassis, the CPUs, or
[11:32] the motherboard. And that number is just
[11:34] the RAM. There's a cheaper version with
[11:36] DDR4, the previous generation, which
[11:39] runs about $295 for the same 64 gig
[11:43] stick. And that's $4,719
[11:46] for a terabyte, 8.7 times cheaper than
[11:50] DDR5.
[11:51] But you pay for it with speed, because
[11:53] DDR4 server RAM is not fast. And with
[11:56] these models, slow memory means slow
[11:58] inference, and in some cases, we're
[12:00] talking single-digit tokens per second.
[12:02] And when we look at GPU cards, the RTX
[12:05] Pro 6000 Blackwell has 96 gigs at an eye
[12:08] watering 1,792
[12:10] gigabytes per second of bandwidth, and
[12:13] NVIDIA lists it at $16,000 each. To get
[12:16] just past the terabyte, you need 11 of
[12:18] them, which is $176,000
[12:21] in cards alone, plus 6,600 W of power
[12:24] draw before you even account for the
[12:26] servers they live in. If you've got that
[12:27] budget, respectfully, what are you doing
[12:30] watching YouTube? And the DGX Station GB
[12:32] 300, NVIDIA's one-box answer, has 748
[12:37] GB, 252 of them fast, with listings
[12:40] running from $90,000 to $115,000,
[12:44] and it doesn't even reach a terabyte.
[12:46] Now, before I get to the per-token math,
[12:49] there's one thing I wish someone had
[12:50] warned me about earlier. It's a hidden
[12:52] gotcha that invalidates a huge number of
[12:54] the it-fits claims you'll see online,
[12:57] which is that macOS only gives the GPU
[12:59] access to about three-quarters of your
[13:01] memory by default. On a 512 GB Mac, that
[13:04] leaves about 412 GB for the model. So
[13:07] the three-bit community build of New
[13:09] Spark Open, the one that's 436 GB and
[13:12] looks like it fits with room to spare,
[13:14] doesn't actually load. It won't until
[13:16] you manually run a sysctl command to
[13:18] raise the memory limit, and that command
[13:20] resets every single time you reboot. It
[13:23] gets even worse for Mistral's official
[13:25] 1,060 GB download because two 512 GB
[13:29] Macs at three-quarters each give you
[13:31] about 825 GB, so Mistral's terabyte
[13:34] doesn't fit. And Meta's recommended two
[13:37] Mac setup runs Meta's four-bit
[13:39] compressed file, not Mistral's model and
[13:42] not the full precision version. So if a
[13:44] guide says a model fits a Mac and
[13:46] doesn't mention the memory limit flag,
[13:48] that guide measured the sticker rather
[13:50] than the machine. What's really rare
[13:52] here is that Apple actually published
[13:54] speed benchmarks for running New Spark
[13:56] Open on its own hardware, on its own
[13:59] machine learning blog, the day the model
[14:01] launched. And that's as good as these
[14:03] numbers get since they were measured by
[14:05] the people who built the hardware and
[14:06] optimized for their own software stack.
[14:08] On two 512 GB Mac Studios with Meta's
[14:12] four-bit weights and a prompt of about
[14:13] 8,000 tokens, The best case split came
[14:16] to 24.99
[14:19] tokens per second, and that's the
[14:20] headline number.
[14:21] If we go to four max, which is $89,196
[14:25] worth of hardware, we get to 36.73.
[14:29] So doubling the hardware bought about
[14:31] 47% more speed rather than double
[14:33] because the interconnect is already
[14:35] eating into your scaling. Now the number
[14:37] in that Apple post that matters more
[14:39] than the writing speed is the one nobody
[14:41] puts in their thumbnail. It's the time
[14:43] to first token, which is 8.2 seconds on
[14:45] two max. And that's how long it takes
[14:48] just to read an 8,000 token prompt
[14:50] before the model writes a single word
[14:52] back. With a 65,000 token prompt, four
[14:56] max took over 50 seconds of pure
[14:58] reading, and Apple had to double the
[15:00] cables between machines to get that down
[15:02] to 40 seconds.
[15:04] This matters a lot in practice because
[15:06] these models don't just read your
[15:07] message, they reread everything. And
[15:10] across artificial analysis is full
[15:12] benchmark, Muse Spark Open read 5.72
[15:16] billion tokens and wrote 90.6 million,
[15:20] which is 63 tokens read for every single
[15:23] token written.
[15:24] So if you're using this for agentic
[15:26] work, like coding assistance, multi-step
[15:28] automation, or anything where the model
[15:30] is picking up tools and rereading
[15:32] output, your effective experience is
[15:35] dominated by that reading phase. And
[15:37] every time the agent edits a file, pulls
[15:39] in a new one, or checks the state of a
[15:41] previous step, it rereads the whole
[15:43] context.
[15:45] On a 128,000 token coding prompt at the
[15:48] reading speed Apple measured, you're
[15:49] waiting about 81 seconds before the
[15:51] first word on every uncashed turn. But
[15:54] the same model hosted starts answering
[15:56] in 9.9 seconds, and it writes at 180
[16:00] tokens a second against your 25. Caching
[16:03] helps since local tools will often keep
[16:05] the unchanged part of a prompt in memory
[16:08] so that not every turn pays the full
[16:09] cost. But the moment something new
[16:11] enters the context, you're paying the
[16:13] full prefill price again. So So gap
[16:16] between local and hosted isn't really
[16:18] the writing speed the benchmarks show.
[16:20] It's the minute more you wait while the
[16:22] model re-reads your code on every
[16:24] iteration.
[16:25] And this next one is the number I wish
[16:27] I'd calculated before I started drooling
[16:29] over Mac Studio pairs. We'll take the
[16:31] best case scenario for owning, which is
[16:33] Apple's own measurement of 24.99 tokens
[16:36] per second. We'll also assume the Mac
[16:38] ran literally non-stop, 24 hours a day,
[16:41] 365 days a year for three years straight
[16:44] with no downtime, no reboots, and no job
[16:48] smaller than the benchmark. If we run
[16:50] flat out like that for three years,
[16:52] 24.99 tokens per second produces about
[16:55] 2.36 billion tokens. The two Macs cost
[16:58] $44,598
[17:01] and Apple rates each one at 385 W under
[17:03] full load. So running both of them for
[17:05] three years at 18 cents per kilowatt
[17:08] hour adds another $3,642
[17:11] in electricity. That's a total cost of
[17:13] $48,240
[17:15] against those 2.36 billion tokens.
[17:18] And when we divide one by the other, we
[17:20] get $20.40 per million output tokens.
[17:23] The hosted price for the exact same
[17:25] model, Muse Spark Open with the same
[17:27] weights and the same everything, is
[17:29] $4.25 per million output tokens. And
[17:33] every major provider on Open Router
[17:35] charges the same price. So the box you
[17:38] bought specifically to stop paying rent
[17:40] is charging you 4.8 times the rent. And
[17:43] that's under the most generous
[17:44] assumptions possible with 100%
[17:46] utilization for three years straight and
[17:48] no downtime. If you use the hardware for
[17:51] eight hours a day, which is a heavy
[17:53] working day and not casual use, your
[17:55] cost climbs to about $58 per million
[17:58] tokens. And I haven't even mentioned the
[18:00] worst part yet. That $20 per million
[18:02] figure only counts the tokens the Mac
[18:05] writes, while the hosted price includes
[18:07] everything, from reading your prompt to
[18:09] all the pre-fill processing to the
[18:11] entire interaction. So you're comparing
[18:13] your writing cost against their all-in
[18:15] cost, which means the real premium
[18:17] you're paying is even higher than 4.8 x.
[18:21] Now, per million tokens is abstract in a
[18:24] way that hides what this actually feels
[18:26] like day-to-day, so we'll put it into
[18:28] one real task. According to Artificial
[18:30] Analysis's benchmark data, an average
[18:33] Mixtral open task writes about 58,000
[18:37] tokens. Rented, that task costs $2.02
[18:41] with reading and writing included. At
[18:44] home, at 24.99 tokens per second,
[18:47] writing those 58,000 tokens alone takes
[18:50] about 38 minutes. Hosted at 180 tokens
[18:54] per second, it takes about 5 minutes.
[18:57] And the 38 minutes doesn't even count
[18:59] reading your prompt.
[19:00] For the two max to break even, which
[19:02] means paying off $44,598
[19:05] at $2.02 per rented task, you'd need to
[19:09] run 22,078
[19:11] benchmark-sized tasks. And at 38 minutes
[19:14] per task, back-to-back and non-stop,
[19:17] that's about 1.6 years of the max
[19:19] running without a break. And that
[19:21] assumes every single one of those tasks
[19:24] would have been rented otherwise. So if
[19:25] you're running three or four a day, the
[19:27] math gets much worse. One person on
[19:29] Local Llama checked Apple's trade-in
[19:31] value for a 512 gig M3 Ultra, the
[19:35] generation before the M5, and the offer
[19:38] came back at about a tenth of what they
[19:40] originally paid because depreciation
[19:42] doesn't care about your utilization
[19:43] rate. Now, I really do have to deliver
[19:46] some news here. All of that cost
[19:48] analysis, the $44,598,
[19:52] the $20 per million, and the 38-minute
[19:54] tasks might be worth it if you were
[19:57] getting the best model in the world for
[19:59] it, and you're not. Artificial Analysis
[20:01] rebuilt its intelligence index on
[20:03] October 27th, and Claude Opus 5.5 leads
[20:07] the leaderboard with a score of 58.
[20:09] Mixtral 8x7B, the model Meta recommends
[20:12] and the one those two max studios are
[20:14] designed to run, scores 25. And Mixtral
[20:17] Large 4 scores 26. So we're looking at
[20:20] 25 and 26. GLM 5.3 Flash 28 with 321
[20:26] billion parameters and 18 billion
[20:28] active. And its three-bit build is about
[20:31] 120 gigs, which fits on one 128 gig DGX
[20:35] Spark.
[20:36] DeepSeek V4.1 Flash scores 32, which is
[20:40] meaningfully higher than either Terabyte
[20:42] model. And its full official download is
[20:44] 510 gigs. So with that MacOS memory flag
[20:47] I mentioned earlier, it runs on a single
[20:49] 512 gig Mac. And one owner measured
[20:52] about 66 tokens per second on one Mac
[20:55] with a 128,000 token prompt, which is
[20:58] nearly three times faster than two Macs
[21:00] running New Spark Open. So to be direct
[21:03] about it, two of the three models
[21:05] everyone means when they say one
[21:07] Terabyte model score lower on
[21:08] intelligence benchmarks than models that
[21:10] fit on a single machine, which goes to
[21:12] show the Terabyte buys you parameters
[21:15] without automatically buying you
[21:16] performance. And that brings us to the
[21:18] exception because Kimi K 3.1 Pro scores
[21:22] 46. That makes it the top open source
[21:25] model currently available, 12 points
[21:27] behind Claude Opus 5.5 and genuinely in
[21:30] a different league from New Spark Open
[21:32] or Mistral Large 4. If you're going to
[21:34] go through the trouble and expense of
[21:36] running a Terabyte at home, Kimi is the
[21:38] model that would actually justify the
[21:40] ambition. The problem is that its
[21:42] download is 1,561
[21:44] GB. The usual fix, compressing it to
[21:47] four bits so it's smaller, has already
[21:49] been done. And Moonshot shipped the
[21:51] expert weights in a four-bit format
[21:53] called MXFP4,
[21:55] so there's no massive full precision
[21:57] file sitting there waiting to be
[21:59] squeezed. And Nvidia's own four-bit
[22:01] conversion, posted on November 12th, is
[22:03] actually bigger at 1,605
[22:06] gigs. You also need memory while Kimi is
[22:09] running because the model advertises a 1
[22:11] million token context window.
[22:14] When we look at its own configuration
[22:15] file, every token of context uses about
[22:18] 107 KB of additional memory. So a full
[22:22] million token context adds roughly 112
[22:25] gigs on top of the weights themselves.
[22:27] The smallest Apple setup that can hold
[22:29] Kimi at all is four 512 gig Mac Studios,
[22:33] which comes to $89,196.
[22:37] Nobody has published measured speeds for
[22:38] Kimi on that four Mac setup yet, so we
[22:41] have to estimate. And since Kimi uses
[22:43] roughly two and a half times as many
[22:45] active parameters as Muse Spark Open,
[22:48] scaling Apple's four Mac number down
[22:50] proportionally lands us around 15 tokens
[22:52] per second. That's an estimate rather
[22:54] than a measurement, but it's the best we
[22:56] have right now. And at 15 tokens per
[22:59] second, running flat out for three years
[23:01] with power included, we end up at about
[23:03] $68 per million tokens.
[23:06] But Moonshot rents Kimi K3.1 Pro for $10
[23:10] per million output tokens. And the same
[23:12] task that costs $3.68 rented takes about
[23:16] 80 minutes at home before you even
[23:18] factor in reading the prompt. Break even
[23:20] on $89,196
[23:23] of hardware at $3.68 per rented task is
[23:27] 24,238
[23:29] tasks. And at 80 minutes each, back to
[23:31] back, that's 3.7 years of nonstop
[23:35] running, which is longer than the
[23:36] three-year lifecycle you're pricing the
[23:38] hardware over in the first place. So the
[23:40] model that's actually worth running at a
[23:42] terabyte is also the one that's most
[23:44] expensive to run, most expensive to buy
[23:46] for, and furthest from breaking even.
[23:48] Now,
[23:49] every time I describe this problem,
[23:51] someone in the comments asks, but what
[23:53] about the cheap routes? There are cheap
[23:55] routes, and I want to be fair to them,
[23:57] but each one trades money for time in
[23:58] ways that are worth pricing out clearly.
[24:01] The first one we'll look at is used DDR4
[24:03] server RAM, which is around $4,700
[24:06] for a terabyte of DDR4 in a dual socket
[24:09] AMD EPYC server board. That's genuinely
[24:12] inexpensive compared to everything else
[24:14] we've looked at. But the catch is speed,
[24:16] because each socket reads at about 200
[24:18] GB per second on paper. And owners
[24:21] running comparable setups on DeepSeek
[24:23] report single digit tokens per second.
[24:25] And something as large as Kimi is slower
[24:27] still. At one token per second, one
[24:30] average benchmark task of 72,000 tokens
[24:34] takes 20 hours. And I'm not being
[24:36] dramatic. That's just the math. The
[24:38] second route is SSD streaming, where you
[24:40] leave the model on a fast NVMe drive and
[24:43] load only the expert weights you need
[24:45] for each token on demand. It's the
[24:47] cheapest option because you probably
[24:48] already own most of the hardware. And
[24:50] you don't need a machine with terabytes
[24:52] of RAM, just fast drives and a
[24:54] reasonable amount of DRAM as a cache.
[24:56] But owners streaming Kimi off SSDs
[24:58] report about 1/3 of a token per second.
[25:01] That means one average benchmark task of
[25:03] 72,000 tokens takes roughly two and a
[25:06] half days. And I really do mean days.
[25:09] I want to be kind here, so I'll just say
[25:11] there are use cases where you might not
[25:12] need the answer quickly. And for those,
[25:14] an SSD streaming setup makes sense. For
[25:17] active work though, you'd be watching a
[25:19] progress bar for days. The third route
[25:21] is the tiny box red Kimi from TinyCorp,
[25:24] which was just announced this month at
[25:25] $30,000.
[25:27] It has four Radeon AI Pro R9700 cards
[25:30] holding 128 GB of combined GPU memory
[25:34] plus 16 SSDs in an array rated at about
[25:37] 238 GB per second. And TinyCorp is
[25:40] claiming 40 tokens per second on Kimi
[25:42] K3. But nobody outside the company has
[25:45] measured that yet. One independent
[25:47] analysis worked out that if every weight
[25:49] came off those SSDs on each token, the
[25:52] theoretical ceiling would be about four
[25:54] tokens per second rather than 40. So the
[25:57] claim of 40 depends on most of each
[25:59] token's expert weights already sitting
[26:01] in GPU memory from previous tokens.
[26:04] That's plausible under some workloads
[26:06] and much less plausible under others.
[26:08] And we'll know more once independent
[26:10] benchmarks come in. And then there's
[26:12] aggressive quantization, which is
[26:14] compressing harder than four bits.
[26:17] Unsloth published a one-bit Kimi K3
[26:19] build that matches the original model's
[26:21] next word predictions 78.9%
[26:24] of the time and comes in at 594 GB,
[26:27] which is genuinely impressive work. But
[26:30] someone in the comment on that release
[26:32] asked the obvious question. If you're
[26:33] done to 594 gigs and 79% agreement, why
[26:37] not just run a smaller model at full
[26:39] quality that fits in that space? a fair
[26:42] question because the whole value of Kimi
[26:44] is that it scores 46 on the intelligence
[26:47] index. And with that much compression,
[26:49] the score is probably significantly
[26:51] lower. Now, one more route we need to
[26:53] address is just adding more boxes until
[26:55] the model fits in RAM, whether that's
[26:57] stacking DGX Sparks, Strix Halo nodes,
[27:00] or whatever else. If we stack eight DGX
[27:03] Sparks, we get 1,099 gigs of combined
[27:07] memory, which still doesn't hold Kimi's
[27:08] 1,561 gigs. You need 16. And that's
[27:12] $111,200.
[27:15] On Nvidia's own developer forum, owners
[27:18] running the full Kimi K3 on 16 DGX
[27:20] Sparks report about 21 to 30 tokens per
[27:23] second for a single user. And that drops
[27:26] to 11 to 13 tokens per second as the
[27:28] context grows long.
[27:30] The reason is really the interconnect.
[27:32] Inside each Spark, memory moves at 273
[27:35] GB per second, while between Sparks, the
[27:38] 200 gigabit network link moves about 25
[27:41] GB per second, which is about 11 times
[27:44] slower.
[27:45] And every token that needs data from a
[27:47] different node, which is a lot of
[27:48] tokens, waits on that slow link. So
[27:51] adding more nodes buys you capacity,
[27:54] meaning more total memory and more users
[27:56] served at the same time. But past a
[27:58] certain point, it buys you almost no
[28:00] additional speed for a single user
[28:02] because the bottleneck has moved from
[28:04] memory to networking. And networking
[28:06] doesn't get faster just because you add
[28:08] more boxes. Someone in a comment section
[28:10] suggested eight Strix Halo machines for
[28:13] $26,000 to $30,000. The economics do
[28:16] look better on paper, but it's the same
[28:19] fundamental problem of cheap nodes on
[28:21] expensive links. Now, I've spent most of
[28:24] this video explaining why the numbers
[28:26] don't work out, but I want to be
[28:27] careful. The numbers not working for
[28:29] most people is very different from
[28:31] nobody ever doing this. And there are
[28:33] real for this hardware for whom the per
[28:35] token analysis doesn't matter the way it
[28:37] matters to me. If your data legally
[28:40] can't leave your building, renting isn't
[28:42] an option at any price. So for clinics,
[28:44] law firms, government contractors, and
[28:47] anyone with a data handling agreement
[28:49] that restricts cloud processing,
[28:51] the per token cost is just the price of
[28:53] running this model at all.
[28:55] And the cheap routes are where you test
[28:57] it before you commit to the full setup
[28:59] and the enterprise buy makes sense. If
[29:01] you're serving a team, the math changes
[29:03] substantially. A cloud provider is cheap
[29:05] because it batches thousands of users at
[29:08] once on shared infrastructure, and you
[29:10] can do the same thing. One benchmarker
[29:12] tested four DGX Sparks running DeepSeek
[29:15] and found that with 16 simultaneous
[29:18] users, total token output was about four
[29:21] and a half times higher than with one
[29:22] user. Pack the hardware with enough
[29:25] parallel users and your per token cost
[29:27] falls fast. So for an internal
[29:29] deployment at a company that generates
[29:31] heavy AI traffic, the numbers could
[29:33] actually be competitive.
[29:35] If you need to fine tune one of these
[29:36] models on your proprietary data, most
[29:38] hosted inference platforms won't let
[29:40] you. And training requires the weights,
[29:43] and the weights need to live somewhere
[29:44] under your control. And the rent could
[29:46] change because most of what makes
[29:48] renting cheap right now is competition.
[29:50] There are 18 providers on Open Router
[29:52] all serving Kimi K 3.1 Pro, pricing each
[29:55] other down from $20 to as low as $6 per
[29:58] million tokens for some. Open weights
[30:01] cap what any single provider can charge
[30:03] as long as other providers keep serving
[30:05] the model.
[30:06] But if that market shifts, say Moonshot
[30:09] changes the license or key providers
[30:11] exit, the rental price could move and
[30:13] owning the hardware insulates you from
[30:15] that.
[30:16] What nobody knows yet is how fast Kimi K
[30:19] 3.1 Pro actually runs on four Mac
[30:21] Studios since nobody's published that
[30:23] measurement. And we also don't know
[30:25] whether the tiny box claim will hold up
[30:27] under independent testing or what memory
[30:30] prices will look like next year in
[30:32] either direction. And each of those
[30:34] unknowns could move the numbers
[30:36] meaningfully.
[30:37] So, what should I have done before I had
[30:38] two $22,000 Macs in my cart? I should
[30:41] have rented the exact model I actually
[30:44] want to run, not a subscription that
[30:46] might give me a different model and not
[30:48] an approximate alternative. I'd rent it
[30:50] for one month of real work with real
[30:53] prompts, real tasks, and the same
[30:55] workload I'd actually use it for.
[30:58] Then I'd look at the invoice at the end
[31:00] of that month rather than the
[31:01] subscription price. And the invoice
[31:03] tells me how many tokens I actually used
[31:05] while the subscription only tells me
[31:07] what the company decided to charge.
[31:09] And then I divide the hardware price by
[31:11] that monthly invoice total.
[31:13] That's how many months the box needs to
[31:15] pay itself off before power costs,
[31:18] before depreciation, and before the next
[31:20] generation model makes this one look
[31:22] outdated. For Mew Spark Open and Mistral
[31:24] Large 4, the invoice step shows that you
[31:27] can rent something that scores higher
[31:29] than either of them for less than it
[31:31] costs to own the hardware for either. So
[31:33] the Terabyte is a prestige purchase for
[31:35] those two. For Kimi K 3.1 Pro, the
[31:38] hardware can hold the model, but it
[31:40] can't write fast enough to close the gap
[31:42] with the hosted price before the
[31:43] hardware is obsolete. None of this means
[31:45] local AI is a bad idea. I still run
[31:48] models locally and love what it enables,
[31:51] but what I try not to do anymore is
[31:53] confuse the cost of the model with the
[31:55] cost of the hardware that holds it. The
[31:57] box isn't free because it charges you
[31:59] every time it writes a word, and the
[32:01] first step in deciding whether to buy
[32:02] one is knowing what that charge actually
[32:05] is. If this video saved you from the
[32:07] same cart mistake I almost made or
[32:09] helped you work out whether local is
[32:11] right for your situation, hit the like
[32:13] button. And it genuinely helps this
[32:15] reach people before they spend $44,000.
[32:18] And if you've already made this purchase
[32:20] and you've got two Mac Studios stacked
[32:22] on your desk while you watch this with a
[32:23] complicated expression, drop a comment.
[32:26] I'd love to know what your per token
[32:28] cost has worked out to in practice. And
[32:30] I might be wrong about some of this. So
[32:32] real world data from real owners is
[32:34] worth more than any benchmark. In the
[32:36] next video, I want to get into which
[32:38] models are actually worth running
[32:40] locally right now, the ones where the
[32:42] tradeoff makes sense, because the sweet
[32:44] spot isn't a terabyte, but it does
[32:46] exist. So until then, price the token
[32:49] before you price the