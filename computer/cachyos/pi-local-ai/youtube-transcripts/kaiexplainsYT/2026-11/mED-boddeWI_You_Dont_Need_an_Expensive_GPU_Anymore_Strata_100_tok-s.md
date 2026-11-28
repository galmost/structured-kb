[00:00] You know that feeling when you've spent
[00:01] 3 hours down a rabbit hole reading
[00:03] Reddit threads about running AI locally
[00:06] with the GPU benchmarks and the VRAM
[00:08] requirements and the context windows and
[00:12] then you open your wallet, look at the
[00:13] number, and slowly close it again?
[00:17] That was me for almost a year. Every
[00:19] time I got excited about running a big
[00:21] model locally, I kept hitting the same
[00:23] wall, which was minimum 24 gigs of VRAM.
[00:27] And every time I looked at a card with
[00:29] 24 gigs, the price made me want to go
[00:31] lie down.
[00:32] And my machine is perfectly solid with a
[00:34] Ryzen 5, 64 gigs of RAM, and an RTX card
[00:38] with 12 gigs of VRAM. So, nothing
[00:40] flashy. But every forum, every YouTube
[00:43] video, and every comment section told me
[00:45] the same thing, which was that 12 gigs
[00:47] isn't enough and I should go bigger and
[00:48] spend more. So, I waited and watched.
[00:51] And I told myself that maybe the next
[00:53] GPU cycle would be different. And then
[00:55] in late September this year, something
[00:57] actually changed. A free engine called
[01:00] Strata dropped on GitHub with an MIT
[01:02] license and a desktop app for Windows,
[01:05] Linux, and Mac.
[01:06] And it claimed, with receipts, to run a
[01:09] 763 billion parameter model on a 12-gig
[01:12] card, which is exactly the card sitting
[01:14] in my machine.
[01:16] So, I immediately lost my mind and had
[01:18] to figure out whether this was real and
[01:19] whether it was actually usable. And most
[01:21] importantly, I wanted to know what the
[01:23] catch was because there's always a
[01:25] catch. This video is everything I found,
[01:28] from the good and the genuinely
[01:29] impressive to the "Wait, this is slower
[01:32] than I thought" and the part nobody's
[01:34] putting in their thumbnails. So, let's
[01:36] get into it. Now, first, what is Strata
[01:39] and why does it matter that it existed
[01:41] for only 38 days before people started
[01:43] losing their minds over it? Strata is a
[01:46] local inference engine, which is the
[01:48] software that actually runs an AI model
[01:50] on your hardware. And it sits in the
[01:52] same category as Llama CPP or Ollama,
[01:55] which you've probably heard of, but it's
[01:57] doing something architecturally
[01:58] different under the hood that we'll get
[02:00] to in a second. It went up on GitHub on
[02:02] September 24th, and in the 38 days after
[02:05] that, it shipped 63 releases. I've had
[02:08] houseplants that needed less attention
[02:09] than that. And it also collected around
[02:11] 37,000 GitHub stars, which in open
[02:14] source terms is the equivalent of
[02:16] everyone in a medium-size city standing
[02:18] up and applauding at the same time. And
[02:20] the model it launched with was Qwen 3.8
[02:23] Flash Next at 125 billion parameters,
[02:27] which for context is already enormous.
[02:30] And we're not talking about a cute
[02:31] little 7 billion parameter model you run
[02:33] as a party trick, we're talking about
[02:35] serious reasoning capability. Then, in
[02:38] late October, they added the model that
[02:40] really made the internet go sideways,
[02:42] which was DeepSeek V4.1 Flash, and it
[02:45] has 763 billion parameters, an MIT
[02:49] license, a 1 million token context
[02:52] window, and a claim that it runs on a 12
[02:54] gig card. And that last part is why
[02:56] people started posting screenshots at
[02:58] 11:00 at night and tagging their
[03:00] friends.
[03:01] But one thing I've learned from years of
[03:02] being an excited early adopter is that
[03:04] when something sounds too good to be
[03:06] true, it's usually not false. It's just
[03:09] incomplete. And the complete story here
[03:11] is a lot more interesting than the
[03:13] headline. Now, the part that actually
[03:15] blew my mind once I understood it isn't
[03:17] magic at all. It's just really clever
[03:19] engineering.
[03:20] You'd assume that to run a model, the
[03:22] whole thing has to live in your GPU's
[03:23] memory, and that's what I assumed, too.
[03:26] And that's what all those minimum 24
[03:28] gigs VRAM requirements are based on. And
[03:30] for some models, it's more or less true.
[03:32] But modern large models, especially the
[03:35] ones called mixture of experts models,
[03:37] don't work that way. And DeepSeek V4.1
[03:40] Flash is one of them. So, instead of one
[03:43] giant brain that always uses all of
[03:45] itself, a mixture of experts model has
[03:47] hundreds of small specialized chunks,
[03:50] which are literally called experts. And
[03:53] for each word it generates, it only uses
[03:55] a small handful of them. When we look at
[03:57] DeepSeek, it has 40 layers, each holding
[04:00] 384 experts, and for every single word
[04:04] it writes, it uses six of those experts
[04:07] per layer. So, at any given moment, most
[04:09] of the model is just sitting there doing
[04:11] nothing. And on top of that, DeepSeek
[04:13] carries something called the N-gram,
[04:16] which is basically two lookup tables
[04:18] totaling 196.6
[04:20] billion parameters or a quarter of the
[04:22] entire model. And for each word, the
[04:25] model dips into those tables for a
[04:27] handful of rows and then ignores the
[04:29] rest. What StriDa does is exactly what
[04:31] you're already thinking. It figures out
[04:33] which parts of the model get used
[04:34] constantly, which parts get [music] used
[04:36] sometimes, and which parts barely get
[04:38] touched, and then it puts each part in
[04:40] the [music] cheapest place it can still
[04:42] be read from fast enough. The hot core
[04:44] of the model, which every single word
[04:46] needs, lives on your GPU. And the
[04:49] experts that [music] get used most often
[04:50] go on the GPU, too, as many as will fit.
[04:53] The next tier of frequently used experts
[04:55] goes into your regular RAM. And the
[04:57] stuff that barely gets touched,
[04:59] including that entire 110 gigabyte
[05:02] table, lives on your SSD and only gets
[05:04] pulled when a specific word actually
[05:06] asks for it. So, we end up with three
[05:08] tiers: [music] the GPU, the RAM, and the
[05:11] SSD, with each byte in the cheapest
[05:13] place that's still fast enough for its
[05:15] job. And that's how we run a 763 billion
[05:19] parameter model on 12 gigs of VRAM
[05:21] because the card doesn't hold the model.
[05:23] It only holds the hot part of it. I
[05:26] genuinely sat back when I understood
[05:27] this and just went, "Okay, that's
[05:29] actually brilliant." And it's a chef who
[05:31] keeps their most used knives on the
[05:33] counter, their occasionally used gadgets
[05:36] in a drawer, and their one-purpose
[05:38] specialty tools in a box in the pantry.
[05:40] And they aren't slower because the box
[05:42] is in the pantry since most of the time
[05:44] they never need what's in it. Now, I
[05:45] have to stop and tell you about the
[05:47] number that went viral. And this is the
[05:49] part that almost made me make a
[05:50] different video, and a much angrier one.
[05:53] On October 25th, a post on X claimed
[05:56] that DeepSeek v4.1 flash was running on
[05:58] a 12 gig RTX 5070 at over 100 tokens a
[06:02] second, and it got almost 100,000 views.
[06:06] And another post the same day said 105
[06:08] to 117, and people were quote tweeting
[06:11] it with fire emojis and local AI is here
[06:14] energy. I saw those posts and got
[06:16] excited, and I did the mental math of
[06:19] what over 100 tokens per second on a
[06:21] model that size would mean for actually
[06:23] using it as a coding assistant.
[06:26] And I even started drafting a list of
[06:27] things I'd finally be able to do.
[06:29] And then I actually read Strata's own
[06:31] documentation. Strata's performance
[06:33] table for that exact card, the 12 gig
[06:36] RTX 5070, shows two numbers. So, are you
[06:39] ready for them?
[06:41] It reads your prompt at about 110 tokens
[06:43] a second, and it writes the answer at 4
[06:45] to 6. So, the viral number was the
[06:48] reading speed, which is the thing it
[06:49] does before it says a single word back
[06:51] to you. And I'm not mad at the people
[06:53] who posted it because I probably would
[06:55] have made the same mistake if I'd been
[06:56] the one running the benchmark. But these
[06:59] are two completely different operations
[07:01] that perform in completely different
[07:03] ways, and the gap between them is
[07:05] enormous. Now, reading your prompt is
[07:08] called prefill, and it processes
[07:10] thousands of tokens all at once in a
[07:12] batch. So, when it fetches an expert
[07:14] from RAM or the SSD, it gets a lot of
[07:17] use out of that fetch across the whole
[07:19] batch. Writing the answer is called
[07:21] decode, and it's fundamentally different
[07:24] because it generates one token at a
[07:25] time. And each token needs its own
[07:28] specific set of experts, and each one is
[07:31] its own round trip to whatever those
[07:32] experts are stored. On a 12 gig card
[07:35] running DeepSeek, a lot of those experts
[07:37] are in RAM or on the SSD, and we're
[07:39] doing a fresh trip for each one. And
[07:41] that's why we get 110 tokens per second
[07:44] reading and 4 to 6 writing, two numbers
[07:47] that are more than 20 times apart. So,
[07:49] if you're in a comment section right
[07:51] now, or you see someone sharing a
[07:53] screenshot with a big number on it, the
[07:55] first question to ask is whether that's
[07:57] the reading speed or the writing speed.
[07:59] And those are two completely different
[08:01] conversations about two completely
[08:03] different things. Now, let's talk about
[08:05] what 4.7 tokens per second actually
[08:08] means for real use, because I think this
[08:10] is where a lot of the excitement needs
[08:12] to get grounded. At that speed, a 1,000
[08:15] token response takes about 3 and 1/2
[08:17] minutes of staring at the screen and
[08:19] waiting.
[08:20] And that's roughly a long function plus
[08:22] an explanation, the kind of thing we ask
[08:24] a coding assistant for all the time. I
[08:26] tried this and genuinely sat there and
[08:28] watched it. I have the patience of a
[08:30] person who once waited 25 minutes for a
[08:32] progress bar in 2007 because the
[08:34] alternative was starting over.
[08:36] But 3 and 1/2 minutes of watching a
[08:38] blinking cursor is its own kind of
[08:40] suffering. Now, I want to be fair here
[08:43] because Qwen 3.8 Flash Next, the 125
[08:46] billion parameter model, runs at around
[08:49] 94 tokens a second on the same hardware.
[08:52] That's genuinely fast. A 1,000 token
[08:55] answer in about 11 seconds, and it's a
[08:58] usable model on a 12 gig card, which is
[09:00] where Strata actually delivered on its
[09:02] original promise. But Deep Seek is a
[09:04] different story. And its reading speed
[09:06] only makes the writing speed feel worse
[09:08] by contrast. The first thing that
[09:09] happens is that your prompt reads in
[09:11] fast and you think, "Okay, here we go."
[09:13] And then it just crawls. There's also
[09:15] the prompt reading side to think about.
[09:17] A real coding agent setup that knows
[09:19] your project structure, your tool
[09:21] definitions, and your current file might
[09:23] open with 30,000 tokens of context.
[09:26] >> [music]
[09:26] >> And on the 5070 PC running Deep Seek in
[09:29] its best reading configuration, that's
[09:31] over 2 minutes before it writes a single
[09:33] character back every time we start a new
[09:36] task. One creator who actually ran an
[09:39] agent workflow with Deep Seek on this
[09:40] setup raised the context window, which
[09:43] we need to do for any serious work. And
[09:45] after that, a single simple question
[09:48] about a small game's code base took 11
[09:50] minutes and 30 seconds. And that was on
[09:52] a 12 gig card plus a 24 gig card running
[09:55] together. An answer that slow to a
[09:57] simple question isn't an AI assistant
[10:00] anymore. It's a very polite email
[10:02] thread.
[10:03] I want to be really careful here not to
[10:05] sound like I'm trashing Strata because
[10:07] I'm not, and I'm genuinely impressed by
[10:09] what they built. But I think the right
[10:11] framing is that Strata made it possible
[10:14] to run Deep Seek on consumer hardware.
[10:16] And what possible feels like in practice
[10:18] depends a lot on your hardware and your
[10:20] patience.
[10:22] And on a card that size, possible and
[10:24] pleasant aren't the same thing yet.
[10:26] Now, the part I spent the most time on
[10:28] is where the conversation about you
[10:30] don't [music] need an expensive GPU gets
[10:32] genuinely complicated. Strata's whole
[10:35] bit rests on one idea, which is that
[10:37] gigabytes in RAM are cheap and gigabytes
[10:39] on the card are expensive. So we keep as
[10:42] little as possible on the card and let
[10:43] the cheap RAM do the heavy lifting. That
[10:45] was an excellent bet when Strata was
[10:47] being designed, but it's a harder bet
[10:49] today. So let me run the actual price
[10:51] list as of late October, because this is
[10:54] the math nobody's putting in their
[10:55] thumbnails. A used RTX 3060 with 12 gigs
[10:59] is about $310 on eBay, which is roughly
[11:02] $26 per gigabyte of VRAM. A 64 gigabyte
[11:06] kit of DDR5 desktop RAM, going by the
[11:09] median price across 77 kits in stock
[11:11] right now, is about $1,200,
[11:14] or about $19 per gigabyte. And the thing
[11:17] that stopped me cold when I did this
[11:19] math is that DDR5 RAM now costs about
[11:22] 70% of what a used 3060's VRAM costs per
[11:26] gigabyte.
[11:27] And a year ago, the same kind of kit was
[11:29] about $191,
[11:31] or $3 a gigabyte. Today it's $19,
[11:35] which is more than six times the price
[11:37] in 12 months. So when we look at the
[11:39] build most people in the Strata
[11:41] community are recommending a used 3060
[11:44] plus 64 gigs of DDR5, that's $310 for
[11:47] the card and $1,200 for the RAM. So the
[11:51] RAM costs four times as much as the
[11:53] graphics card, and the expensive part
[11:55] didn't leave, it just moved one slot to
[11:57] the left. One viewer under a Strata
[12:00] video put it better than I could. In
[12:01] Canada, a 5070 Ti costs what a 4090 did
[12:05] at launch, and not needing an expensive
[12:08] card is doing a lot of work in that
[12:09] sentence. Now, there's actually a
[12:12] genuinely cheap path here, and it's the
[12:14] SSD, which is where Strata keeps pushing
[12:16] as much as possible. A 2-TB PCIe 4 NVMe
[12:20] drive runs about $253 right now, which
[12:23] is 13 cents per gigabyte and 150 times
[12:27] cheaper per gigabyte than DDR5. And
[12:29] Strata is constantly finding ways to
[12:31] move more of the model onto it.
[12:33] DeepSeek's 110 GB Angram table comes to
[12:36] about $14 of SSD, whereas the same table
[12:40] sitting in DDR5 would cost about $2,100.
[12:43] So, every gigabyte that moves from RAM
[12:45] to the SSD saves us roughly $19.
[12:49] But, the catch is that the SSD only
[12:50] works for bytes that don't need to be
[12:52] read constantly. And on this particular
[12:54] model, a lot of what matters gets read
[12:57] constantly. The SSD tier is 10 times
[13:00] slower than DDR5 in bandwidth, and DDR5
[13:03] is already four times slower than VRAM.
[13:05] So, the slow tier is where we really
[13:08] feel the cost of running a model that's
[13:09] too big for our hot tiers. And if you're
[13:11] on DDR4 instead of DDR5, which has its
[13:14] own interesting math, a 64-gig DDR4 kit
[13:18] is about $500, or roughly $7.80 per
[13:22] gigabyte. So, you get more than twice
[13:24] the capacity per dollar. The tradeoff is
[13:26] about half the bandwidth, which means
[13:28] the CPU half of every token takes about
[13:30] twice as long.
[13:31] You get more capacity and slower
[13:33] operation, and depending on what you
[13:35] own, that might be the better deal. So,
[13:38] the right question isn't which GPU
[13:41] should I buy, it's what's my per
[13:43] gigabyte cost across all three tiers,
[13:46] and how many gigabytes does the model I
[13:48] want to run need in each one? That's the
[13:50] math that tells us what our actual
[13:52] options are. Now, there's a result in
[13:54] Strata's performance data that genuinely
[13:56] broke my brain a little, and I have to
[13:58] share it because it's both hilarious and
[14:01] deeply instructive. When we look at
[14:03] Strata's performance table for DeepSeek
[14:05] V4.1 flash on their reference hardware,
[14:07] the RTX 5070 PC writes four to six
[14:11] tokens a second. That's a modern 12-gig
[14:14] card with a 6-core Ryzen 5, 64 gigs of
[14:17] DDR5, and a 3.6 GB/s SSD. Now, look at
[14:21] an RTX 3060, a card from 2021 with about
[14:25] half the memory bandwidth of a 5070, and
[14:28] only 46 gigs of RAM instead of 64,
[14:31] running the same model on the same task.
[14:33] [music] And that PC writes 9 to 11
[14:36] tokens a second. So, the machine with
[14:38] the cheaper, older card is twice as
[14:40] fast. I can't stress enough how
[14:42] counterintuitive this is. I've spent
[14:44] years internalizing the idea that a
[14:46] better GPU means better AI performance,
[14:49] and here's a card from 2021 with
[14:51] objectively worse specs producing a
[14:53] faster result on the same model. The
[14:55] reason is obvious in retrospect once we
[14:57] understand it. When most of the model
[14:59] isn't on the GPU, the GPU isn't the
[15:01] bottleneck anymore. The CPU, the RAM,
[15:04] and the SSD are. And the GPU just
[15:06] finishes its share and waits. Strata's
[15:09] own model guide says it plainly, that on
[15:11] a 12-gig card, most of each token's time
[15:13] is spent waiting on the SSD and the CPU.
[15:16] The 3060 machine happened to have a
[15:18] better CPU, faster storage, or some
[15:21] combination that made the non-GPU work
[15:23] faster. And the expensive newer card had
[15:26] nothing to speed up because the work had
[15:28] moved somewhere the card couldn't reach.
[15:31] The same thing showed up in a comparison
[15:33] between a $7,770
[15:35] RTX 5090, which is the flagship, and a
[15:38] $700 used AMD data center card from 2018
[15:42] called the MI50. And both have 32 gigs
[15:45] of memory, and the 5090 is 11 times the
[15:48] price. On Deep Seek, the MI50 wrote 22
[15:51] to 23 tokens per second, while the 5090
[15:54] got about 15 to 25 depending on
[15:57] conditions. So, the 2018 server card
[15:59] from eBay matched or beat the flagship
[16:02] consumer GPU that cost nearly $8,000.
[16:06] Now, there are important caveats.
[16:08] Because they used different settings,
[16:10] the 5090 was running a longer context,
[16:13] and these were single runs on a warm
[16:15] cache. The comparison isn't perfectly
[16:18] clean, but the ballpark is real. What
[16:20] actually matters for Deep Seek's decode
[16:22] speed isn't the GPU chip, but the number
[16:25] of experts we can keep on the card, and
[16:27] that's decided by capacity, meaning
[16:29] gigabytes, not by how fast those
[16:31] gigabytes are. The MI50 kept about 2,700
[16:35] of Deep Seek's 15,360
[16:38] experts on the card, while the 5090 kept
[16:41] about 1,450
[16:43] because its owner had given a lot of the
[16:45] card's memory to a long context. And
[16:47] more experts on the card meant fewer
[16:49] trips to RAM and the SSD per token, and
[16:52] fewer trips meant faster tokens.
[16:54] >> [music]
[16:54] >> So, the lesson isn't buy a cheap card,
[16:57] it's buy the right amount of capacity
[16:59] for the tier that's your actual
[17:01] bottleneck, and stop paying a premium
[17:03] for speed in tiers that aren't. For Deep
[17:06] Seek, that means we do need a bigger
[17:08] GPU, just not an expensive one. Let me
[17:10] get concrete because, after all of that,
[17:13] what you probably want to know is what
[17:15] you can actually run on the hardware you
[17:17] already own. Strata serves two main
[17:19] models right now, and they're genuinely
[17:21] different experiences.
[17:23] Quen 3.8 flash next at 125 billion
[17:27] parameters is the one that actually
[17:29] delivers on the headline.
[17:30] >> [music]
[17:30] >> In its Q2 build, it runs at about 94
[17:33] tokens a second on the 5070 PC, which is
[17:36] noticeably fast because you ask it
[17:38] something, it thinks for a moment, and
[17:40] then it just writes. At that speed, a
[17:42] 1,000 token answer takes about 11
[17:45] seconds, and a 30,000 token coding
[17:48] prompt pre-fills in about 11 seconds as
[17:50] well. That makes it a working AI
[17:52] assistant at local speeds. The lookup
[17:54] table part of this model is 28.8 gigs
[17:57] and lives on the SSD, and the active
[17:59] experts need about 34 gigs of RAM, while
[18:02] the hot part that runs on the GPU is
[18:04] only about 3.5 gigs. [music] So, a
[18:06] 12-gig card runs it comfortably, and it
[18:09] runs fast. Deep Seek V4.1 flash is the
[18:12] 763 billion parameter one, and the
[18:15] experience there depends almost entirely
[18:17] on your RAM situation because on 64 gigs
[18:20] with 12 gigs of VRAM, we're at four to
[18:23] six tokens a second. But one user with
[18:25] 128 gigs, a 5070 TI, and a fast SSD
[18:29] average 28.8 tokens a second on the
[18:32] smallest quantization. And on a 32-gig
[18:35] card from 2018, we can hit 22 to 23. So,
[18:38] the model scales with capacity. And on
[18:41] most gaming PC setups, it lands in the
[18:43] technically works but requires patience
[18:45] category. Now, a quick word about
[18:47] quality because this matters. The
[18:49] recommended build for both models is a
[18:52] two-bit quantization, which is two bits
[18:54] per weight and the most compressed
[18:56] version that still performs well. On
[18:58] benchmark tests, the DeepSeek two-bit
[19:01] version actually hits 100% of the
[19:03] original's average on several hard
[19:05] reasoning tasks. But the caveat is that
[19:07] it might need more tokens to think its
[19:09] way to the same answer. And at 4.7
[19:12] tokens per second, thinking is the most
[19:14] expensive thing it can do. And keep in
[19:16] mind how fast Strata is still changing.
[19:19] It shipped 63 releases in 38 days. And
[19:22] some of those releases turned
[19:23] performance optimizations on and then
[19:25] off again after they caused quality
[19:27] regressions. In one case, a routing
[19:30] shortcut was added for 12-gig Nvidia
[19:32] cards that made code generation 37%
[19:35] faster. But users reported it repeating
[19:38] itself in long sessions. And when the
[19:40] team checked, they found it failed 4.5
[19:43] out of 10
[19:43] >> [music]
[19:43] >> agent tasks instead of the normal 5.6.
[19:46] So, they turned it off 2 days later.
[19:48] That's not a criticism. It's just what
[19:50] real open-source development looks like
[19:52] at this speed. But it does mean the
[19:54] number you saw benchmark 2 weeks ago
[19:56] might be from a setting that no longer
[19:58] exists in the same form.
[20:00] And now the part I kept not wanting to
[20:02] say out loud because it kind of
[20:04] undercuts the whole premise of this
[20:05] video. But I think you deserve to hear
[20:07] it. If you specifically want to run
[20:09] DeepSeek V4.1 flash and you're on a
[20:11] 12-gig card with 64 gigs of RAM, just
[20:14] rent it. DeepSeek's own API charges 60
[20:17] cents per million output tokens off-peak
[20:20] and $1.20 at peak. The DDR5 kit you'd
[20:24] buy to run this model costs about
[20:26] $1,200.
[20:28] And at the off-peak API price, that
[20:30] $1,200 buys 2 billion output tokens. At
[20:34] 4.7 tokens per second, a local setup
[20:37] would need about 13 and 1/2 years of
[20:39] non-stop writing to produce 2 billion
[20:41] tokens. And even at the peak API price,
[20:44] it's still almost 7 years. And the API
[20:47] is also running the real model, not the
[20:49] 2-bit version using five of its six
[20:51] experts. I'm not telling you this to be
[20:53] discouraging. I'm telling you because
[20:55] the community conversation sometimes
[20:57] gets so focused on whether something can
[20:59] run locally that it skips right past
[21:01] whether it should. The exception, and
[21:04] it's a real one, is privacy. If your
[21:06] code can't leave your machine, if you're
[21:09] under a client contract, or if you're
[21:10] working with a code base that can't
[21:12] touch an external API, none of that math
[21:15] applies, and local is the only option,
[21:18] so cost per token is irrelevant. For
[21:20] everyone else, the question is the same
[21:22] as it's always been. Spend on capacity
[21:24] in the fastest tier you can afford per
[21:26] gigabyte, skip the newest chip, and
[21:29] match the hardware to the model's actual
[21:31] access patterns.
[21:32] A 32-gig card from 2018, chosen for the
[21:35] right reasons, got further on Deep Seek
[21:37] than a 12-gig card from this year.
[21:40] That's a practical conclusion rather
[21:41] than the headline, but it's the one that
[21:43] tells us where to actually put our
[21:45] money. Since RAM is the variable that
[21:47] matters most right now, I sorted the
[21:49] practical breakdown by what you might
[21:50] already own. Because the last thing we
[21:52] want is to buy hardware and then find
[21:54] out we didn't need to.
[21:55] If you have 16 gigs, Stratosphere can
[21:58] load Qwen 3.8 Flash Next in a low RAM
[22:01] mode and pull experts off the SSD. One
[22:03] developer measured that at about eight
[22:05] tokens a second on a 3060 with a single
[22:08] 16-gig stick, which isn't fast, but it
[22:11] works. And for learning, tinkering, or
[22:14] occasional use, it's real. There's also
[22:16] a community fork called Battle Juice
[22:18] that one developer built to squeeze more
[22:20] out of this configuration, and they
[22:22] reported 22 sustained tokens per second
[22:25] on the same box with a different
[22:27] quantization. It's a one-person project
[22:30] from recently and it has trade-offs, but
[22:32] the direction it points is clear.
[22:34] Engines are getting better at needing
[22:35] less RAM, so more of the model can move
[22:38] to that 13 cent per gigabyte SSD. If you
[22:41] have 32 gigs, you're in a sweet spot for
[22:43] Qwen. And the Reddit post with almost
[22:45] 900 upvotes ran the Q2 build on a laptop
[22:48] with an 8-gig card and 32 gigs of DDR5
[22:51] and got up to 30 tokens a second. Strata
[22:53] also ships a coder build that keeps 256
[22:56] of each layer's 512 experts and needs
[22:59] about 30 gigs. Or there's Qwen 3.635B,
[23:03] the smaller cousin, which Strata
[23:05] measured at 59.7 tokens per second on a
[23:08] 3060. So at 32 gigs, we have real, fast,
[23:12] local AI options. If you have 64 gigs,
[23:15] you're Strata's target user because
[23:17] every Qwen 3.8 flash next build fits
[23:20] comfortably. And Deep Seek runs, too.
[23:22] Slowly on a 12-gig card, but it runs.
[23:25] And on a bigger card, it becomes
[23:26] genuinely useful. And if you bought this
[23:29] RAM a year or two ago, congratulations
[23:31] because those 64 gigs are now worth
[23:34] significantly more than what you paid
[23:36] for them, and Strata [music] is arguably
[23:38] the best use they've ever had. If you
[23:40] have 128 gigs or more, Deep Seek starts
[23:43] to make real sense. And one owner with a
[23:46] 5070 Ti, a high-end Ryzen, and 128 gigs
[23:50] averaged 28.8 tokens a second on the
[23:53] smallest quantization with a 4-bit KB
[23:55] cache. And when it's spilled onto the
[23:57] SSD, it dropped to 19, [music]
[23:59] which is still more than four times what
[24:01] a 12-gig card gets. So at that size,
[24:04] Deep Seek becomes an actual coding
[24:06] assistant rather than a patience test.
[24:08] And if you're thinking about buying RAM
[24:10] right now, check DDR4 prices first. At
[24:12] about $7.80 per gigabyte against DDR5's
[24:16] $19, the same money buys more than twice
[24:19] the capacity. We do lose bandwidth,
[24:21] which matters, [music]
[24:22] but if the choice is between 32 gigs of
[24:24] DDR5 and 64 gigs of DDR4 for the same
[24:28] price, the extra capacity wins for these
[24:30] workloads because the bottleneck is
[24:32] usually capacity and not speed. So, do
[24:35] you need an expensive GPU anymore?
[24:38] Strata genuinely moved the answer
[24:40] because a 125 billion parameter model
[24:42] running at 94 tokens a second on a 12
[24:45] gig card from 2021 is not something that
[24:48] was true before. And the fact that I can
[24:50] run quant 3.8 flash next on my machine
[24:53] right now, today, without buying
[24:55] anything, and have a fast local AI
[24:57] assistant
[24:58] >> [music]
[24:58] >> is new and really is worth something.
[25:01] The bigger model, DeepSeek, is more
[25:03] complicated. We can run it on a 12 gig
[25:05] card, but we have to be honest about
[25:07] what that experience looks like on that
[25:09] card at this moment with this hardware.
[25:12] Where for some workloads it's fine and
[25:14] for others we'll spend more time waiting
[25:16] than working. What Strata actually did
[25:18] is shift the bottleneck, where the GPU
[25:21] stopped being the thing we had to spend
[25:22] on and RAM became the thing we have to
[25:24] spend on. And since RAM got six times
[25:27] more expensive this year, the price
[25:28] didn't leave, it just moved. But the
[25:31] direction Strata is moving in is right
[25:33] because every release gets more of the
[25:35] model onto SSDs at 13 cents a gigabyte
[25:37] and squeezes more out of less RAM.
[25:40] And the developer's own PC is a $300
[25:42] range used card and a mid-range CPU, so
[25:45] they're optimizing for the hardware most
[25:47] people actually own. Before you buy
[25:49] anything for this, make a simple list of
[25:51] what GPU you have and how many gigs,
[25:54] what RAM you have and whether it's DDR4,
[25:56] DDR5, and what SSD you have. And then
[26:00] look at what Strata's actual performance
[26:02] tables say for your tier. Don't buy
[26:04] based on the number that went viral
[26:06] without checking which operation that
[26:08] number measured. And don't buy a faster
[26:10] card when the bottleneck is your RAM.
[26:12] And don't buy more RAM when the model
[26:14] you actually want to run fits in what
[26:16] you already have. The expensive GPU
[26:18] really did stop being the price of
[26:20] entry, and the only problem is that the
[26:22] part that replaced it now costs almost
[26:24] as much per gigabyte, which is a much
[26:26] more interesting problem to have. If you
[26:28] found this useful, the like button is
[26:30] right there and it genuinely helps. And
[26:32] if you want more videos where we
[26:33] actually read the docs instead of just
[26:35] reading the tweets, subscribe, and
[26:37] you'll see the next one. And let me know
[26:38] in the comments what GPU and how much
[26:40] RAM you're running. I'm curious what
[26:42] setup most people watching this actually
[26:44] have, because I think it might be
[26:45] different from what most of the online
[26:47] discourse