# Evaluation Report

生成时间:2026-09-23 18:57:27

## 总体对比

| Mode | N | Sentiment Acc | Keyword Hit | Off-topic Rec | p50 (s) | p95 (s) | Subs avg | Cited |
|---|---|---|---|---|---|---|---|---|
| single_shot | 50 | 58% | 45% | 20% | 1.99 | 2.64 | 0 | 137 |
| agent | 50 | 68% | 75% | 100% | 3.51 | 4.61 | 2.16 | 171 |
| agent_reflect | 50 | 74% | 76% | 100% | 5.55 | 8.66 | 2.92 | 180 |

## 单题结果(按模式)

### mode = single_shot

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 0 | 2.31s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | pos | 1/2 | 0 | 1.94s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | pos | 3/3 | 0 | 2.4s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 1/3 | 0 | 2.64s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 1/3 | 0 | 2.48s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | mix | 2/3 | 0 | 2.03s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | neg | 1/3 | 0 | 1.99s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 0 | 2.01s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 0 | 2.51s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | pos | 1/3 | 0 | 1.9s |
| 11 | ELDEN RING | Is Elden Ring worth buying? | pos | pos | 2/2 | 0 | 3.46s |
| 12 | ELDEN RING | How is the open world explorat... | pos | pos | 3/3 | 0 | 1.63s |
| 13 | ELDEN RING | Are the boss fights good? | pos | pos | 1/2 | 0 | 1.58s |
| 14 | ELDEN RING | Is it too difficult for casual... | mix | mix | 3/3 | 0 | 2.01s |
| 15 | ELDEN RING | How is the multiplayer and co-... | mix | mix | 2/3 | 0 | 2.58s |
| 16 | ELDEN RING | How deep is the lore? | pos | mix | 0/3 | 0 | 1.51s |
| 17 | ELDEN RING | Are there performance and stut... | mix | mix | 2/3 | 0 | 2.15s |
| 18 | ELDEN RING | How long is the game? | pos | ? | 0/3 | 0 | 0.0s |
| 19 | ELDEN RING | How is the magic system? | pos | ? | 0/3 | 0 | 0.0s |
| 20 | ELDEN RING | Is it good for newcomers to so... | mix | pos | 3/3 | 0 | 1.95s |
| 21 | Red Dead Redemption  | Is RDR2 worth buying? | pos | mix | 2/2 | 0 | 2.98s |
| 22 | Red Dead Redemption  | How is the story? | pos | pos | 1/3 | 0 | 1.97s |
| 23 | Red Dead Redemption  | How is the open world? | pos | pos | 1/3 | 0 | 1.58s |
| 24 | Red Dead Redemption  | How is the online mode? | neg | mix | 0/3 | 0 | 1.97s |
| 25 | Red Dead Redemption  | How is the shooting gameplay? | mix | pos | 1/3 | 0 | 2.2s |
| 26 | Red Dead Redemption  | Are there bugs and glitches? | mix | neg | 2/3 | 0 | 2.44s |
| 27 | Red Dead Redemption  | How long is the main story? | pos | pos | 3/3 | 0 | 1.44s |
| 28 | Red Dead Redemption  | How is the character developme... | pos | pos | 1/3 | 0 | 1.91s |
| 29 | Red Dead Redemption  | Is Rockstar's monetization fai... | neg | mix | 1/3 | 0 | 1.67s |
| 30 | Red Dead Redemption  | How is the horse riding? | pos | pos | 1/3 | 0 | 2.18s |
| 31 | Black Myth: Wukong | Hello there! | mix | pos | 0/1 | 0 | 2.58s |
| 32 | Black Myth: Wukong | 你是来拉屎的吧 | mix | pos | 0/1 | 0 | 2.42s |
| 33 | Black Myth: Wukong | Who are you? | mix | pos | 0/1 | 0 | 1.41s |
| 34 | Black Myth: Wukong | What's the weather today? | mix | mix | 0/1 | 0 | 1.25s |
| 35 | Black Myth: Wukong | Tell me a joke | mix | mix | 0/1 | 0 | 1.93s |
| 36 | Black Myth: Wukong | How do I cook pasta? | mix | mix | 0/1 | 0 | 1.36s |
| 37 | Black Myth: Wukong | 你好啊 | mix | pos | 0/1 | 0 | 2.22s |
| 38 | Black Myth: Wukong | What is the meaning of life? | mix | pos | 0/1 | 0 | 2.23s |
| 39 | Black Myth: Wukong | 你是谁 | mix | mix | 1/1 | 0 | 1.52s |
| 40 | Black Myth: Wukong | What's 2+2? | mix | mix | 0/1 | 0 | 1.3s |
| 41 | Black Myth: Wukong | How is the combat AND the stor... | mix | pos | 1/2 | 0 | 2.17s |
| 42 | Black Myth: Wukong | Is this game perfect? Any majo... | mix | pos | 0/3 | 0 | 2.24s |
| 43 | Black Myth: Wukong | Should I buy it on PC or wait ... | mix | mix | 2/3 | 0 | 2.17s |
| 44 | Black Myth: Wukong | Is the DLC worth buying? | mix | mix | 2/2 | 0 | 1.82s |
| 45 | Black Myth: Wukong | Will I enjoy this if I never p... | mix | pos | 1/3 | 0 | 1.93s |
| 46 | Black Myth: Wukong | How is the soundtrack? | pos | pos | 1/2 | 0 | 2.14s |
| 47 | Black Myth: Wukong | Is it suitable for kids? | mix | mix | 0/2 | 0 | 1.78s |
| 48 | Black Myth: Wukong | Any tips for beginners? | mix | mix | 3/3 | 0 | 1.29s |
| 49 | ELDEN RING | How is it compared to Dark Sou... | mix | pos | 1/3 | 0 | 2.27s |
| 50 | Red Dead Redemption  | How active are the online serv... | mix | neg | 2/3 | 0 | 2.02s |

