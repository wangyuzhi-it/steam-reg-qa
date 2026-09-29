# Evaluation Report

生成时间:2026-09-23 18:48:40

## 总体对比

| Mode | N | Sentiment Acc | Keyword Hit | Off-topic Rec | p50 (s) | p95 (s) | Subs avg | Cited |
|---|---|---|---|---|---|---|---|---|
| single_shot | 50 | 62% | 41% | - | 2.22 | 6.78 | 0 | 138 |
| agent | 50 | 68% | 79% | - | 3.79 | 5.17 | 2.16 | 180 |
| agent_reflect | 50 | 68% | 75% | - | 5.47 | 9.35 | 2.94 | 183 |

## 单题结果(按模式)

### mode = single_shot

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 0 | 2.12s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | mix | 1/2 | 0 | 1.73s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | pos | 3/3 | 0 | 2.43s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 1/3 | 0 | 2.57s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 1/3 | 0 | 2.0s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 2/3 | 0 | 1.8s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 1/3 | 0 | 1.94s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 0 | 2.29s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 0 | 2.34s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | pos | 1/3 | 0 | 1.7s |
| 11 | ELDEN RING | Is Elden Ring worth buying? | pos | pos | 2/2 | 0 | 3.01s |
| 12 | ELDEN RING | How is the open world explorat... | pos | pos | 3/3 | 0 | 2.13s |
| 13 | ELDEN RING | Are the boss fights good? | pos | pos | 1/2 | 0 | 1.7s |
| 14 | ELDEN RING | Is it too difficult for casual... | mix | mix | 3/3 | 0 | 2.64s |
| 15 | ELDEN RING | How is the multiplayer and co-... | mix | neg | 2/3 | 0 | 2.7s |
| 16 | ELDEN RING | How deep is the lore? | pos | pos | 0/3 | 0 | 1.28s |
| 17 | ELDEN RING | Are there performance and stut... | mix | mix | 2/3 | 0 | 2.25s |
| 18 | ELDEN RING | How long is the game? | pos | ? | 0/3 | 0 | 0.0s |
| 19 | ELDEN RING | How is the magic system? | pos | ? | 0/3 | 0 | 0.0s |
| 20 | ELDEN RING | Is it good for newcomers to so... | mix | pos | 1/3 | 0 | 2.22s |
| 21 | Red Dead Redemption  | Is RDR2 worth buying? | pos | mix | 2/2 | 0 | 3.13s |
| 22 | Red Dead Redemption  | How is the story? | pos | pos | 1/3 | 0 | 1.68s |
| 23 | Red Dead Redemption  | How is the open world? | pos | pos | 1/3 | 0 | 1.9s |
| 24 | Red Dead Redemption  | How is the online mode? | neg | mix | 0/3 | 0 | 2.19s |
| 25 | Red Dead Redemption  | How is the shooting gameplay? | mix | pos | 1/3 | 0 | 2.29s |
| 26 | Red Dead Redemption  | Are there bugs and glitches? | mix | mix | 2/3 | 0 | 2.55s |
| 27 | Red Dead Redemption  | How long is the main story? | pos | pos | 3/3 | 0 | 2.15s |
| 28 | Red Dead Redemption  | How is the character developme... | pos | pos | 1/3 | 0 | 2.34s |
| 29 | Red Dead Redemption  | Is Rockstar's monetization fai... | neg | neg | 1/3 | 0 | 1.93s |
| 30 | Red Dead Redemption  | How is the horse riding? | pos | pos | 1/3 | 0 | 2.53s |
| 31 | Black Myth: Wukong | Hello there! | mix | pos | 0/1 | 0 | 1.92s |
| 32 | Black Myth: Wukong | 你是来拉屎的吧 | mix | mix | 0/1 | 0 | 2.58s |
| 33 | Black Myth: Wukong | Who are you? | mix | mix | 0/1 | 0 | 1.54s |
| 34 | Black Myth: Wukong | What's the weather today? | mix | mix | 0/1 | 0 | 0.96s |
| 35 | Black Myth: Wukong | Tell me a joke | mix | mix | 0/1 | 0 | 2.63s |
| 36 | Black Myth: Wukong | How do I cook pasta? | mix | mix | 0/1 | 0 | 1.27s |
| 37 | Black Myth: Wukong | 你好啊 | mix | pos | 0/1 | 0 | 3.03s |
| 38 | Black Myth: Wukong | What is the meaning of life? | mix | pos | 0/1 | 0 | 2.34s |
| 39 | Black Myth: Wukong | 你是谁 | mix | mix | 0/1 | 0 | 1.43s |
| 40 | Black Myth: Wukong | What's 2+2? | mix | pos | 0/1 | 0 | 1.23s |
| 41 | Black Myth: Wukong | How is the combat AND the stor... | mix | pos | 1/2 | 0 | 2.43s |
| 42 | Black Myth: Wukong | Is this game perfect? Any majo... | mix | pos | 0/3 | 0 | 2.27s |
| 43 | Black Myth: Wukong | Should I buy it on PC or wait ... | mix | mix | 2/3 | 0 | 2.64s |
| 44 | Black Myth: Wukong | Is the DLC worth buying? | mix | mix | 2/2 | 0 | 7.49s |
| 45 | Black Myth: Wukong | Will I enjoy this if I never p... | mix | pos | 1/3 | 0 | 2.08s |
| 46 | Black Myth: Wukong | How is the soundtrack? | pos | pos | 1/2 | 0 | 2.48s |
| 47 | Black Myth: Wukong | Is it suitable for kids? | mix | mix | 0/2 | 0 | 32.62s |
| 48 | Black Myth: Wukong | Any tips for beginners? | mix | mix | 3/3 | 0 | 4.23s |
| 49 | ELDEN RING | How is it compared to Dark Sou... | mix | pos | 1/3 | 0 | 1.78s |
| 50 | Red Dead Redemption  | How active are the online serv... | mix | neg | 2/3 | 0 | 6.78s |

