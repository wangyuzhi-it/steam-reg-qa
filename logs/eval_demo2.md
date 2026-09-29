# Evaluation Report

生成时间:2026-09-23 18:38:57

## 总体对比

| Mode | N | Sentiment Acc | Keyword Hit | Off-topic Rec | p50 (s) | p95 (s) | Subs avg | Cited |
|---|---|---|---|---|---|---|---|---|
| single_shot | 10 | 60% | 63% | - | 2.15 | 2.54 | 0 | 36 |
| agent | 10 | 50% | 77% | - | 3.9 | 4.87 | 2.8 | 53 |

## 单题结果(按模式)

### mode = single_shot

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 0 | 2.19s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | mix | 2/2 | 0 | 2.08s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | pos | 3/3 | 0 | 2.54s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 1/3 | 0 | 2.31s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 1/3 | 0 | 2.15s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 2/3 | 0 | 1.94s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | neg | 1/3 | 0 | 2.2s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 0 | 2.23s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 0 | 2.07s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | pos | 1/3 | 0 | 1.8s |

### mode = agent

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 2/3 | 3 | 4.17s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | mix | 2/2 | 3 | 4.48s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | mix | 3/3 | 3 | 3.9s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 1/3 | 2 | 4.08s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 2/3 | 2 | 2.87s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 3/3 | 3 | 3.51s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 3/3 | 3 | 4.05s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 2/3 | 3 | 3.59s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 3/3 | 3 | 4.87s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | mix | 1/3 | 3 | 3.82s |

## 失败题(sentiment 错或 keyword 漏)

### single_shot (8 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → sentiment: mixed != positive
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['chapter|章节', 'chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['performance|性能', 'fps|帧率']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed; missed: ['souls|魂']
- **Q7** Are there bugs and technical issues?  → sentiment: negative != mixed; missed: ['bugs|bug', 'glitches|bug']
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → missed: ['price|价格', 'value|价值']

### agent (8 题)

- **Q1** Is this game worth buying?  → missed: ['money|金钱']
- **Q2** How is the combat system?  → sentiment: mixed != positive
- **Q3** Are the boss fights well-designed?  → sentiment: mixed != positive
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['chapter|章节', 'chinese|中国']
- **Q5** How is the optimization on PC?  → missed: ['fps|帧率']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed
- **Q8** How long does it take to beat the game?  → missed: ['chapter|章节']
- **Q10** Is it good value for money?  → sentiment: mixed != positive; missed: ['value|价值', 'worth|值得']