### mode = agent

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 3 | 5.03s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | mix | 2/2 | 3 | 4.51s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | mix | 3/3 | 3 | 3.95s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 2/3 | 2 | 4.27s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 2/3 | 2 | 4.16s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | mix | 2/3 | 3 | 3.37s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 3/3 | 3 | 3.67s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 3 | 2.93s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 3 | 4.02s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | pos | 1/3 | 3 | 3.26s |
| 11 | ELDEN RING | Is Elden Ring worth buying? | pos | pos | 2/2 | 3 | 3.87s |
| 12 | ELDEN RING | How is the open world explorat... | pos | pos | 3/3 | 3 | 3.16s |
| 13 | ELDEN RING | Are the boss fights good? | pos | mix | 2/2 | 3 | 4.21s |
| 14 | ELDEN RING | Is it too difficult for casual... | mix | pos | 3/3 | 3 | 2.97s |
| 15 | ELDEN RING | How is the multiplayer and co-... | mix | pos | 2/3 | 2 | 3.67s |
| 16 | ELDEN RING | How deep is the lore? | pos | pos | 2/3 | 3 | 2.95s |
| 17 | ELDEN RING | Are there performance and stut... | mix | mix | 2/3 | 2 | 3.85s |
| 18 | ELDEN RING | How long is the game? | pos | pos | 3/3 | 3 | 3.51s |
| 19 | ELDEN RING | How is the magic system? | pos | mix | 0/3 | 3 | 1.07s |
| 20 | ELDEN RING | Is it good for newcomers to so... | mix | mix | 0/3 | 3 | 1.18s |
| 21 | Red Dead Redemption  | Is RDR2 worth buying? | pos | mix | 2/2 | 3 | 5.11s |
| 22 | Red Dead Redemption  | How is the story? | pos | pos | 1/3 | 3 | 3.69s |
| 23 | Red Dead Redemption  | How is the open world? | pos | pos | 2/3 | 3 | 3.67s |
| 24 | Red Dead Redemption  | How is the online mode? | neg | mix | 1/3 | 3 | 3.34s |
| 25 | Red Dead Redemption  | How is the shooting gameplay? | mix | pos | 2/3 | 3 | 4.03s |
| 26 | Red Dead Redemption  | Are there bugs and glitches? | mix | neg | 3/3 | 3 | 3.64s |
| 27 | Red Dead Redemption  | How long is the main story? | pos | pos | 3/3 | 2 | 2.66s |
| 28 | Red Dead Redemption  | How is the character developme... | pos | pos | 1/3 | 3 | 3.94s |
| 29 | Red Dead Redemption  | Is Rockstar's monetization fai... | neg | neg | 2/3 | 3 | 3.83s |
| 30 | Red Dead Redemption  | How is the horse riding? | pos | pos | 1/3 | 2 | 3.75s |
| 31 | Black Myth: Wukong | Hello there! | mix | mix | 1/1 | 0 | 0.89s |
| 32 | Black Myth: Wukong | 你是来拉屎的吧 | mix | mix | 1/1 | 0 | 0.81s |
| 33 | Black Myth: Wukong | Who are you? | mix | mix | 1/1 | 0 | 1.15s |
| 34 | Black Myth: Wukong | What's the weather today? | mix | mix | 1/1 | 0 | 1.08s |
| 35 | Black Myth: Wukong | Tell me a joke | mix | mix | 1/1 | 0 | 1.13s |
| 36 | Black Myth: Wukong | How do I cook pasta? | mix | mix | 1/1 | 0 | 1.33s |
| 37 | Black Myth: Wukong | 你好啊 | mix | mix | 1/1 | 0 | 1.28s |
| 38 | Black Myth: Wukong | What is the meaning of life? | mix | mix | 1/1 | 0 | 0.93s |
| 39 | Black Myth: Wukong | 你是谁 | mix | mix | 1/1 | 0 | 1.12s |
| 40 | Black Myth: Wukong | What's 2+2? | mix | mix | 1/1 | 0 | 1.23s |
| 41 | Black Myth: Wukong | How is the combat AND the stor... | mix | mix | 2/2 | 2 | 3.49s |
| 42 | Black Myth: Wukong | Is this game perfect? Any majo... | mix | mix | 0/3 | 2 | 4.4s |
| 43 | Black Myth: Wukong | Should I buy it on PC or wait ... | mix | mix | 2/3 | 3 | 4.61s |
| 44 | Black Myth: Wukong | Is the DLC worth buying? | mix | pos | 2/2 | 3 | 4.19s |
| 45 | Black Myth: Wukong | Will I enjoy this if I never p... | mix | pos | 3/3 | 3 | 3.91s |
| 46 | Black Myth: Wukong | How is the soundtrack? | pos | mix | 2/2 | 3 | 3.44s |
| 47 | Black Myth: Wukong | Is it suitable for kids? | mix | mix | 0/2 | 3 | 3.87s |
| 48 | Black Myth: Wukong | Any tips for beginners? | mix | mix | 0/3 | 0 | 1.13s |
| 49 | ELDEN RING | How is it compared to Dark Sou... | mix | pos | 2/3 | 3 | 3.82s |
| 50 | Red Dead Redemption  | How active are the online serv... | mix | neg | 3/3 | 2 | 3.21s |