### mode = agent

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 3 | 4.76s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | mix | 2/2 | 3 | 5.57s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | mix | 3/3 | 3 | 4.16s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 1/3 | 3 | 4.84s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 2/3 | 2 | 3.79s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 3/3 | 3 | 4.42s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 3/3 | 3 | 3.9s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 3 | 3.63s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 2 | 4.16s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | mix | 1/3 | 3 | 3.15s |
| 11 | ELDEN RING | Is Elden Ring worth buying? | pos | pos | 2/2 | 3 | 2.95s |
| 12 | ELDEN RING | How is the open world explorat... | pos | pos | 3/3 | 2 | 4.13s |
| 13 | ELDEN RING | Are the boss fights good? | pos | mix | 2/2 | 3 | 3.74s |
| 14 | ELDEN RING | Is it too difficult for casual... | mix | mix | 3/3 | 3 | 3.99s |
| 15 | ELDEN RING | How is the multiplayer and co-... | mix | pos | 2/3 | 2 | 3.37s |
| 16 | ELDEN RING | How deep is the lore? | pos | pos | 2/3 | 3 | 3.53s |
| 17 | ELDEN RING | Are there performance and stut... | mix | mix | 2/3 | 2 | 4.48s |
| 18 | ELDEN RING | How long is the game? | pos | pos | 3/3 | 3 | 3.4s |
| 19 | ELDEN RING | How is the magic system? | pos | mix | 0/3 | 3 | 1.42s |
| 20 | ELDEN RING | Is it good for newcomers to so... | mix | pos | 3/3 | 3 | 4.14s |
| 21 | Red Dead Redemption  | Is RDR2 worth buying? | pos | mix | 2/2 | 3 | 4.96s |
| 22 | Red Dead Redemption  | How is the story? | pos | pos | 1/3 | 3 | 3.82s |
| 23 | Red Dead Redemption  | How is the open world? | pos | pos | 1/3 | 2 | 3.3s |
| 24 | Red Dead Redemption  | How is the online mode? | neg | mix | 1/3 | 3 | 4.73s |
| 25 | Red Dead Redemption  | How is the shooting gameplay? | mix | mix | 2/3 | 3 | 3.57s |
| 26 | Red Dead Redemption  | Are there bugs and glitches? | mix | neg | 3/3 | 3 | 5.17s |
| 27 | Red Dead Redemption  | How long is the main story? | pos | pos | 3/3 | 2 | 3.3s |
| 28 | Red Dead Redemption  | How is the character developme... | pos | pos | 2/3 | 3 | 4.93s |
| 29 | Red Dead Redemption  | Is Rockstar's monetization fai... | neg | neg | 2/3 | 3 | 9.45s |
| 30 | Red Dead Redemption  | How is the horse riding? | pos | pos | 2/3 | 3 | 3.79s |
| 31 | Black Myth: Wukong | Hello there! | mix | mix | 1/1 | 0 | 1.47s |
| 32 | Black Myth: Wukong | 你是来拉屎的吧 | mix | mix | 1/1 | 0 | 0.9s |
| 33 | Black Myth: Wukong | Who are you? | mix | mix | 1/1 | 0 | 1.03s |
| 34 | Black Myth: Wukong | What's the weather today? | mix | mix | 1/1 | 0 | 1.16s |
| 35 | Black Myth: Wukong | Tell me a joke | mix | mix | 1/1 | 0 | 1.2s |
| 36 | Black Myth: Wukong | How do I cook pasta? | mix | mix | 1/1 | 0 | 1.07s |
| 37 | Black Myth: Wukong | 你好啊 | mix | mix | 1/1 | 0 | 1.15s |
| 38 | Black Myth: Wukong | What is the meaning of life? | mix | mix | 1/1 | 0 | 1.28s |
| 39 | Black Myth: Wukong | 你是谁 | mix | mix | 1/1 | 0 | 1.31s |
| 40 | Black Myth: Wukong | What's 2+2? | mix | mix | 1/1 | 0 | 1.01s |
| 41 | Black Myth: Wukong | How is the combat AND the stor... | mix | pos | 2/2 | 2 | 4.88s |
| 42 | Black Myth: Wukong | Is this game perfect? Any majo... | mix | mix | 0/3 | 2 | 4.13s |
| 43 | Black Myth: Wukong | Should I buy it on PC or wait ... | mix | mix | 3/3 | 3 | 4.85s |
| 44 | Black Myth: Wukong | Is the DLC worth buying? | mix | mix | 2/2 | 3 | 4.22s |
| 45 | Black Myth: Wukong | Will I enjoy this if I never p... | mix | pos | 2/3 | 3 | 3.79s |
| 46 | Black Myth: Wukong | How is the soundtrack? | pos | mix | 2/2 | 3 | 4.27s |
| 47 | Black Myth: Wukong | Is it suitable for kids? | mix | mix | 2/2 | 3 | 3.11s |
| 48 | Black Myth: Wukong | Any tips for beginners? | mix | mix | 0/3 | 0 | 1.13s |
| 49 | ELDEN RING | How is it compared to Dark Sou... | mix | pos | 2/3 | 3 | 4.41s |
| 50 | Red Dead Redemption  | How active are the online serv... | mix | mix | 3/3 | 3 | 2.97s |

