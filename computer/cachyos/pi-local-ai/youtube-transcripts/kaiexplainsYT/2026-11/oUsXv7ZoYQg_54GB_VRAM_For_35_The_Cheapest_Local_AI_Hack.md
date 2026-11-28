[00:00] Somebody in Russia paid 3,000 rubles,
[00:03] about 35 bucks, for a rusty old mining
[00:05] rig with 54 gigs of video memory,
[00:08] and it runs a 35 billion parameter AI
[00:11] model at over 30 tokens a second.
[00:14] But the number that actually made it
[00:15] fast isn't the one in the headline, and
[00:17] we'll get to which one, because you
[00:18] might already own it. For context, the
[00:21] expensive gaming cards have 24 gigs, and
[00:23] the really expensive ones have 48,
[00:25] right? And if you want 80,
[00:27] congratulations, you're now shopping for
[00:29] an Nvidia H100, which costs about the
[00:32] same as a small car, a good small car
[00:34] with heated seats. So yeah, the internet
[00:37] lost its mind. Tom's Hardware covered
[00:39] it, the UCCF Tech covered it. The Reddit
[00:41] post hit around 2,000 upvotes, and
[00:44] roughly 47 YouTube thumbnails showed up
[00:46] with a shocked face next to a pile of
[00:48] graphics cards. So what's the catch?
[00:51] His model only used 23 of those 54 gigs,
[00:54] and a second-hand GTX 1080 in a 2015
[00:57] desktop runs the exact same model at 25
[01:00] tokens a second.
[01:02] So if you've got an 8 gig card and 32
[01:04] gigs of RAM, there's a decent chance you
[01:06] already own this rig and you just don't
[01:08] know it yet.
[01:09] So I want to show you why nine graphics
[01:11] cards behave like one, why this thing is
[01:14] fast anyway, which number actually made
[01:16] it fast, and the one flag that gets you
[01:19] the same speed on hardware you probably
[01:21] already have. And at the end, we'll get
[01:23] to whether you should actually buy one
[01:25] of these at all.
[01:26] If you're new here, I'm Kai, and on this
[01:28] channel I work out what it really costs
[01:30] to run these models at home. And I'll be
[01:32] honest, I came to this story the
[01:34] expensive way. I had a little side
[01:36] project running, nothing crazy, just an
[01:39] agent that reads documents, summarizes
[01:42] them, and fires off some emails. For the
[01:44] first two weeks, I genuinely thought I
[01:46] was Tony Stark. Then the bill came in,
[01:48] and I was not Tony Stark. I was a guy
[01:50] who'd spent $140 running Claude over a
[01:54] document pipeline that could have been a
[01:55] Python script. Sound familiar?
[01:58] So what does any reasonable person do?
[01:59] At p.m. with my laptop cooking my legs
[02:02] and a cup of tea going cold on the desk,
[02:04] I Googled, how to run AI locally for
[02:07] free. That sent me down a rabbit hole
[02:09] that took like weeks through llama
[02:12] setups, through llama CPP builds that
[02:15] failed three times, and through one
[02:17] quantized model that answered every
[02:19] prompt like a philosophy student having
[02:21] a stroke. And at the end of every one of
[02:23] those roads, you hit the same wall,
[02:25] right? VRAM, the memory on your graphics
[02:28] card, and the reason a model flies on a
[02:31] rented server and types through mud on
[02:33] your three-year-old laptop.
[02:35] So when a $35 rig with 54 gigs of it
[02:38] showed up, I watched pretty much every
[02:40] video about it. And some of them got it
[02:42] right, but a lot of them quietly skipped
[02:44] the part that actually matters to you,
[02:46] which is what this means for the
[02:47] computer you already own. So let's start
[02:49] with the story because honestly, it's
[02:51] one of my favorite internet finds of the
[02:53] year.
[02:54] A guy in Russia buys a garage. Inside
[02:56] the garage, like a relic from a previous
[02:58] civilization, is an old crypto mining
[03:01] farm. Nine graphics cards hanging off a
[03:03] frame in a case that's gone rusty from
[03:06] years of sitting in the damp. The owner
[03:08] lists it on Avito, which if you're not
[03:10] aware, is basically Russia's eBay or
[03:12] Craigslist for 5,000 rubles, so about
[03:15] $60. And he's not even sure it works,
[03:18] and he flat out refuses to let anyone
[03:20] test it before buying.
[03:22] Now, most sensible people walk away at
[03:24] this point, right? A Reddit user called
[03:26] Mark Pruncken did not walk away. He took
[03:29] the guy down to 3,000 rubles, paid
[03:31] blind, dragged the rusty thing home, and
[03:34] booted it off a USB stick because there
[03:36] wasn't even an SSD inside.
[03:38] Did it work? All nine cards came up. He
[03:41] loads Quen 3.6, a 35 billion parameter
[03:44] model, and it runs it over 30 tokens a
[03:47] second, which is faster than most people
[03:49] read.
[03:50] And the math is kind of absurd, right?
[03:52] $35 for 54 gigs is about 65 cents per
[03:55] gigabyte, while a used RTX 3090 with 24
[03:59] gigs was was for a median of around
[04:02] 1,552
[04:04] on eBay over the last 90 days, which is
[04:07] $65 a gig.
[04:09] Same kind of memory 100 times the price.
[04:12] So what did I do? Exactly what you're
[04:14] thinking. I went straight to that place
[04:16] where you're typing P106 mining rig into
[04:19] Google and telling yourself it's an
[04:21] investment. I stayed there for like
[04:23] three days.
[04:25] I made a spreadsheet, I priced out power
[04:27] supplies,
[04:28] and then I read the comments. Because
[04:30] with viral tech posts, the headline is
[04:33] the sizzle, and the truth is buried
[04:35] somewhere around comment 47 posted by
[04:37] someone with a 10-year-old account and
[04:39] no flair who actually knows what they're
[04:41] talking about. This one was no
[04:42] different, and we'll get to what those
[04:44] comments said in a bit because they
[04:47] changed the whole picture. First though,
[04:49] you need to know what these cards
[04:50] actually are. These are NVIDIA P10600s
[04:55] and they came out in mid 2017 right in
[04:58] the middle of the first big crypto boom.
[05:00] NVIDIA took the chip from a GTX 1060, a
[05:03] totally normal gaming card from that
[05:05] era, ripped out every display output,
[05:08] and sold the results straight to miners.
[05:10] No HDMI, no display port. You can't even
[05:13] plug a monitor into one of these. So
[05:15] it's a graphics card that was never
[05:17] meant to show you any graphics. Its
[05:19] whole job from day one was solving
[05:21] hashes for Ethereum as fast as it could.
[05:24] Each card has 6 gigs of GDDR5 on a
[05:27] 192-bit bus running at 8,008 MHz
[05:31] effective. And if we run those numbers,
[05:33] we get about 192 GB per second of memory
[05:36] bandwidth. I want to highlight that one
[05:38] because in about 2 minutes it's going to
[05:39] be the most important number in this
[05:41] video. Each card pulls up to 120 W and
[05:44] there are no tensor cores, which are the
[05:47] dedicated matrix math units NVIDIA
[05:49] started shipping after Pascal and the
[05:51] reason a Turing or Ampere RTX card chews
[05:54] through AI works so efficiently. The
[05:56] P106 is Pascal, so it's doing AI maths
[06:00] on hardware that was designed to do
[06:01] mining maths in 2017. Then on September
[06:04] 15th, 2022, Ethereum switched from proof
[06:08] of work to proof of stake, and
[06:10] overnight, the only reason these cards
[06:12] existed just evaporated. Millions of
[06:15] mining cards suddenly had no job, so
[06:17] they flooded the secondhand market,
[06:19] prices collapsed, and they ended up in
[06:21] crates, in garages, and in the hands of
[06:24] people like Mark Pronkin.
[06:25] So that's the hardware. Nine cards, 54
[06:28] gigs combined, old architecture, no
[06:31] display outputs, cheapest chips. What
[06:34] could possibly go wrong?
[06:36] Hold that thought. We're coming back to
[06:37] it.
[06:38] Okay, here's the part that tripped me up
[06:40] completely when I started with multi-GPU
[06:42] setups, and I think it trips up most
[06:44] people watching videos about this rig.
[06:46] You'd assume nine cards act like one big
[06:49] 54 gig card, right? Everything working
[06:51] at once, the job split nine ways, nine
[06:54] times the speed.
[06:56] Nope.
[06:57] This rig has 54 gigs of memory and
[07:00] roughly the speed of one card. So why
[07:02] one card?
[07:03] Every time a language model writes a
[07:05] token, which is roughly a word, it has
[07:07] to pull its weights out of memory and
[07:10] into the chip. The weights are the
[07:12] billions of numbers that hold everything
[07:14] the model learned. And for a normal
[07:16] model, it has to read all of them for
[07:18] every single token.
[07:20] Now here's the problem. These nine cards
[07:22] are hanging off single lanes of PCI
[07:24] Express 2.0, which is a pretty slow
[07:27] link. So the software splits the job by
[07:29] layers. Card one gets the first chunk of
[07:32] layers, card two gets the next chunk,
[07:34] and so on down to card nine. Card one
[07:37] runs its layers, hands a small result to
[07:39] card two, and waits. Card two does its
[07:42] bit, hands off to card three, and waits.
[07:45] And it goes all the way down the line to
[07:46] card nine, and then the whole thing
[07:48] starts over at card one for the next
[07:51] token. So at any moment, one card is
[07:53] working and eight cards are waiting,
[07:55] which kind of defeats the point of nine
[07:57] cards, right?
[07:58] What this means is you get the memory of
[08:00] all nine cards added together, that big
[08:03] 54, and the bandwidth of exactly one
[08:06] card, 192
[08:08] gigs a second. And that lets us do some
[08:11] really simple division because for a
[08:13] dense model, the kind where every
[08:15] parameter gets used on every token, you
[08:18] just take the model size divided by the
[08:20] bandwidth and that's your speed ceiling.
[08:22] So let's try the obvious test, the
[08:24] biggest model that fits.
[08:26] Llama 3.3 70B at 4-bit is about 42.5
[08:30] gigs. So it fits in 54 with room to
[08:32] spare. That's the dream the headline is
[08:34] selling, right? A 70 billion parameter
[08:37] model on $35 of hardware.
[08:39] But 42.5 divided by 192 gives you a
[08:43] ceiling of about 4.5 tokens a second and
[08:46] in the real world you'd see under three.
[08:48] So a 500 token answer, two or three
[08:50] paragraphs, takes almost three minutes.
[08:53] Three minutes for two paragraphs. I've
[08:55] chatted with people who type slower than
[08:57] that, but that's not the point. The
[08:59] point is the 54 gigs lets you load the
[09:02] model. It doesn't let you enjoy it. So
[09:04] how is he getting 30?
[09:06] The answer's in the model's name. He ran
[09:08] Quen 3.6 35B and the A3B is the bit that
[09:12] matters. This is a mixture of experts
[09:15] model or MOE and honestly I'd argue
[09:18] understanding MOE is the single most
[09:20] useful thing you can learn about local
[09:22] AI right now because it changes how you
[09:24] should think about hardware.
[09:26] A dense model like Llama 3.3 70B uses
[09:29] every parameter in every layer for every
[09:32] token. All 70 billion every time. It's
[09:35] like having 70 billion specialists and
[09:38] dragging every one of them into every
[09:40] meeting, even when most of them have
[09:41] nothing to say.
[09:43] A mixture of experts model still stores
[09:45] all its parameters, 35 billion here,
[09:47] which is the 35B in the name, but inside
[09:50] each of its 40 layers, instead of one
[09:53] big network, there are 256
[09:56] small specialist networks called
[09:58] experts. And a router, which is
[10:00] basically a tiny decision maker, looks
[10:03] at each token and switches on just eight
[10:05] of those 256
[10:07] plus one shared expert that always runs.
[10:10] So, per token, only about three billion
[10:13] parameters actually get read, and the
[10:15] other 32 billion just sit there in
[10:17] memory in case they're needed. It stores
[10:19] 35 billion, but it only reads three,
[10:22] right? At four bit, that's roughly two
[10:25] gigs read per token instead of the 42
[10:27] you'd need for the dense 70B.
[10:30] And 192 gigs a second divided by two
[10:33] gigs a token gives you a ceiling of
[10:35] about 96 tokens a second. Wait. 96? He
[10:40] got 30. That's about a third of the
[10:42] ceiling, and we'll come back to where
[10:43] the rest went because it's actually good
[10:45] news for you. Either way, 30 tokens a
[10:48] second from $35 of hardware. The
[10:50] original write-up had a metaphor for
[10:52] this that I really like.
[10:54] The rig is a massive warehouse with one
[10:57] slow loading dock. If you order
[10:59] everything in the warehouse every day,
[11:01] that dock is your bottleneck. But this
[11:03] model only ever orders a few boxes at a
[11:05] time, so most of the warehouse just sits
[11:07] there, and a slow dock is fine when your
[11:09] orders are small. That's the whole
[11:10] trick. The model is cheap to read, so
[11:13] the slow dock barely matters.
[11:15] And when that clicked, I had a slightly
[11:17] uncomfortable realization because the 54
[11:19] gigs, the thing in the headline and in
[11:22] every single thumbnail, wasn't doing
[11:24] what I thought it was doing.
[11:26] He ran a 23 gig model on a 54 gig rig.
[11:29] That's 31 gigs, about five cards worth,
[11:32] holding nothing at all. So now flip it
[11:35] around. What if you don't have 54 gigs?
[11:38] What if you've got eight gigs of VRAM
[11:40] and 32 gigs of normal system RAM? Can a
[11:42] 23 gig model run on that?
[11:45] This is where most of the videos on this
[11:47] rig buried the lid. Remember, the router
[11:50] picks eight experts out of 256. So in
[11:53] every layer, the other 248 experts are
[11:56] idle for that token. They don't need to
[11:58] live on the GPU, right? They just need
[12:00] to be reachable. And Llama CPP, the free
[12:03] open source engine that O Llama was
[12:05] built on and that sits under most local
[12:07] AI apps, has a flag for exactly this.
[12:10] It's called N CPU MOE, and it keeps the
[12:13] expert weights in your system RAM while
[12:15] the attention layers and the shared
[12:17] weights, the stuff that runs on every
[12:19] single token, stay on the graphics card.
[12:21] Per token, the router picks its eight
[12:23] experts. Your CPU runs those eight
[12:26] straight out of RAM. The card handles
[12:28] everything else and the other 248 never
[12:31] get touched. So an 8 gig card can run a
[12:34] 23 gig model. And not just technically
[12:37] run it, run it fast. On May 11th, a
[12:40] developer called Martin Andrews posted
[12:42] his numbers. His machine was a GTX 1080
[12:45] with 8 gigs, so the same Pascal
[12:47] generation as the P106, a card he picked
[12:49] up second hand for under $200 sitting
[12:52] next to an Intel i7 6700 from 2015 and
[12:56] 32 gigs of RAM. Same model, Qwen 3.6 35B
[13:00] at 4 bit with N CPU MOE set to 30. Over
[13:03] a 2,122 token answer, it wrote 24.94
[13:08] tokens a second. One card, 83% of the
[13:11] nine card rig. Then XDA developers ran
[13:13] it on a Lenovo Legion 5 gaming laptop
[13:16] with a mobile RTX 3070 and 8 gigs of
[13:19] VRAM. Without the flag, four tokens a
[13:21] second. With N CPU MOE at 28, 32.82,
[13:26] faster than the nine card rig on a
[13:28] laptop from one flag.
[13:30] Another developer tried a 12 gig RTX
[13:32] 3060 with 31 gigs of DDR4. Without the
[13:35] flag, it ran out of memory before it
[13:37] even finished loading. With the flag,
[13:41] on a slightly smaller three bit build.
[13:44] And at the top end, someone measured a
[13:46] single used RTX 3090 at 101.7
[13:50] tokens a second on the same model.
[13:53] That's 3.4 times the rig. So here's the
[13:56] leaderboard for the exact model in the
[13:58] headline. The RTX 3060, 23 tokens a
[14:01] second. The 2016 GTX 1080 desktop, 25.
[14:05] The $35 nine card rig, 30. The gaming
[14:08] laptop with a mobile 3070, 33. And
[14:12] 13090, about 100. The rig lands right in
[14:16] middle of hardware most gamers already
[14:18] own.
[14:19] I had two feelings about this list at
[14:20] once, and you might too.
[14:22] Is this disappointing?
[14:24] Or is this kind of amazing?
[14:25] Honestly, it's both. If you've already
[14:28] got a gaming PC with 8 GB of VRAM and 32
[14:31] GB of RAM, you might already own this
[14:33] rig's performance, which is a bit
[14:35] deflating if you were excited about the
[14:36] rig.
[14:37] But a 2015 desktop with a 2016 graphics
[14:40] card running a 35 billion parameter
[14:42] model at 25 tokens a second is wild, and
[14:46] almost nobody knows the flag exists.
[14:48] Now, I've spent a few minutes tearing
[14:50] down the rig's main selling point, so
[14:52] let me be fair. The 54 GB isn't useless.
[14:55] It just isn't what made this thing fast.
[14:57] So what does it actually buy you? Three
[15:00] things that an 8 GB card plus 32 GB of
[15:03] RAM really can match.
[15:05] Number one is higher precision. The same
[15:07] Qwen model at 8-bit gives you noticeably
[15:10] better output, better reasoning, fewer
[15:12] weird hallucinations, and it needs about
[15:15] 38 GB in total.
[15:17] On a 40 GB system that's also running an
[15:19] OS and a browser with 11 tabs open about
[15:21] why your llama CPP build failed,
[15:24] that doesn't fit. On the rig, it does
[15:26] with room to spare.
[15:28] Number two is long context, and this one
[15:30] surprised me.
[15:31] Every token you feed the model, every
[15:33] page of a document, every line of code,
[15:37] every message in the chat takes memory
[15:39] to hold while it's working. That's the
[15:41] KV cache, which is basically the model's
[15:44] short-term memory. So it grows with
[15:46] every token you add, right?
[15:48] On an 8 GB card, a long conversation
[15:50] eats into the room you need for the
[15:52] weights, and eventually stuff spills
[15:54] into RAM or just breaks. On the rig, all
[15:56] of it stays in fast VRAM.
[15:59] One developer estimated that a 65,000
[16:01] token context, think pasting a whole
[16:04] codebase into the chat, takes 10 to 15
[16:07] GB on top of the weights. So that 31 GB
[16:10] of empty VRAM suddenly very occupied. So
[16:13] if you do document analysis, long-form
[16:16] writing, code review across big repos,
[16:19] anything where you feed the model a lot,
[16:21] that spare VRAM is genuinely valuable.
[16:24] Number three is something the buyer
[16:25] mentioned himself, which is nine
[16:27] separate workers.
[16:29] Each P106 has 6 GB and reads at 192 GB a
[16:33] second when it isn't waiting on its
[16:35] neighbors. Split the work right, nine
[16:37] small jobs in parallel instead of one
[16:39] long chain, and you've got nine decent
[16:41] little workers going at once. That's
[16:43] less run the biggest model and more run
[16:46] lots of things at once, and his plan
[16:48] points that way. He wants to move the
[16:49] cards into a bigger 12-slot case with a
[16:52] proper CPU and add three more cards,
[16:54] which takes it to 72 GB. Those are real
[16:56] uses. They're not the use in the
[16:58] thumbnail, but they're not nothing.
[17:00] Okay, remember comment 47? Here's where
[17:03] I get nitpicky, and I'm not sorry,
[17:05] because this is what separates a useful
[17:07] tech video from a dopamine dispenser and
[17:09] a trench coat. Almost every video on
[17:11] this rig quoted the same two numbers,
[17:14] and nobody actually measured either of
[17:16] them. The first is about 400 tokens a
[17:18] second for reading your prompt, which is
[17:20] called prefill.
[17:22] It sounds plausible, right? Nine cards,
[17:25] decent raw compute, and prompt reading
[17:27] leans on raw maths more than bandwidth.
[17:30] But here's the problem. Pascal has no
[17:32] tensor cores, so the units that make
[17:34] modern cards blaze through that maths
[17:36] just aren't there. And nobody has
[17:38] measured prefill on this rig. It's a
[17:40] guess that turned into a fact by being
[17:42] repeated. I've seen it quoted in videos
[17:44] like it's settled. It isn't. The second
[17:47] is 150 W at idle. Measured? Nope. The
[17:51] one person in the thread who did
[17:53] measure, someone with two P102,
[17:56] the 10 GB cousin of the P106, reported 7
[18:00] W per card sitting idle, which times
[18:02] nine is 63 W, not 150. And that matters
[18:07] because power is the running cost that
[18:09] decides whether local AI actually saves
[18:12] you money, right?
[18:14] So let's do the real numbers. Nine cards
[18:16] at 7 W is 63 W. Leave it on for a month,
[18:20] which is 730 hours, and that's 46
[18:23] kilowatt hours. And at the US average
[18:25] home rate of about 18 cents, that's
[18:26] about $8.35 a month for the rig to sit
[18:30] there doing nothing. In California, it's
[18:32] closer to $14. Now add actual use. With
[18:35] the layer split running, one card works
[18:38] at up to 120 watts, while the other
[18:40] eight idle. So call it 176 watts for the
[18:43] cards while it's riding. And remember,
[18:45] that's a ceiling, not a measurement. At
[18:47] 30 tokens a second, a million tokens
[18:50] takes about 9.26 hours, and 176 watts
[18:54] for 9.26 hours is 1.63 kilowatt hours,
[18:58] which works out to about 30 cents per
[19:00] million output tokens. So how does that
[19:02] compare to just paying someone? Open
[19:05] Router lists this exact model at about
[19:07] 90 cents per million output tokens from
[19:09] most providers and as low as 10 cents
[19:12] from the cheapest one right now. So
[19:13] writing on the rig is cheaper if you're
[19:15] paying for power, right? 30 cents versus
[19:17] 90. But here's the kicker, and the
[19:19] spreadsheet only shows it when you
[19:20] squint. That $8.35 idle bill at the US
[19:24] average buys you about 9.3 million
[19:27] output tokens at 90 cents a million.
[19:30] That's the rig writing nonstop,
[19:32] literally nonstop, for 86 hours a month
[19:35] just to break even on standby. A heavy
[19:37] chat user might put out a couple of
[19:39] million output tokens a month. At that
[19:41] rate, you'd spend $2 on a hosted API and
[19:44] over $8 keeping the rig awake. Not
[19:47] great. If you run agents all day, the
[19:49] rig writes for hours at a stretch, your
[19:52] power's cheap, and the math flips your
[19:54] way. If you use it for an hour in the
[19:55] evening and then go to bed, switch it
[19:57] off at the wall. And again, the 8 gig
[20:00] card in your desktop is already plugged
[20:02] in and already on your bill. It doesn't
[20:04] cost you anything extra to do AI work.
[20:06] Now you might be asking, Kai, why not
[20:09] just do what every other video said?
[20:11] Because almost all of them ended the
[20:12] same way. If you're not in Russia, buy a
[20:15] Tesla P100 or a P40 instead. Data center
[20:19] cards with more memory and similar cheap
[20:21] prices secondhand. Sounds reasonable,
[20:23] right?
[20:24] So here's what happened to those prices
[20:26] after the videos came out.
[20:28] According to GPU Dojo's price tracker,
[20:30] on August 28th, the cheapest 16 gig
[20:33] Tesla P100 was $79.97.
[20:38] By November 13th, about two and a half
[20:40] months later, it was $219.99.
[20:45] That's 2.75 times higher.
[20:48] The 24 gig P40 went from $239 to
[20:51] $383.90,
[20:54] up 61%.
[20:56] The 32 gig V100 went from $650 to
[20:59] $1,039.
[21:01] There's a comment with 179 likes that
[21:04] basically writes the epitaph for every
[21:06] cheap AI hardware video, and I'll
[21:08] paraphrase it.
[21:09] Every time a video shows cheap hardware
[21:11] running AI, that hardware stops being
[21:14] cheap. The P106 themselves are still
[21:16] cheap in the US, for now. Single cards
[21:19] list for about $20 to $60, and there's
[21:22] apparently a lot of 24 going for $499,
[21:26] which is about $21 a card. So nine of
[21:29] those is around $189 for the cards
[21:32] alone.
[21:33] But the board, the frame, nine PCIe
[21:35] risers, and power supplies that can
[21:38] handle a 1,080 watt ceiling are all
[21:40] extra.
[21:41] That's what the $35 hides. He bought a
[21:44] finished rig, right? You'd be building
[21:46] one, and piece by piece with new parts,
[21:49] you are nowhere near $35 anymore.
[21:52] So if you still want to do this, copy
[21:54] what the buyer did. Search your local
[21:56] listings for a whole mining farm, not
[21:58] single cards, because the frame and the
[22:00] power supplies are where a from scratch
[22:02] build gets expensive fast.
[22:04] And plan to run it headless. No display
[22:06] outputs means you need a board with
[22:08] built-in graphics or another machine to
[22:10] connect from. And remember, what could
[22:13] possibly go wrong? Here's the other
[22:15] thing. Nvidia has said the 580 driver
[22:17] branch is the last one that supports
[22:19] Pascal, which is the architecture these
[22:21] cards are built on. CUDA 13 has already
[22:24] dropped offline compilation for anything
[22:26] below compute capability 7.5 and the
[22:28] P106 is 6.1. Security updates for the
[22:32] 580 branch run through October 2028
[22:35] according to Tom's Hardware. After that,
[22:37] nothing new. Today it mostly works fine.
[22:39] Olama ships a CUDA 12 runner that
[22:41] handles these cards and Lama CPP still
[22:44] builds for Pascal against CUDA 12. The
[22:46] community advice is basically to pin
[22:48] your driver, stop it auto updating,
[22:51] stick to the Q4 and Q8 quant formats
[22:53] that use the 8-bit integer path, and
[22:56] stay away from anything heavy on half
[22:57] precision maths because on Pascal half
[23:00] precision runs at 1/64th of full speed.
[23:04] 64th. That's not a typo. So you've got
[23:07] roughly two years of runway with a fence
[23:09] at the end and after 2028 things get
[23:12] uncertain.
[23:13] The GTX 1080 from earlier is in exactly
[23:15] the same boat, Pascal being Pascal.
[23:18] For a $35 rig that paid for itself on
[23:20] day one, two more years is a great
[23:22] return, right? If you're building from
[23:24] scratch right now, factor in that
[23:26] timeline. So should you buy one? I want
[23:28] to give you a straight answer and not a
[23:30] hedge. There's one person this rig is
[23:32] exactly right for and it's the guy who
[23:34] bought it. Why him? His electricity is
[23:37] included in his rent and even if it
[23:38] weren't, he says power is cheap where he
[23:41] lives. P106 and their 10 gig cousins go
[23:44] for $10 to $20 locally. He wanted
[23:47] unlimited use, long context, and privacy
[23:51] and he doesn't want an AI agent reading
[23:53] his messages through someone else's
[23:54] server while he pays for the privilege.
[23:56] For him, almost every cost in this video
[23:59] is basically zero. A complete rig for
[24:02] $35, free power, room to run a bigger
[24:05] model at 8-bit with 65,000 tokens of
[24:08] context, all fully local. That's a great
[24:11] purchase. And the same logic works for
[24:13] you if all of this is true. You find a
[24:15] complete working rig near scrap price
[24:18] and I mean complete. So cards, frame,
[24:21] board, power supply, everything. Your
[24:24] power is cheap, included, or you'll run
[24:26] it enough to cover standby. You're fine
[24:28] on Linux with hardware that has no
[24:30] display outputs,
[24:31] and you specifically need what 54 gigs
[24:33] gives you, which is eight-bit precision,
[24:36] very long context, or lots of small jobs
[24:39] in parallel.
[24:40] If those don't all apply, your upgrade
[24:42] probably isn't a mining rig. It might be
[24:44] better RAM, it might be a machine where
[24:46] the CPU and GPU share one unified pool
[24:49] of memory, and there are some options
[24:51] going that way. Or it might just be
[24:52] turning on one flag and finding out you
[24:55] already have what you need.
[24:56] So, would running it locally have saved
[24:59] me that $140?
[25:01] Yes, just not on a mining rig.
[25:03] Don't buy a mining rig to run the model
[25:05] in this headline. Run it on what you've
[25:07] got first. So, what do you actually do
[25:09] tonight? Here are the steps so you can
[25:11] skip the three days of forum diving I
[25:13] did. If your desktop has an eight-gig
[25:15] NVIDIA card and 32 gigs of RAM, you
[25:18] probably already own the rig's 30 tokens
[25:20] a second, right?
[25:22] It's sitting right there, and the only
[25:23] thing missing is the flag. Step one,
[25:26] install llama cpp. Why not olama?
[25:29] Because n cpu moe is a llama cpp flag,
[25:33] so you want llama cpp directly. The XDA
[25:35] Developers article on this model is a
[25:37] solid reference because they ran it
[25:39] clean with and without the flag and
[25:41] published the numbers properly. Step
[25:43] two, grab a four-bit build of Quinn 3.6
[25:47] 35 B. Unsloth's builds are the most
[25:49] popular and well maintained.
[25:51] The download's about 23 gigs, so clear
[25:53] some space and set n cpu moe to 30 to
[25:57] start. Step three, run llama bench,
[26:00] which is the benchmark tool built into
[26:02] llama cpp instead of a does this feel
[26:05] fast vibe check? Run it three times with
[26:07] the flag and three times without because
[26:09] one run can be noisy, and compare the
[26:11] generation tokens per second. Step four,
[26:14] if you're on olama and want to stay
[26:16] there, run olama ps before anything
[26:19] else. If it shows part of your model
[26:21] sitting on the CPU, you're already
[26:23] paying the speed cost of not using the
[26:24] flag, you just don't know it. Step five,
[26:28] still under 20 tokens a second and you
[26:30] think it should be
[26:31] Check your RAM before you look at
[26:32] graphics cards. The experts get read
[26:34] from system RAM, right? So if you're
[26:36] running one stick in single channel
[26:38] instead of two, you're leaving a lot of
[26:40] bandwidth on the table. Two sticks in
[26:42] dual channel on an older Intel platform
[26:44] can double it. That's a free upgrade if
[26:46] you've got a spare stick in a drawer.
[26:48] Only once you know what your current
[26:49] hardware actually does does it make
[26:51] sense to think about new hardware. And
[26:53] when you do, price it by what the model
[26:55] reads per token, not by what the card
[26:57] holds. That's the number that sets your
[26:59] speed.
[27:00] Which brings us back to the missing
[27:02] tokens. The math said 96 and he got 30.
[27:06] But look at what that 30 came off. A
[27:08] 2017 architecture, nine cards handing
[27:11] every token down a chain of single lane
[27:13] PCIe links, a Celeron with a few gigs of
[27:16] RAM, a default Ollama install booted
[27:19] from USB with zero tuning.
[27:22] My guess is those nine handoffs eat a
[27:24] big chunk of the gap, but nobody's
[27:26] tested that properly yet, so treat it as
[27:29] a guess. And that's the good news for
[27:30] you because your one card doesn't have
[27:33] nine handoffs, which is part of why a
[27:34] single GTX 1080 gets to 25. So the
[27:38] number that made this rig fast was the
[27:40] three, the 3 billion parameters it reads
[27:43] per token, never the 54. And I think
[27:46] that's the useful bit under all the
[27:47] hardware talk. Right now, almost every
[27:49] hardware conversation in AI is about how
[27:51] much you can hold. VRAM, parameters,
[27:55] context windows, gigabytes. Those
[27:58] numbers make great thumbnails, right?
[28:00] The question that actually decides fast
[28:02] or slow, cheap or expensive is how much
[28:05] you have to read. Mixture of experts is
[28:07] shaking up local AI precisely because it
[28:10] splits those two apart. So a 35 billion
[28:12] parameter model only reads 3 billion per
[28:15] token. Once that clicks, a lot of
[28:17] hardware you wrote off as two weeks
[28:19] starts looking a lot more capable. And
[28:21] my API build problem solved. I'm running
[28:23] my pipeline locally now on a machine I
[28:25] already owned. Not a flashy rig, not a
[28:28] $35 garage find, just a desktop with an
[28:31] 8 gig card, 32 gigs of RAM, and one flag
[28:34] in a config file. It does 25 tokens a
[28:37] second, which is the same as a nine
[28:39] card, 54 gig $35 mining rig. I did still
[28:44] make a spreadsheet about it. Old habits.
[28:46] Anyway, that's it for this one. If this
[28:49] helped you figure out your setup,
[28:50] subscribe because I do a lot of these
[28:52] where we go past the headline and find
[28:54] out what's real. And if you try this,
[28:56] drop a comment with your card and the
[28:58] number you get after you turn on the
[29:00] flag.
[29:00] I want to build a leaderboard out of
[29:02] real numbers instead of theoretical
[29:04] ones. See you in the next one.