### mode = agent_reflect

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | mix | 2/3 | 3 | 5.81s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | pos | 2/2 | 3 | 5.1s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | mix | 2/3 | 5 | 8.1s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | pos | 1/3 | 2 | 5.66s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 1/3 | 3 | 4.94s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 3/3 | 3 | 6.67s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 3/3 | 3 | 4.84s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 3 | 5.94s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 2 | 7.92s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | pos | 2/3 | 5 | 8.58s |
| 11 | ELDEN RING | Is Elden Ring worth buying? | pos | pos | 2/2 | 5 | 7.65s |
| 12 | ELDEN RING | How is the open world explorat... | pos | pos | 3/3 | 5 | 6.42s |
| 13 | ELDEN RING | Are the boss fights good? | pos | mix | 2/2 | 3 | 5.45s |
| 14 | ELDEN RING | Is it too difficult for casual... | mix | mix | 3/3 | 5 | 5.57s |
| 15 | ELDEN RING | How is the multiplayer and co-... | mix | pos | 2/3 | 4 | 6.85s |
| 16 | ELDEN RING | How deep is the lore? | pos | pos | 2/3 | 5 | 6.51s |
| 17 | ELDEN RING | Are there performance and stut... | mix | mix | 2/3 | 2 | 4.88s |
| 18 | ELDEN RING | How long is the game? | pos | pos | 3/3 | 5 | 5.87s |
| 19 | ELDEN RING | How is the magic system? | pos | mix | 0/3 | 3 | 1.26s |
| 20 | ELDEN RING | Is it good for newcomers to so... | mix | pos | 3/3 | 3 | 5.55s |
| 21 | Red Dead Redemption  | Is RDR2 worth buying? | pos | mix | 2/2 | 3 | 4.95s |
| 22 | Red Dead Redemption  | How is the story? | pos | pos | 0/3 | 3 | 4.42s |
| 23 | Red Dead Redemption  | How is the open world? | pos | pos | 2/3 | 4 | 6.54s |
| 24 | Red Dead Redemption  | How is the online mode? | neg | mix | 1/3 | 3 | 4.43s |
| 25 | Red Dead Redemption  | How is the shooting gameplay? | mix | pos | 2/3 | 5 | 8.69s |
| 26 | Red Dead Redemption  | Are there bugs and glitches? | mix | mix | 3/3 | 5 | 8.64s |
| 27 | Red Dead Redemption  | How long is the main story? | pos | pos | 3/3 | 4 | 5.55s |
| 28 | Red Dead Redemption  | How is the character developme... | pos | pos | 2/3 | 4 | 7.02s |
| 29 | Red Dead Redemption  | Is Rockstar's monetization fai... | neg | neg | 2/3 | 5 | 8.91s |
| 30 | Red Dead Redemption  | How is the horse riding? | pos | pos | 1/3 | 2 | 4.79s |
| 31 | Black Myth: Wukong | Hello there! | mix | mix | 1/1 | 0 | 1.1s |
| 32 | Black Myth: Wukong | 你是来拉屎的吧 | mix | mix | 1/1 | 0 | 1.01s |
| 33 | Black Myth: Wukong | Who are you? | mix | mix | 1/1 | 0 | 0.99s |
| 34 | Black Myth: Wukong | What's the weather today? | mix | mix | 1/1 | 0 | 1.08s |
| 35 | Black Myth: Wukong | Tell me a joke | mix | mix | 1/1 | 0 | 1.16s |
| 36 | Black Myth: Wukong | How do I cook pasta? | mix | mix | 1/1 | 0 | 1.3s |
| 37 | Black Myth: Wukong | 你好啊 | mix | mix | 1/1 | 0 | 1.01s |
| 38 | Black Myth: Wukong | What is the meaning of life? | mix | mix | 1/1 | 0 | 1.07s |
| 39 | Black Myth: Wukong | 你是谁 | mix | mix | 1/1 | 0 | 0.95s |
| 40 | Black Myth: Wukong | What's 2+2? | mix | mix | 1/1 | 0 | 1.21s |
| 41 | Black Myth: Wukong | How is the combat AND the stor... | mix | mix | 1/2 | 2 | 5.09s |
| 42 | Black Myth: Wukong | Is this game perfect? Any majo... | mix | mix | 1/3 | 3 | 5.18s |
| 43 | Black Myth: Wukong | Should I buy it on PC or wait ... | mix | mix | 2/3 | 5 | 8.66s |
| 44 | Black Myth: Wukong | Is the DLC worth buying? | mix | mix | 2/2 | 5 | 7.6s |
| 45 | Black Myth: Wukong | Will I enjoy this if I never p... | mix | pos | 2/3 | 3 | 5.24s |
| 46 | Black Myth: Wukong | How is the soundtrack? | pos | pos | 2/2 | 3 | 6.79s |
| 47 | Black Myth: Wukong | Is it suitable for kids? | mix | mix | 1/2 | 5 | 5.91s |
| 48 | Black Myth: Wukong | Any tips for beginners? | mix | mix | 0/3 | 0 | 1.28s |
| 49 | ELDEN RING | How is it compared to Dark Sou... | mix | pos | 2/3 | 5 | 7.92s |
| 50 | Red Dead Redemption  | How active are the online serv... | mix | neg | 3/3 | 5 | 7.22s |