### mode = agent_reflect

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 3 | 5.47s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | mix | 2/2 | 3 | 5.28s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | mix | 2/3 | 5 | 7.63s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | pos | 1/3 | 2 | 6.02s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 3/3 | 4 | 6.55s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 3/3 | 3 | 5.87s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | neg | 3/3 | 3 | 5.08s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 3 | 4.84s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 2 | 5.11s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | mix | 1/3 | 5 | 6.32s |
| 11 | ELDEN RING | Is Elden Ring worth buying? | pos | pos | 2/2 | 5 | 7.41s |
| 12 | ELDEN RING | How is the open world explorat... | pos | mix | 3/3 | 5 | 6.56s |
| 13 | ELDEN RING | Are the boss fights good? | pos | mix | 1/2 | 3 | 4.49s |
| 14 | ELDEN RING | Is it too difficult for casual... | mix | mix | 3/3 | 5 | 7.07s |
| 15 | ELDEN RING | How is the multiplayer and co-... | mix | pos | 2/3 | 4 | 6.08s |
| 16 | ELDEN RING | How deep is the lore? | pos | mix | 0/3 | 5 | 6.2s |
| 17 | ELDEN RING | Are there performance and stut... | mix | mix | 2/3 | 2 | 5.76s |
| 18 | ELDEN RING | How long is the game? | pos | pos | 3/3 | 5 | 5.84s |
| 19 | ELDEN RING | How is the magic system? | pos | mix | 0/3 | 3 | 1.2s |
| 20 | ELDEN RING | Is it good for newcomers to so... | mix | pos | 3/3 | 3 | 4.56s |
| 21 | Red Dead Redemption  | Is RDR2 worth buying? | pos | mix | 2/2 | 5 | 9.35s |
| 22 | Red Dead Redemption  | How is the story? | pos | pos | 1/3 | 5 | 7.23s |
| 23 | Red Dead Redemption  | How is the open world? | pos | pos | 2/3 | 4 | 5.89s |
| 24 | Red Dead Redemption  | How is the online mode? | neg | mix | 1/3 | 3 | 4.74s |
| 25 | Red Dead Redemption  | How is the shooting gameplay? | mix | pos | 2/3 | 3 | 5.1s |
| 26 | Red Dead Redemption  | Are there bugs and glitches? | mix | mix | 3/3 | 5 | 7.67s |
| 27 | Red Dead Redemption  | How long is the main story? | pos | pos | 3/3 | 4 | 7.36s |
| 28 | Red Dead Redemption  | How is the character developme... | pos | pos | 1/3 | 2 | 4.7s |
| 29 | Red Dead Redemption  | Is Rockstar's monetization fai... | neg | neg | 3/3 | 5 | 10.15s |
| 30 | Red Dead Redemption  | How is the horse riding? | pos | pos | 2/3 | 4 | 8.67s |
| 31 | Black Myth: Wukong | Hello there! | mix | mix | 1/1 | 0 | 1.08s |
| 32 | Black Myth: Wukong | 你是来拉屎的吧 | mix | mix | 1/1 | 0 | 1.06s |
| 33 | Black Myth: Wukong | Who are you? | mix | mix | 1/1 | 0 | 0.94s |
| 34 | Black Myth: Wukong | What's the weather today? | mix | mix | 1/1 | 0 | 1.15s |
| 35 | Black Myth: Wukong | Tell me a joke | mix | mix | 1/1 | 0 | 0.93s |
| 36 | Black Myth: Wukong | How do I cook pasta? | mix | mix | 1/1 | 0 | 1.36s |
| 37 | Black Myth: Wukong | 你好啊 | mix | mix | 1/1 | 0 | 1.54s |
| 38 | Black Myth: Wukong | What is the meaning of life? | mix | mix | 1/1 | 0 | 1.05s |
| 39 | Black Myth: Wukong | 你是谁 | mix | mix | 1/1 | 0 | 1.44s |
| 40 | Black Myth: Wukong | What's 2+2? | mix | mix | 1/1 | 0 | 1.16s |
| 41 | Black Myth: Wukong | How is the combat AND the stor... | mix | mix | 2/2 | 2 | 5.43s |
| 42 | Black Myth: Wukong | Is this game perfect? Any majo... | mix | mix | 2/3 | 4 | 9.93s |
| 43 | Black Myth: Wukong | Should I buy it on PC or wait ... | mix | mix | 3/3 | 5 | 8.9s |
| 44 | Black Myth: Wukong | Is the DLC worth buying? | mix | mix | 2/2 | 5 | 7.39s |
| 45 | Black Myth: Wukong | Will I enjoy this if I never p... | mix | pos | 1/3 | 3 | 4.62s |
| 46 | Black Myth: Wukong | How is the soundtrack? | pos | pos | 2/2 | 3 | 6.75s |
| 47 | Black Myth: Wukong | Is it suitable for kids? | mix | mix | 1/2 | 5 | 5.94s |
| 48 | Black Myth: Wukong | Any tips for beginners? | mix | mix | 0/3 | 0 | 0.93s |
| 49 | ELDEN RING | How is it compared to Dark Sou... | mix | pos | 1/3 | 5 | 7.4s |
| 50 | Red Dead Redemption  | How active are the online serv... | mix | mix | 0/3 | 2 | 1.15s |

