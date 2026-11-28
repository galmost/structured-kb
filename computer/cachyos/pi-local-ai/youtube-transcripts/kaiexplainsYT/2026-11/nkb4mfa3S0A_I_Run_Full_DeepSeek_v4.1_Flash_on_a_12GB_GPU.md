[00:00] Okay, I think you've been here before.
[00:02] You saw the Reddit post where someone
[00:04] ran DeepSeek, the actual 500 GB monster,
[00:07] on a regular gaming GPU, which was a
[00:09] 5-year-old card with 12 gigs of VRAM.
[00:12] And you got excited, stayed up too late,
[00:15] followed the guide, and downloaded the
[00:16] files. Then you read the fine print
[00:19] where somebody in the comments said,
[00:20] "Oh, this isn't the real model. It's the
[00:23] two-bit version. It's basically a
[00:24] lobotomy." And you sat there at 2:00
[00:27] a.m. staring at a progress bar asking
[00:29] yourself whether this thing is even
[00:31] thinking or whether it's just doing a
[00:32] really confident impression of thinking.
[00:35] I've been there more than once, and I
[00:37] want to talk about that feeling today
[00:39] because I think it's the wrong question.
[00:41] But we have to understand why it's the
[00:42] wrong question before we can get to
[00:44] what's actually happening here. And
[00:45] something genuinely new happened this
[00:47] week where a developer named Ryan Flavel
[00:50] released an engine called Promethevs
[00:52] that claims to run the full DeepSeek
[00:54] v4.1 flash, all 510 GB of it, on a 12 GB
[01:00] graphics card. And the moment I saw that
[01:02] headline, I had two thoughts in rapid
[01:04] succession, where the first was, "No
[01:06] way." And the second was, "Wait, what
[01:08] does full even mean?" And it turns out
[01:10] that second question is the one that
[01:12] changes everything. So, what's up,
[01:14] everyone? And this video is going to go
[01:16] a little differently from the usual
[01:17] model speed and benchmark format. And I
[01:20] think there's a much more interesting
[01:22] conversation underneath all of that, and
[01:24] it gets skipped in almost every video
[01:26] about running DeepSeek locally. That
[01:28] conversation is about what a word And I
[01:31] don't mean in money, though we'll get to
[01:33] that, too, and the numbers will surprise
[01:34] you, but what it costs your PC in
[01:37] gigabytes every single time the model
[01:39] writes one token. Once you understand
[01:41] that number, everything else clicks into
[01:44] place, from the speeds and the tradeoffs
[01:46] to the debates about full versus fake
[01:48] and the recommendations at the end. So,
[01:50] let's build up to it properly, and at
[01:52] the very end, we'll also look at whether
[01:54] this is even worth the bother or whether
[01:56] 11 bucks a month does the job instead.
[01:58] Let me start with my own specific
[02:00] because I think you've had a version of
[02:02] it, too. A few weeks back, I saw the
[02:04] launch post from Daz Lab, which is a
[02:06] research lab in Austria, saying you
[02:08] could run a 763 billion parameter model
[02:12] on a 12 GB GPU.
[02:14] That post got seen about 186,000
[02:17] times, and I was not immune to the hype.
[02:20] So, I followed the Strata installer,
[02:22] which was one line of terminal and
[02:24] incredibly smooth, and it worked. And
[02:26] then I actually used it for something,
[02:28] and that's where the crack started
[02:29] showing. The speed was fine for casual
[02:32] use, and the answers felt good, mostly,
[02:35] but there was something in the back of
[02:36] my head that wouldn't let it go, because
[02:38] every couple of responses, something
[02:40] would feel slightly off, like the model
[02:42] was just barely missing the punchline of
[02:44] a joke it was trying to tell. It was
[02:46] coherent, and it was responsive,
[02:48] but it had this subtle quality of a
[02:50] person recounting a movie they saw once
[02:53] 6 months ago, where the vibe is right
[02:56] and the details are wrong. And then the
[02:57] comments started, saying this isn't a
[02:59] real model, it's a lobotomized copy, and
[03:02] the 2-bit compression throws away half
[03:04] the information. Now, I know internet
[03:07] comments aren't a peer-reviewed journal,
[03:09] but they planted a seed. So, when Ryan
[03:11] dropped Prometheus with the words "full
[03:13] model, no shortcuts", I genuinely
[03:16] stopped what I was doing. And what took
[03:18] me a bit to work out is that the debate
[03:20] everyone was having was using the wrong
[03:22] unit. It was never really about full or
[03:24] fake, it was about bytes per word. And
[03:27] to understand why, we have to look at
[03:29] what Deep Seek actually shipped. Okay,
[03:32] this next part made me go back and stare
[03:34] at a wall for a minute. Everyone in the
[03:36] 2-bit debates talks about the full model
[03:38] like it's some pristine, uncompressed,
[03:41] 16-bit floating-point behemoth sitting
[03:44] on a server farm, and the compressed
[03:46] version is a pale shadow of that, which
[03:49] is the implied story. But, if we go open
[03:51] Deep Seek's own config file on Hugging
[03:53] Face, the quantization section says the
[03:56] dense weights ship as FP8, and the
[03:59] expert weights, which are the most
[04:01] important part, ships as FP4, which is 4
[04:04] bits.
[04:05] That's the release, meaning it's what
[04:07] DeepSeek itself ships and what that API
[04:09] serves. So, the full model is already
[04:11] 4-bit. Let me put some numbers on this
[04:14] to make it land. Now, 763 billion
[04:17] parameters at 16 bits would be 1,526
[04:21] GB, which is not a file you're
[04:23] downloading on any internet connection
[04:25] that exists in a residential building.
[04:27] And DeepSeek ships the experts at 4
[04:29] bits, which brings the expert weights
[04:31] alone to about 288.8 GB from 15,360
[04:36] experts at about 18.8 MB each. Then we
[04:40] add another 196 gigs for a lookup
[04:42] structure called N-gram, and there are
[04:44] 25 or so gigs for everything else, like
[04:46] the attention layers, the draft head,
[04:49] and the vision components. So, we end up
[04:51] at 510 gigs. So, the real gap isn't 16
[04:54] bits versus two, it's 4 bits versus two
[04:57] on the part that makes up most of the
[04:59] file. In other words, the compressed
[05:01] models keep half the bits DeepSeek
[05:03] itself chose for its experts. That's a
[05:06] real difference, but it's not the
[05:08] difference the debate implies. And this
[05:10] reframing matters enormously for what
[05:12] comes next. Now, the number that runs
[05:15] everything starts with the shape of the
[05:17] model. DeepSeek has 40 layers, and each
[05:20] layer has 384 experts. And when the
[05:22] model writes a word, any word at all,
[05:25] whether it's the or mitochondria, each
[05:27] layer picks six of those experts to
[05:29] handle it. So, 240 experts touch every
[05:33] single token the model produces. At 18.8
[05:36] MB per expert * 240 experts, every word
[05:40] costs about 4.5 GB of expert weights,
[05:44] and that's for one single word. And your
[05:46] graphics card, the 12-gig one, is the
[05:48] fastest storage in your system. But
[05:51] we're asking it to serve 4.5 GB of
[05:54] expert weights for every single token,
[05:56] while it only holds 12 gigs of anything
[05:58] at all. So, you can probably already
[06:00] feel the math starting to strain. Now,
[06:02] Prometheus stores a 2-bit copy of each
[06:04] expert at about 11.5 megabytes instead
[06:07] of 18.8. So, a word on Prometheus's
[06:10] costs about 2.8 gigabytes. And Strata's
[06:13] 2-bit files are even smaller at about 9
[06:15] megabytes per expert, which puts a word
[06:17] at around 2.1 gigabytes and 1.8 when it
[06:21] drops to sixth expert. The other
[06:23] structure, engram, barely factors in
[06:25] because each word only reads a few rows
[06:28] of it, so it can sit happily on your SSD
[06:30] without causing any trouble. Now, this
[06:33] is where the hardware setup gets
[06:34] humbling. Ryan's reference machine is a
[06:36] Ryzen 9 3950X with 64 gigs of RAM, the
[06:40] RTX 3060, and two crucial NVMe drives.
[06:43] And on that machine, the graphics card
[06:45] holds about 78 of the most used experts
[06:48] at any time out of 15,360,
[06:51] which is 0.9 gigabytes on the card and
[06:54] half a percent of the model. Engineers
[06:56] call this memory bound. But the more
[06:58] useful name for what we're doing here is
[07:01] bytes per word because that's the bill
[07:03] your PC pays for every token the model
[07:05] writes. And while the graphics card is
[07:07] the fastest shelf in the building, it
[07:09] only holds half a percent of the
[07:11] inventory. So, how fast is fast enough?
[07:14] That question is a personal one, so
[07:16] let's put real numbers on it. Ryan
[07:18] measured the actual full weights,
[07:20] meaning the original FP4 experts with no
[07:22] compression and no tricks, on the
[07:24] reference machine and got 2.14 tokens
[07:27] per second on a 12-gig card. And that
[07:29] lines up with the math. The two NVMe
[07:32] drives read together at up to 9.9
[07:34] gigabytes per second, and at 4.5 gigs of
[07:37] weight per word, that comes out to about
[07:39] 0.45 seconds per word, or 2.2 words per
[07:42] second. So, the measured number lands
[07:44] almost exactly where it should. One
[07:46] person in the comments went further and
[07:48] ran the native FP4 checkpoint on an RTX
[07:51] 5060 with 8 gigabytes and 31 gigs of
[07:53] RAM, and they got about 1.6 tokens per
[07:56] second straight from a PCIe 5 drive and
[07:59] 2.4 tokens per second with a RAM cache.
[08:01] Now, that's one comment and not a full
[08:04] benchmark, but the numbers line up with
[08:05] everything else. So, let's be real,
[08:07] about 2.14 tokens per second, which is
[08:10] one word roughly every half second.
[08:13] For a 300-word paragraph, that's about 2
[08:15] and 1/2 minutes of watching the cursor
[08:16] blink. And for anything that involves a
[08:18] chain of reasoning, which is the kind of
[08:20] thinking where Deep Seek is actually
[08:21] impressive,
[08:22] you might be watching that cursor for a
[08:24] very, very long time. Now, compare that
[08:27] to Strata, where the 2-bit file with
[08:29] fewer bytes per word runs at about 4.7
[08:32] tokens per second on a 5070
[08:34] with 64 gigs of RAM and a decent drive.
[08:37] And if we divide that by 2.14, we get
[08:39] 2.2 times faster on roughly half the
[08:42] bytes per word. So, the math checks out,
[08:44] and speed really does track bytes. The
[08:47] weird outlier in Strata's docs is a 3060
[08:50] with only 46 gigs of RAM showing 8 to 10
[08:53] tokens per second, which the docs don't
[08:55] explain, and I'm not going to explain
[08:57] either. So, please don't go buy a 3060
[09:00] based on that line. When we look at
[09:01] real-world results from people who
[09:03] aren't the developers, the picture is a
[09:05] lot slower. AI Receipts got 1.84 tokens
[09:09] per second on a 5070 with 32 gigs,
[09:12] and No Place Like Localhost got 2.8 on a
[09:15] 4070 with 128 gigs, then added a 24-gig
[09:19] card and got to 4.7.
[09:22] And on that setup, a single coding
[09:24] question took 11 minutes and 30 seconds.
[09:26] And I want you to hold that number in
[09:28] your head for later. Okay. So, if the
[09:30] fine-weights do 2.14 tokens per second,
[09:34] how does Prometheus claim seven? This
[09:36] part is genuinely clever, and it's where
[09:38] I went from skeptical to actually
[09:40] impressed.
[09:41] Ryan calls the method compress, then
[09:44] correct. Every word is computed first on
[09:46] the 2-bit copy of the experts, which is
[09:49] the fast pass on the cheap bytes.
[09:51] Then the engine looks at how confident
[09:53] the model was by measuring the gap
[09:54] between the top two candidate words. And
[09:57] if that gap is small, closer than a
[09:59] threshold of 0.45,
[10:01] the model wasn't sure, and that word
[10:03] gets flagged.
[10:04] For a flagged word, the engine does
[10:06] something interesting, because it has
[10:08] stored correction data alongside the
[10:10] two-bit copy, which is enough to
[10:12] reconstruct the full precision FP4
[10:14] experts from the compressed version. So,
[10:16] it rebuilds those experts, recomputes
[10:18] the word, and keeps whatever the full
[10:20] weights actually pick. And an overturned
[10:22] word costs 2.6 to 3.2 extra seconds,
[10:26] which is the correction tax. Now, at
[10:28] this point, you're probably thinking
[10:30] that this handles accuracy, but
[10:32] corrections are slow. So, how do we get
[10:34] from two tokens per second to seven? And
[10:36] the second half of the trick is the part
[10:38] I think is actually beautiful.
[10:40] DeepSeek ships a small draft head inside
[10:42] the model itself, which is a component
[10:44] DeepSeek put in the box and not
[10:46] something Ryan invented. It guesses the
[10:48] next four words, and the engine checks
[10:51] all four of them in one single pass over
[10:53] the experts. So, you get four words for
[10:55] the price of one pass. In one code run
[10:58] that Ryan logged, 122 out of 129 guesses
[11:03] were accepted, which is a 94.6%
[11:06] acceptance rate. With each round
[11:08] committing an average of 4.13 words at
[11:11] once. So, instead of paying 4.5 GB of
[11:14] expert reads per word, we're paying 4.5
[11:17] GB per four words. The effective cost
[11:20] per word drops to about 1.1 GB, which is
[11:23] what gets you to seven tokens per
[11:25] second. And so, the 12 gig card was
[11:27] never really the lever here, because the
[11:29] lever was the draft head the whole time.
[11:32] This is the part of the video where I'm
[11:33] going to be honest with you, even when
[11:35] the numbers get a little uncomfortable.
[11:37] Prometheus published its accuracy audit,
[11:39] and across 960 words on three different
[11:42] prompts, the two-bit copy alone, before
[11:44] any corrections, picked the same word as
[11:47] the full model 97.4%
[11:50] of the time. That's 25 words different
[11:52] out of 960, and after corrections, it
[11:55] climbed to 98.33%.
[11:58] Now, those numbers sound impressive, and
[12:00] they kind of are. But, I want us to slow
[12:02] down for a second here, because there's
[12:04] a subtlety that matters. That 97.4%
[12:08] is per word, measured against the full
[12:10] model's output one word at a time, and
[12:13] assuming everything before it matched.
[12:15] But, real generation doesn't work that
[12:17] way.
[12:18] Once one word comes out differently,
[12:20] every word after it is computed on a
[12:22] different sentence, so the divergence
[12:25] compounds. And the second person to
[12:27] install Prometheus checked exactly this
[12:29] with the same engine, the same prompts,
[12:31] and greedy decoding, so nothing random.
[12:34] On an agent prompt, their answer matched
[12:36] word for word only up to word four out
[12:38] of 56. And on a code prompt, it matched
[12:40] up to word on one pass and word two on
[12:43] another. And on that one machine, the
[12:45] streamed answer and the non-streamed
[12:47] answer came out different from each
[12:49] other. But, none of that means the
[12:51] answers were worse. It just means nobody
[12:53] can confirm they got the full model's
[12:55] answer by comparing the text, because
[12:57] this engine doesn't write the same text
[12:59] twice. The two-bit copy and the full
[13:01] model mostly agree on the next word, but
[13:04] they'll still write two different
[13:05] essays. Now, compare that to Strata's
[13:07] measurement, where its two-bit file
[13:09] picks the same top word as the original
[13:11] 83.7% of the time, and the 2.25-bit
[13:15] version gets to 87.2%.
[13:18] And perplexity, which measures how
[13:19] surprised the model is by real text,
[13:22] rises 15.5%
[13:24] on the two-bit file. And the rise is
[13:26] worse on regular text and somewhat
[13:28] better on code and agent tasks. There
[13:30] was one real side-by-side, where AI
[13:33] Receipts gave the local two-bit copy the
[13:35] same car racing prompt they'd given Deep
[13:37] Six API. Two blind reviewers scored the
[13:40] cloud response 10 out of 12, and the
[13:42] local response two out of 12. That's one
[13:45] test with thinking off and faster mode
[13:47] on, so take it with salt. But, it points
[13:49] in the same direction as everything
[13:51] else. Now, this is my favorite part of
[13:54] the whole story, and I think it says
[13:56] something important about how we should
[13:57] actually evaluate this stuff. Since Ryan
[13:59] dropped Prometheus, two people outside
[14:02] the original build have reported real
[14:04] installs. The first one, on November
[14:06] 3rd, had a Ryzen 7950X3D
[14:09] with 192 192 gigs of DDR5 RAM and two
[14:13] RTX 3090s, which is three times the RAM
[14:17] and four times the graphics memory of
[14:18] the reference build.
[14:20] The result was 3.10 tokens per second on
[14:23] code and 0.49 on reasoning.
[14:26] But the engine used just one of the two
[14:27] cards and RAM usage stayed at 67 gigs.
[14:31] So, all of that extra hardware got the
[14:32] same speed. The second install on
[14:34] November 5th was more interesting. With
[14:37] an RTX 4090, an i9, 64 gigs of DDR5, and
[14:42] a PCIE 5 drive, and its stock settings
[14:44] it got 2.66 tokens per second on code
[14:48] and 1.20 on reasoning. And the install
[14:50] verification check failed. So, they dug
[14:53] into it and it turned out the engine
[14:55] fills the graphics card with hot experts
[14:58] and by default leaves only 384 megabytes
[15:01] free. Well, that same card is also
[15:03] driving the desktop, so the display was
[15:06] fighting the model for VRAM and the
[15:08] model was losing bites of cash on every
[15:10] frame. They reserved 3,000 megabytes of
[15:13] graphics memory instead, which is a
[15:15] one-line setting, and pinned the engine
[15:17] to the performance cores. And code went
[15:19] from 2.66 to 9.75 tokens per second,
[15:23] reasoning went from 1.20 to 5.23, and
[15:27] corrections dropped from 5 to 7 seconds
[15:29] each to about 1 second. So, that's 3.7
[15:32] times faster from changing one number,
[15:34] which means the hardware was fine the
[15:36] whole time and the default was the bug.
[15:39] If your graphics card is also your
[15:40] display driver, which it is on most
[15:42] gaming PCs, that setting is aimed
[15:45] directly at you.
[15:46] The second install found it by filing
[15:48] issue number seven on the GitHub. So,
[15:51] one stranger and one GitHub issue got
[15:53] that whole gain. This is why I always
[15:55] say to wait two weeks before making a
[15:57] verdict on any new local AI tool. And
[16:00] the bugs that matter are rarely in the
[16:02] model and they're usually sitting in the
[16:04] defaults. There's one more number I want
[16:06] to put in front of you because it
[16:07] doesn't come up enough in the speed
[16:09] comparisons. Everything we've talked
[16:11] about so far is writing speed, meaning
[16:13] tokens per second once the model is
[16:15] rolling. But before the first word, the
[16:18] model has to read your prompt. And on a
[16:20] 1,163
[16:22] token prompt, Prometheus' first word
[16:24] arrives after about 126 seconds of
[16:27] pre-fill, which is two full minutes of
[16:29] your life before the cursor starts
[16:31] moving. Follow-up messages in the same
[16:33] conversation start in about 2 seconds
[16:35] because the engine keeps what it already
[16:37] read, and that part is genuinely good.
[16:40] But, now think about A Gentic work for a
[16:41] second. No place like Local Hosts one
[16:44] open code question used about 9,100
[16:47] tokens of context, and at 9.2 tokens per
[16:51] second of pre-fill, we're looking at
[16:52] approximately 16 minutes before the
[16:54] first word if that rate holds. But,
[16:56] Strata reads much faster at up to 231
[17:00] tokens per second at an 8K context on
[17:02] the 5070, so the same prompt takes about
[17:05] 39 seconds with Strata. And this is also
[17:08] where those 100 tokens per second on a
[17:10] 12 gig card posts came from. But, that
[17:13] was the reading speed, and the writing
[17:15] speed was 4.7, which is a very different
[17:17] thing. So, what's the context window,
[17:19] too? Strata's deep seek defaults to
[17:22] 8,192
[17:23] tokens, and that one open code question
[17:26] needed 9,100,
[17:28] so the default wouldn't have held it.
[17:29] Let me put the full price of Prometheus
[17:31] on the table because it's part of the
[17:33] conversation, too.
[17:34] Prometheus needs about 1,009 GB of
[17:37] storage, roughly 1.08 TB, which covers
[17:40] deep six raw weights, the 2-bit copies,
[17:43] the correction layers, the FP4 copies,
[17:46] and mirrors so both drives can read in
[17:48] parallel. Strata needs 257 gigs, so
[17:52] Prometheus needs 4.2 times more disk.
[17:55] It's Windows only, and it supports one
[17:57] Nvidia RTX 30 or 40 series card, which
[18:00] means no RTX 5070, no AMD, and no Mac.
[18:04] And it answers one request at a time.
[18:07] The build on Ryan's PC took about 4
[18:09] hours, and a 2 TB NVMe drive was running
[18:12] around $300 as of November 1st. And all
[18:15] of that, the terabyte, the Windows
[18:17] lock-in, the 4-hour build, and the 300
[18:20] bucks moves you from 83.7%
[18:23] to 97.4%
[18:25] top order agreement before corrections
[18:27] and to 98.33%
[18:30] after. Nine words corrected out of 960
[18:33] is what the full setup buys over the
[18:34] best two-bit alternative. Whether that
[18:36] trade is worth it genuinely depends on
[18:38] who you are. Okay, I've been building to
[18:40] this, so I'll deliver it straight. Deep
[18:42] Seek's own API serves v4.1 flash, the
[18:45] same model version, at 60 cents per
[18:48] million output tokens off-peak and $1.20
[18:51] at peak. Now, take Promethius at its
[18:53] best case of 7.4 tokens per second and
[18:56] run it every second of every hour of a
[18:58] full 30-day month, and that gets you
[19:00] 19.2 million tokens, which at the
[19:03] off-peak API price is $11.51
[19:06] for the whole month or $23 at peak. And
[19:09] that's the price of running that PC
[19:11] absolutely flat out at peak performance
[19:13] for a whole month priced in API calls
[19:16] before we even count electricity. And
[19:18] Open Code Go, which is a $10 monthly
[19:20] subscription, includes $100 worth of
[19:23] Deep Seek v4.1 flash at Deep Seek's own
[19:26] prices. And $100 at 60 cents per million
[19:30] is 166.7
[19:32] million output tokens, which is 8.7
[19:35] months of that PC running non-stop at
[19:37] its best. The card racing game that AI
[19:40] Receipts ran locally took 2 hours and 7
[19:42] minutes for 13,316
[19:45] tokens, and on the API, that's less than
[19:47] 1 cent, which goes to show the full
[19:49] model is cheapest when someone else's PC
[19:51] is the one moving the bytes. I'm not
[19:53] saying that to dismiss local inference
[19:55] because I genuinely love local inference
[19:57] and I think it matters, but I'm saying
[19:59] it because the cost framing changes the
[20:01] conversation from whether we can do it
[20:04] to why we'd want to.
[20:06] Now, there's one buyer for whom all of
[20:08] that API math is completely irrelevant,
[20:11] and I want to talk about them
[20:12] specifically. If your prompts can't
[20:13] leave the building because you're in
[20:15] finance, healthcare, legal, defense, or
[20:18] any space with real data privacy
[20:20] constraints, the API was never an option
[20:23] because Deep Seek's API runs on Deep
[20:25] Seek's servers and as AI receipts put it
[20:28] in a reply, nobody can change the rules
[20:30] on a model sitting on your own drive.
[20:32] So, for that buyer, a slow model on a
[20:35] local drive beats a fast model they're
[20:37] not legally allowed to use, which makes
[20:39] the calculus different and the slowness
[20:41] is a feature rather than a bug because
[20:43] the alternative is not at all.
[20:45] Then there's the other end with a 4090,
[20:48] 64 gigs of DDR5 and a PCIE5 drive.
[20:52] With that one setting changed, 9.75
[20:55] tokens per second on code is not a stunt
[20:58] and that's genuinely usable and it's
[21:00] faster than I read when I'm tired. And
[21:02] with 128 gigs of RAM or more, there's
[21:05] another option in Anisloth's lossless
[21:08] 508 gig build, which runs in plain
[21:10] llama.cpp and got merged on October
[21:13] 25th. So, there's no new engine to
[21:15] install, no Windows lock-in, and no
[21:18] terabyte of correction data. All right,
[21:20] so to wrap this up with something you
[21:21] can actually act on, the starting point
[21:24] is your RAM and not your GPU or your
[21:26] CPU. With 32 gigs, don't because AI
[21:30] receipts measured 1.84 tokens per second
[21:33] in a real benchmark and a 64 gig DDR4
[21:36] kit is about $500 right now, which is 50
[21:39] months of Open Code Go, so spend the $10
[21:41] on the subscription. With a 12 gig card
[21:44] and 64 gigs of RAM, run Stratus 2-bit
[21:46] file. When you set it up, switch on full
[21:49] quality mode so it uses all six experts
[21:51] instead of five, push the context window
[21:53] above 8K, and turn thinking mode off for
[21:56] quick jobs. That setup is fast and it's
[21:58] proven, it's been tested by a lot of
[22:00] people, and it's honest about what it
[22:01] is. On Windows with an RTX 30 or 40 card
[22:05] and a free terabyte and a real wish to
[22:07] contribute to something, run Prometheus.
[22:10] But set the graphics memory reserve
[22:11] before benchmarking anything and if the
[22:13] card drives the display, reserve at
[22:15] least 3 gigs. And then file the results
[22:18] on the GitHub because they've had two
[22:19] external installs report and a third
[22:21] genuinely helps. On a Mac with 64 gigs
[22:24] of unified memory, Strata has a deep
[22:26] seat built, too. And if you get paid for
[22:28] your output, use the API where it's full
[22:31] weights on someone else's power bill for
[22:33] under a dollar on most tasks.
[22:35] And the thing I keep coming back to
[22:36] after going through all of this is that
[22:38] the conversation about full or fake was
[22:41] never really about accuracy. It was
[22:43] about trust. When we're waiting 2
[22:45] minutes for the first word and then 11
[22:47] minutes for the first answer, we want to
[22:49] know the wait was worth it and that the
[22:51] model was actually thinking and not
[22:53] doing a compressed approximation of
[22:55] thinking.
[22:56] So, is the compression question real? It
[22:58] is, but the gap is narrower than the
[23:00] debate implies because Deep Seek shipped
[23:02] a 4-bit model, the 2-bit copies keep
[23:05] half of that, and Prometheus tries to
[23:07] recover most of the difference with
[23:08] corrections. How much of the difference
[23:11] it actually recovers in practice, on
[23:13] your prompts and on your hardware, is
[23:15] something you'd have to test yourself.
[23:17] What I can say for sure is that bytes
[23:18] per word is the number that runs
[23:20] everything, and speed, accuracy,
[23:23] storage, and every trade-off downstream
[23:26] from how many gigabytes the PC has to
[23:28] move every time the model writes a word.
[23:30] Once we see the problem that way, we
[23:32] stop asking whether this is a real model
[23:34] and start asking what the right bytes
[23:36] per word is for our use case, and that's
[23:38] a question we can actually answer. If
[23:40] you try any of these setups, I really
[23:42] want to hear how they go. Drop your
[23:44] hardware in the comments with the card,
[23:47] the RAM, and the drive speed, and what
[23:49] you actually got because the more data
[23:51] points we have, the better the picture
[23:53] gets for everyone. And if this helped
[23:55] you cut through the noise, subscribe
[23:57] because that's the whole goal of this
[23:58] channel, and I'll see you in the next