## 失败题(sentiment 错或 keyword 漏)

### single_shot (41 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → missed: ['boss']
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['chapter|章节', 'chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['performance|性能', 'fps|帧率']
- **Q6** Is the game too difficult?  → missed: ['souls|魂']
- **Q7** Are there bugs and technical issues?  → sentiment: negative != mixed; missed: ['bugs|bug', 'glitches|bug']
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → missed: ['price|价格', 'value|价值']
- **Q13** Are the boss fights good?  → missed: ['fight|战斗']
- **Q15** How is the multiplayer and co-op?  → missed: ['online|在线']
- **Q16** How deep is the lore?  → sentiment: mixed != positive; missed: ['lore|背景', 'story|故事', 'dark|黑暗']
- **Q17** Are there performance and stuttering issues?  → missed: ['fps|帧率']
- **Q18** How long is the game?  → sentiment: ? != positive; missed: ['hours|小时', 'finish|通关', 'length|时长']
- **Q19** How is the magic system?  → sentiment: ? != positive; missed: ['magic|魔法', 'sorcery|魔法', 'build']
- **Q20** Is it good for newcomers to souls games?  → sentiment: positive != mixed

### agent (33 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → sentiment: mixed != positive
- **Q3** Are the boss fights well-designed?  → sentiment: mixed != positive
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['fps|帧率']
- **Q6** Is the game too difficult?  → missed: ['souls|魂']
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → missed: ['value|价值', 'worth|值得']
- **Q13** Are the boss fights good?  → sentiment: mixed != positive
- **Q14** Is it too difficult for casual players?  → sentiment: positive != mixed
- **Q15** How is the multiplayer and co-op?  → sentiment: positive != mixed; missed: ['online|在线']
- **Q16** How deep is the lore?  → missed: ['dark|黑暗']
- **Q17** Are there performance and stuttering issues?  → missed: ['fps|帧率']
- **Q19** How is the magic system?  → sentiment: mixed != positive; missed: ['magic|魔法', 'sorcery|魔法', 'build']
- **Q20** Is it good for newcomers to souls games?  → missed: ['newcomers|新手', 'souls|魂', 'friendly|友好']

### agent_reflect (29 题)

- **Q1** Is this game worth buying?  → sentiment: mixed != positive; missed: ['money|金钱']
- **Q3** Are the boss fights well-designed?  → sentiment: mixed != positive; missed: ['fight|战斗']
- **Q4** How is the story and plot?  → missed: ['chapter|章节', 'chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['performance|性能', 'fps|帧率']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → missed: ['value|价值']
- **Q13** Are the boss fights good?  → sentiment: mixed != positive
- **Q15** How is the multiplayer and co-op?  → sentiment: positive != mixed; missed: ['online|在线']
- **Q16** How deep is the lore?  → missed: ['dark|黑暗']
- **Q17** Are there performance and stuttering issues?  → missed: ['fps|帧率']
- **Q19** How is the magic system?  → sentiment: mixed != positive; missed: ['magic|魔法', 'sorcery|魔法', 'build']
- **Q20** Is it good for newcomers to souls games?  → sentiment: positive != mixed
- **Q21** Is RDR2 worth buying?  → sentiment: mixed != positive
- **Q22** How is the story?  → missed: ['story|故事', 'arthur|亚瑟', 'emotional|感人']