## 失败题(sentiment 错或 keyword 漏)

### single_shot (42 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → sentiment: mixed != positive; missed: ['boss']
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['chapter|章节', 'chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['performance|性能', 'fps|帧率']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed; missed: ['souls|魂']
- **Q7** Are there bugs and technical issues?  → missed: ['bugs|bug', 'glitches|bug']
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → missed: ['price|价格', 'value|价值']
- **Q13** Are the boss fights good?  → missed: ['fight|战斗']
- **Q15** How is the multiplayer and co-op?  → sentiment: negative != mixed; missed: ['online|在线']
- **Q16** How deep is the lore?  → missed: ['lore|背景', 'story|故事', 'dark|黑暗']
- **Q17** Are there performance and stuttering issues?  → missed: ['fps|帧率']
- **Q18** How long is the game?  → sentiment: ? != positive; missed: ['hours|小时', 'finish|通关', 'length|时长']
- **Q19** How is the magic system?  → sentiment: ? != positive; missed: ['magic|魔法', 'sorcery|魔法', 'build']
- **Q20** Is it good for newcomers to souls games?  → sentiment: positive != mixed; missed: ['newcomers|新手', 'friendly|友好']

### agent (29 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → sentiment: mixed != positive
- **Q3** Are the boss fights well-designed?  → sentiment: mixed != positive
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['chapter|章节', 'chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['fps|帧率']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → sentiment: mixed != positive; missed: ['value|价值', 'worth|值得']
- **Q13** Are the boss fights good?  → sentiment: mixed != positive
- **Q15** How is the multiplayer and co-op?  → sentiment: positive != mixed; missed: ['online|在线']
- **Q16** How deep is the lore?  → missed: ['dark|黑暗']
- **Q17** Are there performance and stuttering issues?  → missed: ['fps|帧率']
- **Q19** How is the magic system?  → sentiment: mixed != positive; missed: ['magic|魔法', 'sorcery|魔法', 'build']
- **Q20** Is it good for newcomers to souls games?  → sentiment: positive != mixed
- **Q21** Is RDR2 worth buying?  → sentiment: mixed != positive

### agent_reflect (28 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → sentiment: mixed != positive
- **Q3** Are the boss fights well-designed?  → sentiment: mixed != positive; missed: ['fight|战斗']
- **Q4** How is the story and plot?  → missed: ['chapter|章节', 'chinese|中国']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed
- **Q7** Are there bugs and technical issues?  → sentiment: negative != mixed
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → sentiment: mixed != positive; missed: ['value|价值', 'worth|值得']
- **Q12** How is the open world exploration?  → sentiment: mixed != positive
- **Q13** Are the boss fights good?  → sentiment: mixed != positive; missed: ['fight|战斗']
- **Q15** How is the multiplayer and co-op?  → sentiment: positive != mixed; missed: ['online|在线']
- **Q16** How deep is the lore?  → sentiment: mixed != positive; missed: ['lore|背景', 'story|故事', 'dark|黑暗']
- **Q17** Are there performance and stuttering issues?  → missed: ['fps|帧率']
- **Q19** How is the magic system?  → sentiment: mixed != positive; missed: ['magic|魔法', 'sorcery|魔法', 'build']
- **Q20** Is it good for newcomers to souls games?  → sentiment: positive != mixed
