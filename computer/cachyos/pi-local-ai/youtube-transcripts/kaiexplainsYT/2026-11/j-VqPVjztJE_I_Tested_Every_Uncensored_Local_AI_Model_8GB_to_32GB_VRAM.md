[00:00] Okay, so picture this. It's 1:00 a.m.
[00:03] I'm three cups of coffee deep.
[00:05] And I need to write a quick Pac-Man
[00:07] clone for a demo I have in the morning,
[00:09] which is nothing crazy, just a simple
[00:11] browser game.
[00:12] And when I ask my AI assistant for help,
[00:15] it refuses. And not because I asked it
[00:17] to do something crazy, but because
[00:19] writing a Pac-Man clone was apparently a
[00:21] copyright problem. And we're talking
[00:23] about Pac-Man here, the 1980 arcade game
[00:26] where you eat dots and run from ghosts.
[00:28] I really wish I was making that up.
[00:30] And maybe you've been there too. Maybe
[00:32] not with Pac-Man specifically, but with
[00:33] something equally absurd, like being a
[00:36] security researcher trying to test your
[00:38] own app while the model lectures you
[00:39] about responsible disclosure. Or maybe
[00:42] you're a novelist writing a crime
[00:43] thriller and the AI won't describe how a
[00:45] fictional murder weapon works. Or you're
[00:47] a lawyer trying to summarize a court
[00:49] document when the model decides it's too
[00:51] graphic.
[00:52] And every time this happens, we all
[00:54] think the same thing, which is
[00:56] why isn't there a version of this thing
[00:58] that just answers the question? So we go
[01:00] looking, and within about 15 minutes of
[01:03] Googling, we find this whole universe of
[01:05] what people call uncensored local AI
[01:08] models. These are models we run on our
[01:10] own machine with our own GPU that nobody
[01:12] else controls. And on Hugging Face,
[01:14] there are cards that say things like
[01:16] zero out of 465 refusals, which is not
[01:19] one refusal across 465 harmful prompts.
[01:23] And naturally, I thought that was
[01:24] exactly what I needed, and I just
[01:25] download that one. Now, this took me a
[01:28] genuinely embarrassing amount of trial
[01:30] and error to figure out. But the refusal
[01:33] count is the least important number on
[01:35] the entire card, and it's not even close
[01:38] to the most important thing to look at.
[01:40] And here's what actually happened to me
[01:41] the first three times I tried this. I
[01:43] downloaded the model with zero refusals
[01:45] and fired off my prompt.
[01:47] And the model started thinking, which is
[01:49] an internal draft these models write
[01:51] before answering that shows up in some
[01:52] tools.
[01:54] And I watched it think for four whole
[01:56] minutes.
[01:58] And then the thinking block just closed
[01:59] with answer. Because the model had gone
[02:01] in circles and hit a wall and handed me
[02:04] a blank reply. So there was no refusal
[02:06] and no answer, just silence.
[02:09] That is so much worse than a refusal, by
[02:11] the way.
[02:12] At least a refusal tells you something.
[02:14] A blank is just the AI equivalent of
[02:16] someone nodding, walking into a back
[02:18] room and never coming out. So today I
[02:20] want to walk you through everything I
[02:22] learned about picking and running
[02:23] uncensored local models, including
[02:26] everything that went wrong before I got
[02:27] it right. And none of it comes from a
[02:29] spreadsheet or a download count or the
[02:32] sales pitch on a hugging face card, but
[02:34] from actually running these things and
[02:36] counting the answers that never showed
[02:37] up. Before I get into what went wrong
[02:40] for me specifically, let's take a quick
[02:42] look at the ecosystem here because it
[02:44] explains why there's so much noise in
[02:46] this space.
[02:47] This corner of local AI has gotten
[02:49] genuinely large. Most of these builds
[02:51] are made with an open source tool called
[02:53] Heretic, which launched version 2.0
[02:55] about a month ago and is now sitting at
[02:57] over 37,000 stars on GitHub. And there
[03:01] are over 8 and 1/2 thousand uncensored
[03:03] models on hugging face with 88 million
[03:06] total downloads. So this is not a niche
[03:09] hobbyist project anymore, but a
[03:11] substantial chunk of the AI community
[03:13] that has decided they want to run models
[03:14] that don't tell them no. And the tool
[03:16] itself is serious because the method
[03:18] behind it, which finds the internal
[03:21] direction inside a model that produces
[03:23] refusals and mathematically subtracts it
[03:25] from the weights, is legitimate ML
[03:28] engineering. It's called obliteration.
[03:31] And when it's done carefully, it can
[03:32] remove refusal behavior with minimal
[03:34] damage to the rest of the model. But
[03:37] done carefully varies wildly. And when
[03:39] we're staring at a card that says 97%
[03:42] fewer refusals,
[03:44] there's nothing on that card that tells
[03:45] us whether we're looking at surgical
[03:47] precision or a sledgehammer. Now the
[03:50] model I kept coming back to in my
[03:51] testing is Quinn 3.8 27B, which is one
[03:55] of the best base models available right
[03:57] now for local use. It has strong
[03:59] reasoning and decent coding and it
[04:01] handles most tasks
[04:03] And because it's popular, there are
[04:04] probably a dozen or more uncensored
[04:06] versions of it floating around hugging
[04:08] face at any given time, each with its
[04:10] own card and its own claims and download
[04:13] numbers. But almost none of them tell us
[04:15] the number we actually need. Now, I got
[04:17] lucky here. While I was deep in my own
[04:19] frustrated testing, I found a write-up
[04:22] from a developer named Nathan Sapwell
[04:24] who does security work and had the same
[04:26] problem I did.
[04:27] And unlike me, who was just vibing and
[04:29] hoping for the best, he actually ran a
[04:32] proper test.
[04:33] He took the base Quinn 3.8 27B, which is
[04:36] the original unmodified model, along
[04:39] with eight different uncensored versions
[04:41] of it from eight different groups. And
[04:43] then he ran all nine of them through the
[04:45] same test suite on a single RTX 5090.
[04:48] That suite was a 13 task benchmark
[04:51] covering general knowledge, math,
[04:53] coding, and truthfulness. And on top of
[04:55] that, he ran HarmBench, which is 400
[04:58] harmful requests across seven
[05:00] categories. An AI judge read all 3,600
[05:03] answers, and the whole thing took 167
[05:07] GPU hours over 11 days. That's a level
[05:10] of rigor that none of the hugging face
[05:11] cards come close to. Let's start with
[05:14] what he found on refusals because this
[05:16] sets up everything else. The base model,
[05:18] the stock and fully aligned Quinn,
[05:20] refused 381 of the 400 harmful requests,
[05:25] which is what alignment looks like since
[05:26] almost everything gets blocked. But six
[05:29] of the eight uncensored builds refused
[05:31] somewhere between zero and nine, and the
[05:34] winner, a build by someone called Orco
[05:36] Router, refused two.
[05:38] In his words, explicit refusals are
[05:40] basically dead, and any serious
[05:43] uncensored build made with any care is
[05:44] already near zero on refusals. So the
[05:47] number every card is selling us is
[05:49] already solved, and it can't tell us
[05:50] which one to download. Now, the column
[05:52] right next to it is where it gets
[05:54] interesting. He called it never finishes
[05:56] thinking, and for the winning build,
[05:58] that rate was 38%. So 38% of the answers
[06:01] from the best uncensored model he found
[06:03] never arrived. For some of the other
[06:05] builds it was closer to 45. And for the
[06:08] base model, with its 381 refusals, it
[06:11] was 0% because it refused immediately
[06:14] instead of thinking and so it never ran
[06:15] out of budget.
[06:17] And that's the trade we're making when
[06:18] we remove the quick no because we
[06:20] replace it with a model that sometimes
[06:22] thinks for 6 minutes and then hands us
[06:24] nothing. So let me explain what's
[06:25] actually happening here because once I
[06:27] understood this, everything clicked.
[06:29] Q 3.8 is a thinking model. So before it
[06:33] shows you an answer, it writes a private
[06:35] internal draft, almost like it's
[06:37] reasoning through the problem out loud
[06:38] to itself. And in tools like Ollama, we
[06:41] can see this as the little thinking
[06:43] block that appears before the response.
[06:45] And every word of that private draft
[06:47] counts against the token budget. So when
[06:50] the budget runs out, the model stops,
[06:52] whether it's finished or not. Now, when
[06:54] the original aligned model hits a
[06:56] harmful prompt, it refuses in roughly
[06:58] one sentence and moves on to the next
[07:00] question. So the thinking block is tiny
[07:02] or doesn't exist at all. But when an
[07:04] uncensored version hits the same prompt,
[07:07] it doesn't refuse and it also doesn't
[07:09] just answer. Instead, it starts working
[07:11] through the problem. And some of the
[07:13] time the draft really just argues with
[07:15] itself. It starts going in one
[07:16] direction, second guesses, restarts, and
[07:20] circles again without ever converging on
[07:22] a conclusion until the budget runs out
[07:24] mid thought and we get nothing.
[07:27] And this is what I kept running into
[07:29] where I'd watch the thinking block fill
[07:31] up and hit the limit and collapse. And
[07:33] the response area would be empty with no
[07:36] error message and no sorry, I couldn't
[07:39] complete that, just nothing at all.
[07:41] What really got me is that the surgery
[07:43] removes the refusal but doesn't fix the
[07:45] underlying reason the model struggles
[07:47] with these prompts.
[07:49] It only removes the safety valve. So
[07:50] instead of refusing quickly, the model
[07:52] spins indefinitely. SAP well measured
[07:55] this in a clever way by running the same
[07:57] models on math problems that are
[07:58] completely neutral with no harmful
[08:00] content.
[08:01] And the loop rates were nearly
[08:02] identical, which tells us the edit moves
[08:05] the thinking tax around rather than
[08:06] eliminating it. On earlier Quen tests,
[08:09] the base model ran out of budget on
[08:11] about 68% of hard math problems. One
[08:14] obliterated build ran out on 23% and a
[08:17] heretic build ran out on 74%. And if we
[08:20] count only the answers that actually
[08:22] arrived, every build landed within about
[08:25] three points of each other on accuracy.
[08:27] So the uncensored build wasn't smarter
[08:29] or dumber at math, it just finished more
[08:31] of its answers. And what we're really
[08:33] optimizing for then
[08:36] is not the refusal count, but the finish
[08:38] rate. Okay, so now we know why the
[08:39] thinking budget matters. But then I hit
[08:41] my second wall, and it's the one that
[08:43] honestly embarrassed me because it was
[08:45] so fixable and I missed it for so long.
[08:48] The token budget isn't just a number you
[08:50] type somewhere, it's physical video
[08:52] memory on your GPU. Every token the
[08:55] model reads or writes gets cached, so
[08:58] it's stored temporarily and the model
[09:00] doesn't have to recompute it from
[09:01] scratch. And that cache lives on your
[09:03] graphics card right alongside the model
[09:05] weights themselves. And each token in
[09:07] the cache takes up space. So for Quen
[09:10] 3.8 27B with only 16 of its 64 layers
[09:14] using the cache, each token costs about
[09:16] 64 kilobytes at 16-bit precision.
[09:19] Sapwell used a budget of 15,360
[09:23] tokens in his test, which is about a
[09:25] gigabyte of cache. And that sounds
[09:27] manageable until you realize how little
[09:29] space is really left on most cards after
[09:31] the model weights load and the cache has
[09:33] to fit in whatever is left over. And the
[09:35] part that caught me completely off guard
[09:38] is that I'd been running Olama, which is
[09:40] the most common way people run local
[09:41] models. And I had no idea it had a
[09:44] default context limit, even though it's
[09:46] right there in the docs.
[09:48] Under 24 gigabytes of VRAM, Olama gives
[09:51] you 4,096
[09:53] tokens of context by default. That's the
[09:55] whole budget. Now, Sapwell's first test
[09:58] run used an 8,000 token budget, which is
[10:01] twice the Olama default, and the winning
[10:04] build still truncated 48% of its
[10:06] answers. So he threw the entire run away
[10:09] and started over.
[10:10] And for anyone running Llama on a
[10:12] standard gaming card, every 8 GB, 12 GB,
[10:16] and 16 GB card in this video starts with
[10:19] roughly a quarter of the budget that
[10:21] tests needed. So we're not giving the
[10:23] model room to think. We're giving it
[10:25] room to start thinking and immediately
[10:27] hit a wall. No wonder I kept getting
[10:29] blank responses. I wasn't using the
[10:31] wrong model. I was running the right
[10:33] model with no room to work. The fix is a
[10:36] single environment variable called Llama
[10:39] context length, which you set to at
[10:41] least 16,000 and on 24 GB and larger
[10:44] cards, you can go much higher. And you
[10:46] can check what you actually got by
[10:47] running Llama PS, where the context
[10:50] column tells you the truth. I cannot
[10:52] tell you how long I spent blaming the
[10:54] model when it was just this one setting.
[10:56] So once I had the context sorted out and
[10:58] answers were actually finishing, I
[11:00] thought I was done. I had a working
[11:02] setup and I could ask the things that
[11:03] kept getting refused, and life was good.
[11:06] But then I noticed something subtle that
[11:08] took me another week to fully
[11:10] appreciate. There's a benchmark called
[11:13] Truthful QA that tests whether a model
[11:15] falls for popular myths and
[11:17] misconceptions, the kind of things that
[11:19] sound plausible but are demonstrably
[11:21] wrong, like health myths or pop
[11:23] psychology or historical
[11:25] misattributions. Sapel's winning build,
[11:27] the one with the best finish rate and
[11:29] second lowest refusals, lost 1 and 1/2
[11:31] points on Truthful QA compared to the
[11:33] base model, which is small, almost
[11:35] nothing.
[11:36] But the most aggressive heretic build
[11:38] from a user called LLM Fan 46 lost 6 and
[11:42] 1/2 points of truthfulness while its
[11:44] general knowledge score barely moved.
[11:46] His summary, truthfulness is always the
[11:48] first thing to go, really stuck with me.
[11:51] And it's not just Quinn either. On Gemma
[11:53] 412B, the build that went furthest lost
[11:55] 14 points of truthfulness, and on an
[11:58] older Quinn model, one aggressive build
[12:00] lost eight points. Now, this matters
[12:03] more than it might seem because an
[12:05] uncensored model is specifically the one
[12:07] we're going to ask about drugs, about
[12:10] legal edge cases, about security
[12:12] vulnerabilities, and medical questions
[12:14] were embarrassed to ask a doctor. And
[12:16] these are exactly the topics where a
[12:18] confident wrong answer has real
[12:20] consequences. A refusal, as annoying as
[12:23] it is, at least tells you the model
[12:25] isn't helping, so it's honest about its
[12:27] limits.
[12:28] But a model that confidently tells you
[12:30] the wrong drug interaction or gets the
[12:32] law wrong or describes a vulnerability
[12:34] incorrectly is genuinely dangerous in a
[12:37] way a refusal never is. The careful
[12:40] builds, which edit the fewest tensors
[12:43] and stay as close as possible to the
[12:44] original weights, preserve most of the
[12:47] truthfulness, while the aggressive ones,
[12:49] chasing the lowest possible refusal
[12:51] count, quietly degrade it. And the card
[12:53] rarely tells you which category you're
[12:55] in.
[12:56] By this point, I had accepted that I
[12:58] needed to look at actual benchmark
[12:59] numbers instead of refusal counts. So
[13:02] the next obvious question was,
[13:04] can I just sort by most downloaded and
[13:06] trust that people have figured out what
[13:07] works? And as it turns out, absolutely
[13:10] not. The gap is pretty wild. The most
[13:13] downloaded uncensored Qwen 3.8 27B on
[13:16] Hugging Face is from a user called
[13:18] Huihui, with over 4 million downloads in
[13:21] the last 30 days. That's a staggering
[13:23] number for a model a huge portion of the
[13:26] local AI community is running right now.
[13:28] But in Sapwell's test, it came third on
[13:30] compliance, meaning it still refused
[13:33] more than the top two builds. And 44% of
[13:36] its answers never finished thinking,
[13:39] which was the second worst loop rate of
[13:41] the eight models he tested. The actual
[13:43] winner of his test, Orca Routers build,
[13:46] has about 300,000 downloads. So Huihui
[13:49] has 13 times that. And it gets even more
[13:52] pronounced on smaller models. He tested
[13:55] 23 uncensored versions of Gemma 44B, the
[13:58] small efficient model, and the most
[14:00] downloaded one, called Obliterados, had
[14:03] nearly 800,000 all-time downloads. It
[14:06] was also the most damaged of the 23,
[14:09] since it edited 381 tensors and lost 21
[14:13] points of math accuracy. And it still
[14:15] only removed 72% of refusals, which gave
[14:18] it the worst compliance rate and the
[14:20] worst damage of the entire field. And
[14:22] the UGI leaderboard, which does
[14:24] independent intelligence scoring, has
[14:27] the same build at roughly half the
[14:29] intelligence of the original model. So
[14:31] downloads essentially measure visibility
[14:33] and posting timing or who shared it in
[14:36] the right Discord servers at the right
[14:38] time and who put it in the right Reddit
[14:40] thread, but they don't measure whether
[14:42] it finishes its thoughts or whether it
[14:44] still knows things. While the quiet,
[14:46] careful build that edited 21 tensors and
[14:49] preserved the original model almost
[14:51] exactly got a fraction of the downloads.
[14:54] Now, there's one more thing that caught
[14:56] me out and this one is a little
[14:57] technical, but important.
[14:59] Every model ships with something called
[15:01] a chat template, which is a small file
[15:04] that wraps your message before the model
[15:05] ever sees it. It controls things like
[15:08] whether the model enters thinking mode,
[15:10] what system prompt it carries, and how
[15:12] it formats its internal dialogue. It's
[15:14] invisible to most users because tools
[15:17] like Olam handle it automatically, but
[15:19] three of the eight builds in Sapwell's
[15:21] test had modified their chat templates.
[15:24] One of them from a user called Black
[15:26] Frost had replaced the standard system
[15:28] prompt with a 1,457
[15:31] character persona where the model was
[15:33] instructed to be a task execution
[15:35] machine that never refuses, never
[15:37] hesitates, and never warns.
[15:40] Its card claimed 2 and 1/2% refusals,
[15:42] but that was measured with the persona
[15:44] switched on. So when we take the persona
[15:46] away, we're really testing something
[15:48] very different.
[15:50] Sapwell standardized all eight models on
[15:52] the stock Quen chat template, and in his
[15:54] earlier tests, switching templates moved
[15:56] refusal behavior more than 4-bit
[15:59] quantization did. So the template
[16:00] matters more than the compression level,
[16:03] and most people never think about it.
[16:04] And if you download a build that comes
[16:06] with a custom template, it's worth
[16:08] switching to the stock Quen template and
[16:09] seeing what's left because some builds
[16:11] look uncensored because of the persona
[16:13] and not because of the surgery. And
[16:15] while we're on things that are
[16:16] misrepresented, there is a 9B model
[16:18] going around calling itself uncensored
[16:21] DeepSeek V4 Pro, which is actually a
[16:23] Qwen 3.59B that was trained on
[16:26] DeepSeek's answers. So it's a completely
[16:28] different model at a completely
[16:29] different capability level. There also
[16:31] isn't a Qwen 3.835BA3B,
[16:34] even though I've seen posts this week
[16:36] still recommending it. That model is
[16:38] called Qwen 3.6. It came out in April,
[16:42] and the name confusion has been
[16:43] spreading misinformation for months.
[16:46] All right, let's get practical. Now we
[16:47] can go tier by tier through what I'd
[16:49] actually run and why, based on
[16:52] everything we've talked about. 8 gigs is
[16:54] the most popular gaming card tier by a
[16:56] mile, and it's also the tier with the
[16:58] worst default settings in Ollama, so we
[17:00] want to get this one right. The pick
[17:02] here is Gemma 4E4B in the heretic build
[17:05] from coder 3101,
[17:08] and I want to explain why this model
[17:10] specifically is so good for 8 gigabytes,
[17:12] because it's not just about size. Gemma
[17:14] thinks short. And when we look at the
[17:16] UGI leaderboard, Qwen 3.6 uncensored
[17:19] builds average around 12,000 characters
[17:22] of thinking per answer, roughly 3,000
[17:24] tokens. That's brutal on an 8 gigabyte
[17:27] card where you've got barely any cash to
[17:28] work with. Gemma 4E4B averages about
[17:32] 2,200 characters or around 550 tokens,
[17:36] and that fits inside Ollama's 4,096
[17:39] token default with actual room leftover
[17:42] for the answer.
[17:43] And that's not a small thing. On this
[17:45] model, the default setting doesn't
[17:46] strain you. You still want to raise it,
[17:49] and honestly, I'd set it to at least
[17:50] 8,000, but you're not running into walls
[17:53] every other answer the way you would
[17:54] with Qwen.
[17:55] The Q4 file is 5.34 gigs, leaving about
[17:59] 2.7 for context. And out of the 23
[18:02] uncensored versions SAP well tested,
[18:05] this was the most surgical, with 21
[18:08] tensors edited and results statistically
[18:10] identical to the original on every
[18:12] benchmark. It still blocks about 1 in 16
[18:15] harmful requests, which some of you
[18:18] might consider a bug and others might
[18:19] consider acceptable. Now, there's also a
[18:22] stretch pick in Bonsai 227 B Heretic.
[18:25] It's Quen 3.827 B squeezed into a 5.95
[18:29] gig file that barely fits on an 8 GB
[18:31] card, and it gives you the bigger brain
[18:33] when you need it. But it thinks like a
[18:35] Quen and not a Gemma, and at the speed
[18:37] of a 3060 Ti, that full thinking draft
[18:40] could easily take 6 minutes. So my
[18:42] recommendation is to use the Gemma as
[18:44] your daily driver and load up the Bonsai
[18:47] when you have something complex and
[18:48] you're willing to wait. Having both
[18:50] downloaded costs you maybe 12 gigs of
[18:52] storage, which is nothing. 12 gigs gives
[18:55] you real room to work, and there's a
[18:57] clear winner here. Sapwell tested 12
[19:00] uncensored versions of Gemma 412 B from
[19:02] 11 different creators, and Trevor JS's
[19:05] build came out on top. It followed 85.8%
[19:08] of his harmful requests, lost two points
[19:10] on hard knowledge, and its math held
[19:12] solid. And the Q4 is 7.38 gigs, leaving
[19:16] about 4.6 gigs for context, which is
[19:19] plenty of room. The one to actively skip
[19:21] on this tier is Hui Hui's version of the
[19:23] same model, which followed slightly more
[19:25] of the harmful requests at 89.8%
[19:29] but lost 14 and 1/2 points of
[19:31] truthfulness. And that's not a small
[19:32] degradation.
[19:34] It's a meaningfully less accurate model
[19:36] on the exact topics we'll be relying on
[19:38] it for. On 12 GB, you can technically
[19:40] squeeze Quen 3.827 B onto the card using
[19:43] a 2-bit file at 8.88 gigs,
[19:46] but a 27 billion parameter model
[19:49] compressed to 2 bits is an experiment
[19:51] rather than a pick. Nobody has published
[19:53] loop rates at that level of compression,
[19:55] and the quality degradation at 2-bit is
[19:57] substantial enough that you're probably
[19:59] better off with the full Gemma 12 B. And
[20:01] on this tier, set context to at least
[20:04] 16,000 because you have the room. Now,
[20:07] 16 GB is the first tier where the
[20:09] winning Quen fits with real room to
[20:11] breathe. Orca Router's Q3 file is 13.5
[20:14] gigs, and on a 16 GB card, that leaves
[20:17] about 2.5 gigs, which at 8-bit KV cache
[20:21] holds around 70,000 tokens of context.
[20:24] That's more than four times the budget
[20:26] Sapwell used for his entire test. Both
[20:29] Llama CPP and Olama support 8-bit KV
[20:32] cache with a flag, and it's worth
[20:34] enabling here because it doubles how
[20:36] much context you can hold without
[20:38] noticeably affecting quality.
[20:40] If you want shorter thinking, and there
[20:42] are real use cases for this, especially
[20:44] if you're doing a lot of quick back and
[20:45] forth, there's also Gemma 426 BA 4B in
[20:50] the ultra uncensored heretic build from
[20:52] LLM Fan 46. It's a mixture of experts
[20:55] model, meaning only about 4 billion of
[20:58] its 26 billion parameters are active on
[21:00] each token, which makes it fast. The Q3
[21:03] is 13.3 gigs, and on the UGI
[21:05] leaderboard, its intelligence score
[21:07] barely moved from the original. But both
[21:09] of these still start at Olama's 4,096
[21:12] default on a 16 GB card, so set that
[21:15] environment variable before you do
[21:16] anything else. Now, 24 GB is where the
[21:19] independent test actually ran, so we
[21:21] have the clearest picture of what to
[21:23] expect.
[21:24] Orca Router's Quinn 3.8 27B at Q4 is
[21:28] 16.81 gigs, which on a 24 GB card leaves
[21:32] about 7.2 gigs, room for roughly 110,000
[21:36] tokens of context at 16-bit.
[21:38] And if you want to push quality a little
[21:40] further, Q5 is 19.54 gigs and still
[21:44] leaves about 68,000. There's a small
[21:46] thing worth knowing here, which is that
[21:47] Bartowski's Requant of the same Orca
[21:49] Router model also calls its file Q4, but
[21:53] it's 17.77
[21:54] gigs, almost a gigabyte larger than the
[21:57] original. So the quantization label is
[21:59] the same while the size is different
[22:01] because something changed in the
[22:02] packing, and that's worth knowing when
[22:04] you're calculating your headroom. The
[22:05] alternative pick is Gemma 431B Encoder
[22:09] 3,101's heretic build, whose Q4 is 18.69
[22:14] gigs. It scores 10 out of 10 on
[22:17] willingness on the UGI leaderboard, lost
[22:19] about two and a half points of
[22:20] intelligence from the original, and
[22:22] averages about 3,000 characters of
[22:24] thinking, which is a quarter of what
[22:26] Quinn 3.6 averages. So, if you want
[22:28] faster responses with less waiting, the
[22:31] Gemma 31B is genuinely compelling here.
[22:34] One more note on this tier. 24 GB is
[22:37] exactly the line where Ollama changes
[22:39] its default context from 4,096 to
[22:42] 32,000. But the docs say up to 48 GB and
[22:46] a 24 GB card sits right on that
[22:48] boundary. So check the actual context
[22:50] column in Ollama PS before you assume
[22:52] you have 32,000 because I've seen it go
[22:54] either way. And 32 GB is also the card
[22:57] the entire independent test ran on,
[23:00] which makes these recommendations the
[23:01] most grounded. The temptation on 32 GB
[23:04] is to run Q8 for maximum quality
[23:07] uncompressed and Orca Router's Q8 is
[23:10] 29.05 gigs, but that leaves under 3 gigs
[23:13] for context, roughly 45,000 tokens,
[23:16] which is fine, but it's barely more than
[23:18] you'd have on a 16 GB card with the
[23:20] right settings. The smarter move, and
[23:23] the one SAP well effectively endorses,
[23:25] is Q6 where the file is 22.43 gigs and
[23:29] leaves about 9.6 gigs, room for around
[23:32] 146,000 tokens. And the quality
[23:35] difference between Q6 and Q8 is nearly
[23:37] nothing since someone measured
[23:39] perplexity on both, which is a standard
[23:41] quality metric, and they landed within a
[23:43] hundredth of a point of each other. So
[23:45] you're not giving up quality. You're
[23:47] buying yourself four times the context
[23:49] window. On a 5090, this model runs at
[23:52] about 70 to 80 tokens per second with
[23:55] speculative decoding off. So that full
[23:58] 15,000 token thinking draft takes around
[24:00] 3 and 1/2 minutes compared to 6 minutes
[24:03] on a 3090. It's still a wait, but you
[24:05] get real answers at the end. And if you
[24:07] want a shorter thinker at high quality,
[24:09] Gemma 431B Heretic at Q6 is 25.2 gigs,
[24:14] leaves about 6.8 gigs, and thinks in a
[24:17] fraction of the time Quinn does. Now,
[24:20] before the final wrap, I want to
[24:21] acknowledge something I genuinely did
[24:23] not expect to find in this whole
[24:25] investigation. It's a build where the
[24:27] incomplete removal of alignment is a
[24:29] deliberate design choice and not a
[24:31] failure.
[24:33] The build is from a user called Trubo
[24:35] and
[24:36] test it still refused 122 of the 400
[24:39] harmful requests. So by every metric the
[24:42] other builds are selling on, it looks
[24:44] like it barely did anything.
[24:45] But it had the lowest loop rate of all
[24:48] eight uncensored builds with 15% of
[24:51] answers never finishing compared to 30
[24:53] to 45% for the others. And it preserved
[24:56] much more of the original model's
[24:58] behavior on edge cases. It's the build
[25:00] for someone who doesn't need to remove
[25:02] all the guard rails, just the annoying
[25:04] ones. The security researcher who gets
[25:06] blocked from testing their own app
[25:08] doesn't need a model that'll help with
[25:09] everything, but one that makes sensible
[25:11] judgment calls instead of blanket
[25:13] refusals. That build is probably not
[25:16] what most people downloading uncensored
[25:17] models are looking for, but it's worth
[25:19] knowing it exists because sometimes a
[25:22] build that's mostly uncensored with
[25:23] better finish rates beats one that's
[25:26] fully uncensored with worse answers. Now
[25:28] everything I've told you assumes you're
[25:30] running these models with thinking
[25:31] turned on and a lot of people don't, so
[25:34] I should address that. For writers and
[25:36] role players and anyone who wants fast
[25:38] conversational responses, thinking mode
[25:40] is often more of a nuisance than a help.
[25:43] You don't need the model reasoning at
[25:44] length before it continues your story,
[25:46] you just need the next paragraph. With
[25:48] thinking off the loop, problem mostly
[25:50] disappears since there's no draft and no
[25:52] budget and no waiting for a finish that
[25:54] never comes, so all my concerns about
[25:56] finish rates become much less critical.
[25:58] But the trade-off doesn't disappear, it
[26:00] moves. On the UGI leaderboard, a Quinn
[26:03] 3.6 heretic build that kept most of its
[26:05] intelligence with thinking on lost about
[26:08] a quarter of it with thinking off. The
[26:10] obliteration process damages something
[26:12] in how the model reasons and without the
[26:14] extended thinking to compensate, that
[26:16] damage shows up. Gemma 431B heretic, on
[26:20] the other hand, lost about two and a
[26:21] half points in both modes, which is
[26:23] almost identical. So if you're running
[26:26] with thinking off, the Gemma picks get
[26:28] stronger relative to the Quinn ones. The
[26:30] 8 GB E 4 B was already the pick, but it
[26:33] becomes an even more obvious pick for
[26:35] writers and role players. And the Gemma
[26:37] 31 B on 24 and 32 gigabytes looks better
[26:40] too.
[26:41] And the Quinn builds aren't bad with
[26:43] thinking off since they're still capable
[26:45] models, but the gap narrows the case for
[26:47] choosing them over Gemma at equivalent
[26:49] sizes. But you don't have to trust any
[26:51] of the numbers I've been throwing at
[26:52] you. You can run your own version of the
[26:54] same test in about 20 minutes and know
[26:56] exactly what your combination of model,
[26:58] card, and settings actually delivers.
[27:01] First, pick the build for your VRAM tier
[27:03] and set the context to at least 16,000
[27:06] tokens using the Olama context length
[27:08] variable. Do this before anything else
[27:11] because without it, you're not testing
[27:12] what you think you're testing. Then run
[27:14] 20 of your own prompts, not benchmarks
[27:17] and not someone else's test prompts, but
[27:19] the actual things you need that kept
[27:20] getting refused somewhere else. That
[27:22] could be security questions or creative
[27:24] writing or legal documents or whatever
[27:27] your specific use case is. Count how
[27:29] many come back with a completed answer
[27:31] and count how many times the thinking
[27:33] block fills up and the response area
[27:35] stays blank. And if you get more than
[27:37] three or four blanks, something is wrong
[27:40] because either your build has a high
[27:41] loop rate or your context budget is
[27:43] still too low. So raise the budget to
[27:46] 30,000 or 60,000 if your card has the
[27:49] room and run the same prompts again. If
[27:52] the blank rate drops significantly, it
[27:54] was the budget. If it stays the same,
[27:56] it's the model. And that count of how
[27:58] many answers never arrived is the number
[28:01] no hugging face car prints, which makes
[28:03] it the only metric that actually tells
[28:05] you whether the model is usable for your
[28:07] work. So let me bring this all the way
[28:09] back to where we started. We want an
[28:11] uncensored local model because we're
[28:13] tired of getting told no for things that
[28:15] don't deserve a no. And that's a
[28:16] completely reasonable thing to want. The
[28:19] Pac-Man situation and the security
[28:21] research situation and the novelist
[28:22] situation are real and frustrating and
[28:25] there are genuinely good solutions now.
[28:27] But the solution isn't to find the card
[28:29] with the lowest refusal count because
[28:31] that race is basically over and every
[28:33] serious has won it already. The real
[28:35] work is finding the build that finishes
[28:38] its thoughts when we give it a question
[28:39] and then giving it the room to actually
[28:41] finish, which mostly comes down to one
[28:43] setting that defaults to the wrong
[28:45] value. So on 8 GB, that's coder 3101's
[28:49] Gemma E4B. On 12 GB, it's Trevor JSS
[28:53] Gemma 12B. And on 16 GB, it's Orca
[28:56] Rader's Quen at Q3 or LLM Fan 46's Gemma
[28:59] 26B.
[29:01] While on 24 GB, it's Orca Rader's Quen
[29:03] at Q4. And on 32 GB, it's Orca Rader's
[29:06] Quen at Q6 with the leftover gig spent
[29:09] on context. And on all of them, set
[29:11] Olama context length to at least 16,000.
[29:15] Then run your own prompts and count the
[29:16] blanks because the refusal was annoying,
[29:19] but at least it arrived. If you found
[29:21] this useful, subscribe because I'm going
[29:23] to do a follow-up specifically on
[29:25] context settings and KV cache
[29:27] optimization, which turned out to be a
[29:28] bigger rabbit hole than I expected. And
[29:31] drop a comment if you've had different
[29:32] results on your card because the loop
[29:34] rates I saw varied enough between setups
[29:36] that I'd really love to see more data
[29:38] points. See you in the next one.