[00:00] So I have a Mac Studio on my desk, which
[00:02] cost more than my first car. And a few
[00:05] weeks ago, I opened Claude Code and told
[00:07] it to go and research a few different
[00:08] modules while I grabbed the coffee,
[00:10] because the whole point of a setup like
[00:11] this is that the AI does the work and I
[00:13] come back to finished code.
[00:15] And when I came back five minutes later,
[00:17] nothing had happened. The cursor was
[00:19] still spinning and the terminal was
[00:21] still blinking. My local model, running
[00:23] on my own machine, which is the whole
[00:25] reason I went down the local AI rabbit
[00:26] hole in the first place, was doing
[00:28] basically nothing useful. So I'm
[00:30] standing there with my coffee going
[00:32] cold, wondering what on earth is going
[00:34] on. Now, when we look at what was
[00:36] actually happening,
[00:38] Claude Code had fanned out four sub
[00:40] agents to work in parallel, and all four
[00:43] of them sent a request to my local model
[00:45] at the same time.
[00:46] And my model was running on Ollama,
[00:48] which every YouTube video, Reddit
[00:51] thread, and blog post had told me was
[00:53] the best choice. It was answering those
[00:55] four requests one at a time in a queue,
[00:58] like it was the DMV. So sub agent one
[01:01] was working while sub agents two, three,
[01:03] and four sat there waiting and burning
[01:06] time. And that is when I went digging.
[01:08] And what I found genuinely surprised me,
[01:11] because it isn't what any of the popular
[01:12] comparisons will tell you. So what are
[01:14] all of those Ollama versus LM Studio
[01:17] videos actually measuring? The wrong
[01:19] thing. And I am going to show you
[01:21] exactly what I mean. So the question for
[01:23] this video is a specific one. If you are
[01:25] using an AI coding agent like Claude
[01:28] Code, Open Code, or anything else that
[01:30] fans out sub agents, which app should be
[01:33] running your local model on your Mac?
[01:35] And once we understand what is actually
[01:37] happening under the hood, the answer
[01:39] isn't even close. But we are going to
[01:41] get there the right way by looking at
[01:43] the evidence first, then walking through
[01:45] the mechanism, and then working out a
[01:47] real verdict for each kind of Mac.
[01:50] Now, most of us have watched at least
[01:52] one Ollama versus LM Studio comparison,
[01:55] and they usually follow the same format.
[01:57] Somebody opens both apps, types the same
[02:00] and sees which one answers faster.
[02:02] Sometimes it's a document summary and
[02:04] sometimes it's a coding task. And at the
[02:06] end, they show the tokens per second and
[02:08] one app wins by a little. And those
[02:10] tests are not wrong. They are just
[02:12] testing a world that most of us don't
[02:14] live in anymore. The best one I have
[02:16] seen comes from a creator called The
[02:18] Dark Factory, who ran a really careful
[02:21] four-way race with four apps, two
[02:23] models, three document sizes, and three
[02:26] runs of each combination. And he showed
[02:28] the middle run rather than the best one.
[02:31] And that is the right way to do it
[02:33] because cherry-picking your best run is
[02:35] how you end up with YouTubers flexing
[02:37] numbers that never show up in real life.
[02:39] And when we look at his results, they
[02:41] were pretty clear because Ollama read a
[02:43] long 16,000 token document on Qwen
[02:46] 3.827B
[02:48] at 1,442
[02:50] tokens per second, while LM Studios MLX
[02:53] download read the same document at
[02:55] 1,372,
[02:57] which is about a 5% difference. On short
[02:59] prompts with the larger model, Ollama
[03:01] showed the first word in 1.3 seconds,
[03:04] the fastest of all four apps in the
[03:06] test. And on writing speed, Ollama was
[03:09] doing about 90 tokens a second while the
[03:11] other apps sat at around 42 to 48. So
[03:14] his verdict was that for most people,
[03:16] Ollama is the one to pick. That test was
[03:19] done carefully and the numbers are real.
[03:21] And if I'd watched that video 6 months
[03:23] ago, I'd have set up Ollama and never
[03:25] looked back. But there's one phrase in
[03:27] that verdict that gets glossed over, and
[03:29] that is most people. And what does that
[03:31] actually mean? Most people in that sense
[03:35] means one prompt at a time with one chat
[03:37] window and one person typing a message,
[03:40] waiting for the answer, and then typing
[03:42] another.
[03:43] And that is how I used AI tools for
[03:45] about 2 years. So I completely
[03:47] understand why it's the default
[03:48] assumption. The problem is that most
[03:51] people increasingly includes people who
[03:53] have handed the keyboard to an agent.
[03:56] And agents don't send one prompt at a
[03:58] time. They send four or eight or
[04:00] sometimes 20 all within the same second.
[04:03] So let's talk about what actually
[04:04] happens when two things ask the same
[04:07] model a question at the same time
[04:09] because that changes everything. Now
[04:11] stay with me here because once this
[04:12] clicks everything else in the video
[04:14] makes sense.
[04:16] Every Apple chip, whether that is an M4
[04:18] or an M5, does something kind of amazing
[04:21] when it runs a language model. For every
[04:23] single token it writes it reads the
[04:26] entire model out of memory. So if we
[04:28] take Quinn 3.827B
[04:31] at 4-bit quantization that is roughly 18
[04:34] GB traveling from unified memory to the
[04:37] GPU cores for every token it generates.
[04:41] The math at the end of that trip, the
[04:43] actual matrix multiplication and
[04:44] transformer computation barely takes any
[04:47] time at all.
[04:48] The bottleneck is really the trip
[04:50] itself, 18 GB over and over for every
[04:53] word. Now what happens if we have four
[04:56] requests all waiting? There are two ways
[04:58] a server can handle that. The first is
[05:00] to work on them one at a time, making
[05:03] the full 18 GB trip for request one to
[05:05] write its next token, then the full trip
[05:08] again for request two and so on, while
[05:11] each request waits in line for the
[05:12] others to finish. Engineers call that a
[05:15] queue and I call it a taxi with one cab
[05:17] per passenger and one passenger at a
[05:19] time.
[05:20] The second way is to work on them
[05:22] together where the server makes the 18
[05:24] GB trip once and on that single pass
[05:27] does the math for all four requests and
[05:29] writes one token for each of them from
[05:31] the same read. Engineers call that
[05:33] continuous batching and I call it a bus
[05:36] with the same trip carrying four
[05:37] passengers. And the total work barely
[05:40] changes between the two. What changes
[05:42] dramatically is how long request number
[05:44] four has to wait for its first word. In
[05:46] a queue where each request takes 30
[05:48] seconds Savage and four doesn't get its
[05:50] first word until 90 seconds in, which
[05:53] means it sits there completely idle for
[05:56] a minute and a half before the server
[05:58] even acknowledges it exists. With
[06:00] batching all four start writing right
[06:02] away and the combined output is roughly
[06:05] 2.7 times what a single request would
[06:07] produce in the same time because none of
[06:10] those memory trips get spent on waiting.
[06:12] So it ends up being two minutes against
[06:14] 45 seconds on the same Mac with the same
[06:17] model. And that difference between
[06:19] batching and queuing is what this whole
[06:21] video is about because as of September
[06:23] 25th, these two apps handle it very
[06:26] differently. On September 25th, Ollama
[06:29] released version 0.4.0 and the release
[06:32] notes have a line about Apple Silicon.
[06:33] It says that any model architecture the
[06:35] MLX runtime supports now runs on MLX
[06:39] automatically. They listed Qwen 3.8,
[06:41] Gemma 4, Qwen 3.6 and Qwen 3.5 as
[06:45] examples and those are exactly the
[06:47] models everyone is running for coding
[06:49] work right now. And this was really
[06:51] exciting news because MLX is Apple's own
[06:54] machine learning framework and it's
[06:56] optimized for Apple Silicon in ways that
[06:58] generic runtimes just can't match. For
[07:00] single requests, it's noticeably faster.
[07:03] So the whole thing sounded like a pure
[07:04] upgrade. But what the release notes
[07:07] didn't prominently flag is what happens
[07:09] to parallel requests. There's a GitHub
[07:11] issue number 17280
[07:14] filed back in July where someone noticed
[07:16] that models served through the MLX
[07:18] engine were processing requests strictly
[07:20] sequentially regardless of the parallel
[07:22] setting they had configured.
[07:24] They set parallel requests to eight,
[07:26] sent several requests at once and
[07:28] watched the wall time come out at
[07:30] exactly eight times one request, which
[07:33] is perfect queuing. And it turns out the
[07:35] MLX runner gets launched without a
[07:37] parallel flag at all. Now, to be fair,
[07:39] Ollama has been working on this and
[07:42] their November third release, version
[07:44] 0.40.15
[07:46] did add parallel requests for some
[07:48] models. But the release notes says those
[07:50] are recurrent and vision GGUF models. So
[07:53] we are talking about GGUF and not MLX.
[07:57] So if your model loaded on the MLX
[07:59] engine, which it probably did
[08:01] automatically after September 25th, the
[08:03] parallel setting isn't reaching it at
[08:05] all. And we can check this by opening
[08:07] activity monitor while a model is loaded
[08:09] or running PS in terminal. If the runner
[08:12] process says MLX engine, you are on MLX
[08:15] and the parallel setting isn't doing
[08:17] anything. And the part that really got
[08:19] me is that I'd done this myself. Nearly
[08:21] every setup guide for Claude code on
[08:23] Ollama gives the same standard tip,
[08:26] which is to set Ollama num parallel to
[08:28] four.
[08:29] I followed it and I thought I'd fixed
[08:31] the problem, but I hadn't. On a Mac
[08:33] running Ollama 0.40 with an MLX model,
[08:37] that variable goes nowhere useful where
[08:39] the server receives it and the runner
[08:41] doing the actual work never hears about
[08:43] it. There's a workaround, which is to
[08:45] pull the GGUF version of your model so
[08:47] it runs on Ollama's llama CPP path where
[08:50] the parallel setting actually works. But
[08:52] then we are giving up the MLX speed
[08:54] boost we just upgraded for in the first
[08:56] place and single request speed drops
[08:58] noticeably, so we end up trading our
[09:00] fast lane for more lanes and doing it by
[09:03] accident with no warning anywhere in the
[09:05] app. And that is a rough situation to be
[09:08] in and I was in it. Meanwhile, LM Studio
[09:11] had been quietly going in a completely
[09:13] different direction because back in
[09:15] February in version 0 to 4.2, they added
[09:19] parallel requests for MLX through
[09:21] continuous batching, not as a workaround
[09:23] or a GGUF fallback, but as a first-class
[09:25] feature of their MLX engine. And the
[09:28] default is four concurrent predictions,
[09:30] which just works. Now, I will be honest,
[09:33] I'd always slightly dismissed LM Studio.
[09:36] I know that is irrational, but Ollama
[09:38] has this MIT open source energy that
[09:40] just feels right. It runs headless and
[09:43] it has great CLI tooling with one
[09:45] command, Ollama pull, and you are done.
[09:48] And LM Studio always felt like it was
[09:50] trying a little too hard with its fancy
[09:52] UI and I was wrong about that. In June,
[09:55] they extended their MLX batching to
[09:57] vision language models, which is exactly
[09:59] what Qwen 3.6 and Qwen 3.8 are and those
[10:02] are the two most popular models for
[10:04] coding work right now.
[10:06] And they published a before and after
[10:07] showing what that actually looks like on
[10:10] an M3 Max MacBook Pro with 36 GB, four
[10:13] short chats at once took 37.6 seconds on
[10:16] the old engine and 16.78 seconds on the
[10:20] new one. That is 2.2 times faster for
[10:23] the same amount of output on the same
[10:25] machine with the same model.
[10:27] But the number that really landed for me
[10:29] came from a competitor, an engine called
[10:31] Rapid MLX, which markets itself as
[10:34] faster than LM Studio. They published a
[10:36] benchmark table from an M5 Max with 36
[10:39] GB running Qwen 3.8 27B. And when we
[10:42] look at the LM Studio rows, a single
[10:45] stream did 26.0 tokens per second, while
[10:48] four simultaneous streams did 69.7
[10:51] tokens per second combined. So that is
[10:54] 2.68 times the output from the same Mac
[10:57] on a competitor's own chart from a
[10:59] company whose whole pitch is that they
[11:01] are better than LM Studio and who are
[11:03] using that table as their comparison
[11:05] point. Now, if we put that into
[11:07] practice, say an agent fans out to four
[11:09] sub agents and each answer takes 30
[11:11] seconds in a queue. With LM Studio's
[11:13] measured batching, 120 seconds of work
[11:16] finishes in about 45.
[11:18] All four agents start writing almost
[11:20] immediately and the main agent gets all
[11:22] four answers back and can keep moving
[11:24] instead of two full minutes of watching
[11:26] a spinner on the same Mac with the same
[11:27] model. But those numbers come from
[11:29] controlled benchmarks and competitor
[11:31] tables. So I want to bring in a
[11:33] real-world test from someone actually
[11:35] using this for work.
[11:37] An owner who posts as US Marty ran a
[11:39] translation job on two M5 Ultra Max
[11:42] Studios, one with 256 GB of memory and
[11:46] one with 96. And this was not a lab
[11:48] test. It was an article split into
[11:50] chunks of about 900 characters with 16
[11:53] requests going in at once, which is a
[11:55] real workload. And when we look at the
[11:57] 96 GB machine, LM Studio produced 557.5
[12:02] tokens per second combined across all 16
[12:04] streams, while Ollama produced 103.8,
[12:08] which is 5.4 times the work. And And to
[12:11] go through all the fine print because I
[12:13] hate it when people skip it. Ollama was
[12:15] running with its parallel setting at
[12:17] one, which is the default. With the
[12:18] setting raised to two on the 256 GB
[12:21] machine, Ollama reached 170.3
[12:25] tokens per second while LM Studio
[12:27] produced 519.9
[12:29] on the same hardware. So it was still
[12:30] about three times. There's also one more
[12:32] bar in that data worth noting, which is
[12:35] plain llama cpp running directly without
[12:38] either app as a wrapper, and that hit
[12:40] 680.4
[12:42] tokens per second. So the engine
[12:44] underneath was never the problem, and it
[12:46] was the defaults in front of it that
[12:47] were. Now, this is a single person's
[12:50] test, and the post had under 100 views
[12:52] when it first surfaced, so take it with
[12:54] some salt. But it lines up with every
[12:56] mechanism we have talked about so far,
[12:59] and the numbers are not surprising once
[13:01] we understand the difference between
[13:02] batching and queuing.
[13:04] And the uncomfortable part is that the
[13:05] more memory you bought, the more a queue
[13:08] costs you. Someone who spent £4,000 on
[13:11] an M5 Ultra and runs Ollama on default
[13:13] settings is using maybe a fifth of what
[13:16] they paid for in multi-agent throughput.
[13:18] Now, I want to stop here and make the
[13:20] strongest case I can for Ollama because
[13:23] it's a real case and it deserves a
[13:24] proper hearing.
[13:26] That 90 tokens per second Ollama was
[13:28] hitting in the Dark Factories race,
[13:30] while LM Studio sat at 42 to 48, isn't a
[13:34] fluke. And it doesn't come from MLX
[13:36] alone. It comes from something called
[13:38] speculative decoding.
[13:40] The basic idea is clever. We run a small
[13:43] draft model alongside the big one, and
[13:45] the draft model is fast and dumb, so it
[13:48] guesses the next several tokens ahead,
[13:49] and then the big model checks those
[13:51] guesses in a single pass. And when the
[13:53] guesses are right, which they often are
[13:55] on predictable text, we get several
[13:57] tokens for the price of one big model
[14:00] check. So it works as a shortcut through
[14:02] the most common paths. Ollama added D
[14:04] Flash 2 draft models on MLX in version
[14:07] 0.40 at the end of October, and the Quen
[14:10] 3.8 page on their website lists a 27B D
[14:13] Flash 2 NVFP4 tag at 19 GB. The dark
[14:17] factory found that speculative decoding
[14:20] running by default with no way to switch
[14:22] it off. And that is genuinely impressive
[14:25] because it gives roughly 2 x the writing
[14:27] speed on a single stream out of the box
[14:30] with no configuration needed. So on one
[14:32] request, Olama really does win both on
[14:35] time to first token for short prompts
[14:37] and on sustained writing speed. And the
[14:40] draft is doing real work there. Now,
[14:42] does that 2 x single stream advantage
[14:44] actually cancel out LM Studios 2.7 x
[14:47] batching gain once we have four agents
[14:49] running? Roughly speaking, they are in
[14:51] the same ballpark on paper since Olama's
[14:54] draft doubles one stream and LM Studios
[14:57] batching gets 2.7 x the output from four
[14:59] streams. But the key difference that the
[15:01] math alone doesn't capture is that in LM
[15:04] Studio, sub agent 4 doesn't wait for sub
[15:07] agents 1 2 and 3 and it starts writing
[15:11] right away on the same pass and the
[15:12] experience for whoever is watching the
[15:14] terminal is completely different. And
[15:17] Olama's 2 x boost is per stream. So in a
[15:20] queue, it makes the queue a bit less
[15:21] painful, but it doesn't change the fact
[15:23] that it's still a queue.
[15:25] Unless, of course, LM Studio had a draft
[15:28] of its own.
[15:29] And as of September 19th, it does. LM
[15:32] Studio 0.4 added something called Splash
[15:35] from a company called Inco AI as an
[15:38] experimental backend on Max. Splash is
[15:40] built for exactly two models, Quinn
[15:43] 3.635B
[15:44] and Quinn 3.827B
[15:47] and each one comes with its own D Flash
[15:49] 2 draft. So we get the speculative
[15:51] decoding boost from the draft and the
[15:52] continuous batching from LM Studios MLX
[15:55] engine in one place. Inco published
[15:58] numbers from a 48 GB M5 Pro where Quinn
[16:02] 3.827B
[16:03] did 74 tokens per second on a single
[16:06] short request and 170 combined with four
[16:09] streams running at once. And that is the
[16:12] draft and the batch working together. I
[16:14] do want to put two warnings on that. The
[16:16] first is that those are Inco's own
[16:18] numbers and the same post compared
[16:20] against Olama at 24 tokens per second.
[16:23] But that measurement was taken before
[16:25] Olama 0.40 and before Olama had the
[16:28] flash drafts. So the Olama number there
[16:31] is stale and that comparison should not
[16:33] be taken at face value. The second is
[16:35] that Splash has real hardware
[16:37] requirements, which are an M3 chip or
[16:39] newer, macOS 26.4 or later, and at least
[16:43] 36 GB of memory with 48 recommended. So
[16:46] on a 16 GB MacBook Air, you'll never see
[16:49] Splash and it will not even show up as
[16:51] an option. But on a 48 GB M5 Pro or
[16:54] anything larger, things get genuinely
[16:57] exciting because the draft handles the
[16:59] speed on each individual answer and the
[17:01] batch handles the throughput when agents
[17:03] run in parallel. So we are not choosing
[17:05] one or the other. And one thing that
[17:07] would be easy to miss is that this is an
[17:08] experimental backend. So it isn't Inco's
[17:11] models running on LM Studio server, it's
[17:14] Inco's inference engine, Splash,
[17:16] available as an alternative backend
[17:18] inside LM Studio's interface. If you
[17:21] want to try it, it's in settings and
[17:23] clearly labeled as experimental, so
[17:25] treat it that way. But the trajectory
[17:27] here is obvious and it's only going in
[17:28] one direction. Now, before we go and set
[17:30] any of this up, we need to talk about
[17:32] context length because both apps have
[17:34] quietly been biting people here and
[17:36] neither of them makes it obvious.
[17:38] Context length is the amount of text a
[17:40] model can hold in its working memory at
[17:42] once and it includes the system prompt,
[17:44] the whole conversation so far, the tool
[17:47] calls, and the tool results.
[17:49] Claude Code's own documentation says its
[17:51] first request alone can run to 33,000
[17:54] tokens and every request after that
[17:56] grows with the conversation. Olama sets
[17:59] the context length automatically based
[18:01] on available memory with 4,000 tokens
[18:03] under 24 GB and 32,000 between 24 and 48
[18:08] GB. And Olama's own documentation says
[18:11] coding tools want at least 64,000. So
[18:13] what happens on a 24 GB machine running
[18:16] Claude Code? Olama is silently giving us
[18:19] a context window about half the size of
[18:21] a single request,
[18:23] and things start getting cut off in ways
[18:24] that are confusing and hard to debug.
[18:27] The fix is straightforward, which is to
[18:28] set Ollama context length manually. But
[18:31] most people don't know to do that until
[18:33] something subtle goes wrong and they
[18:34] spend two hours working out why their
[18:36] agent keeps losing track of earlier
[18:38] context.
[18:39] And LM Studio isn't safe either because
[18:41] there's an open bug report from August
[18:43] about a 24 GB MacBook Pro with an M4.
[18:47] The auto fit feature in LM Studio's MLX
[18:50] engine detected the memory constraints
[18:52] and silently set the context to 4,096
[18:56] tokens, overriding the 24,576
[18:59] the user had typed in. The user didn't
[19:01] notice
[19:02] and the model just quietly got shorter.
[19:04] So in LM Studio, the check is to run LM
[19:07] SPS in the terminal after loading a
[19:09] model and confirm the context length
[19:12] that actually loaded matches what you
[19:13] configured. And in Ollama, we send one
[19:16] request and run Ollama PS, which shows
[19:19] the context the model loaded with. That
[19:21] is two commands and they are worth
[19:23] running every time we try a new model or
[19:26] update the app.
[19:27] And there's one more gotcha I found the
[19:28] hard way. Ollama 0.40 converts older
[19:32] GGUF models to its new format in the
[19:35] background the first time you load them
[19:37] and it keeps the original file next to
[19:38] the converted copy. One user counted
[19:41] about 20.6 extra gigabytes across just
[19:43] four models. So if your storage is
[19:45] slowly disappearing, that might be why.
[19:48] And once you are sure you don't need the
[19:49] originals, you can clean them out of
[19:51] your Ollama models folder. Now, the
[19:53] right answer genuinely depends on which
[19:56] Mac you have. So let's go through it one
[19:58] memory tier at a time.
[20:00] At 16 gigabytes or 24 gigabytes, which
[20:02] is a MacBook Air or an entry MacBook
[20:04] Pro, the 18 GB M 3.8 27 B doesn't even
[20:09] fit in 16 gigabytes at a usable
[20:11] quantization. So we're on smaller models
[20:14] or heavy quantization and at 24
[20:16] gigabytes, it technically fits but
[20:18] leaves almost no room for a long context
[20:20] alongside it. Patching barely helps at
[20:22] this tier because there isn't enough
[20:24] memory to run several long conversations
[20:26] next to the model, so the parallel
[20:28] question almost never comes up in
[20:30] practice. Here, Ollama's single stream
[20:33] speed and its speculative decoding are
[20:35] genuinely the right call, so pick the
[20:37] app you like using. And if you prefer
[20:39] the CLI and open source, Ollama is your
[20:41] answer and most of this video doesn't
[20:43] really apply to you. Now, at 32 GB,
[20:46] which covers a MacBook Pro with an M4 or
[20:48] M5 and a Mac Mini with an M5 or M6, we
[20:52] are in a middle ground. Cuen 3.8 fits,
[20:55] Ollama gives 32,000 tokens of context,
[20:58] and there might be room for two
[20:59] conversations running at once. Splash is
[21:02] out of reach here. And you'll see some
[21:03] benefit from LM Studio's batching if you
[21:06] run agents heavily. But Ollama's draft
[21:08] advantage on single requests still
[21:10] matters. So I test both and see which
[21:12] feels faster in your actual workflow. At
[21:14] 48 GB to 64 GB, which is an M5 Pro or
[21:18] the upper Mac Mini tier, Splash becomes
[21:20] available and there's genuine room for
[21:22] multiple long contexts alongside the
[21:24] model. And this is where LM Studio
[21:26] starts to pull noticeably ahead for
[21:28] anyone running agents because the
[21:30] batching gap becomes real and
[21:32] consistent. For any serious coding agent
[21:34] work at this tier, LM Studio with MLX
[21:37] and Splash is the setup I'd recommend
[21:39] without hesitation. At 96 GB to 128 GB
[21:43] on an M5 Max or M5 Ultra,
[21:46] there's room for every sub-agent Claude
[21:48] code will ever spawn to hold a full
[21:51] 64,000 token context at the same time.
[21:54] And a queue wastes a genuinely
[21:56] embarrassing amount of what you paid
[21:58] for.
[21:59] This is exactly the hardware where that
[22:00] 5.4x difference from the translation
[22:03] test shows up the most. And at 256 GB
[22:06] and beyond on an M5 Ultra or M5 Ultra
[22:09] Max, it helps to remember that the
[22:11] translation test we looked at earlier
[22:13] ran on an M5 Ultra with 96 GB and with
[22:16] 256 GB,
[22:18] and the gap held at 5.4x and 3x
[22:21] respectively. So if you are at this tier
[22:23] and using Ollama with default settings
[22:25] for agent work, you have my full
[22:27] permission to feel vaguely annoyed on
[22:29] behalf of your credit card. Now, let me
[22:31] go through the actual setup steps for
[22:33] each app, so nothing quietly reverts to
[22:36] a bad default after an update. In LM
[22:39] Studio, download the MLX version of your
[22:41] model rather than GGUF. When you load
[22:44] it, turn on manual load parameters and
[22:46] open the advanced settings where you'll
[22:48] find max concurrent predictions, which
[22:51] is your batching ceiling, and you can
[22:53] leave it at four or raise it depending
[22:55] on your memory, and set your context
[22:57] length in the same panel. Then, before
[22:59] you do anything else, run LMSP S in your
[23:03] terminal and check that the context
[23:05] length in the output matches what you
[23:06] typed because with the autofit bug, it
[23:09] might not. If it doesn't match, go back
[23:11] and check your memory settings and model
[23:13] quantization. And if your hardware
[23:15] qualifies and you want to try Splash, go
[23:17] to settings, switch the backend to
[23:19] Splash and reload your model, and the
[23:21] same context check applies. Now, in
[23:24] llama, the Mac app reads its environment
[23:27] variables from launch CTL rather than
[23:29] from your terminal session, and this
[23:31] catches people constantly. So, if you
[23:33] set value to four in your terminal
[23:35] before running llama, it does nothing
[23:37] because launch CTL already launched the
[23:39] app without that variable. To set it
[23:41] properly, run launch CTL set env llama
[23:45] context length 64000
[23:47] and restart llama. Or if you are running
[23:50] llama serve yourself in a terminal, put
[23:52] the variables in front of the command on
[23:53] the same line. Then, after you load a
[23:55] model and send one request, run llama
[23:58] PS, which shows the context the model
[24:01] actually loaded with. If it says 4000
[24:03] when you wanted 64000,
[24:06] the variable didn't reach the app and
[24:08] that is the first thing to fix. And if
[24:10] you need parallel requests and don't
[24:11] mind trading some single stream speed,
[24:13] pull the GGUF version of your model with
[24:16] llama pull model name Q4 or similar,
[24:19] then set llama num parallel through
[24:21] launch CTL as above, and the GGUF model
[24:24] will run on llama CPP where the parallel
[24:26] flag actually works. And finally, check
[24:28] activity monitor or PS in terminal while
[24:31] your model is loaded, where MLX engine
[24:34] and the runner process means you are on
[24:35] MLX and something with llama in it means
[24:38] you are on GGUF. It's worth knowing
[24:40] which world you are in because the
[24:42] settings that work in one don't work in
[24:44] the other, and 5 minutes of setup is
[24:46] worth more than switching apps every few
[24:48] weeks hoping something changed.
[24:50] So after going through all of this, here
[24:52] is where I actually land. For single
[24:55] chat use, Ollama is genuinely the better
[24:57] app today because its speculative
[24:59] decoding gives you roughly double the
[25:01] writing speed on M 3.8 out of the box
[25:04] and it got to the first word fastest on
[25:06] short prompts in careful benchmarks.
[25:08] It's MIT open source, it runs headless
[25:10] as a background server, and there's one
[25:13] command that wires it directly into
[25:15] Claude code. So with one chat window
[25:17] open and you doing the typing, Ollama is
[25:19] the right call. But for agent use on
[25:22] larger Macs, which is anything M 5 Pro
[25:24] and above with 48 GB or more, LM Studio
[25:27] is the answer and it isn't close.
[25:30] Continuous batching on MLX means every
[25:33] parallel sub agent starts writing almost
[25:35] immediately instead of queuing. And if
[25:37] you can run Splash, you get the draft
[25:39] and the batch together.
[25:41] And that 5.4 X difference from the real
[25:43] world test isn't a fluke, it's the
[25:46] logical endpoint of continuous batching
[25:48] at scale. So before you pick one, the
[25:50] thing to ask is simple, which is how
[25:52] many things will ask my Mac a question
[25:54] at the same time?
[25:55] If the answer is one, meaning just you
[25:57] in one chat, then Ollama. And if the
[26:00] answer is four or more with Claude code
[26:02] running sub agents, open code, or any
[26:05] agent that fans out work, then LM Studio
[26:08] on a capable Mac. And on a 16 or 24 GB
[26:11] Mac, most of this doesn't apply yet. So
[26:14] use Ollama, enjoy the speed, and come
[26:17] back to this video when you upgrade.
[26:19] One more thing I want to say is that
[26:20] this situation isn't static. Ollama's
[26:23] issue 17280 is still open and the
[26:26] parallel GGUF support they added in
[26:28] November tells us they are working in
[26:30] that direction. So by the time you watch
[26:32] this, things may have changed. The right
[26:35] habit is to check the release notes
[26:36] every time there's a major update,
[26:38] verify your settings with Ollama PS and
[26:41] LM's PS, and not just assume things work
[26:44] because you set them 1 6 months ago. The
[26:46] Mac you have is really incredible and
[26:48] the models you can run on it are
[26:49] genuinely useful and the defaults in the
[26:52] app sitting in front of them are the
[26:53] only things standing between you and
[26:55] using all of it. So don't let those
[26:57] defaults win. And if you made it this
[26:58] far, thank you because this is a dense
[27:01] topic and I could have made it three
[27:02] times longer. There's a whole rabbit
[27:04] hole about prompt caching and whether
[27:06] turn two requests hit the cache properly
[27:08] that I didn't even get into. If you want
[27:10] to run that cache, check yourself. Run
[27:12] Ollama, run with the verbose flag, send
[27:14] a long message, then send a short
[27:16] follow-up and compare the prompt eval
[27:18] count. If the second number is small,
[27:21] your cache is working. But if it's the
[27:22] same big number both times, your model
[27:25] is re-reading the full conversation
[27:27] every turn. And that is a lot of wasted
[27:30] time and memory bandwidth. Links to the
[27:32] benchmarks I referenced, the GitHub
[27:34] issues and Inco splash numbers are all
[27:36] in the description and they are worth
[27:38] reading if you want to verify any of
[27:40] this yourself rather than taking my word
[27:42] for it. And if this was useful, the
[27:44] subscribe button is right there and it
[27:46] genuinely helps the algorithm show this
[27:48] to people sitting there right now with a
[27:49] cold coffee and a spinning cursor,
[27:51] wondering why their agent is so slow.
[27:54] I'll see you in the next one.