# Evaluation Report

生成时间:2026-09-23 18:37:35

## 总体对比

| Mode | N | Sentiment Acc | Keyword Hit | Off-topic Rec | p50 (s) | p95 (s) | Subs avg | Cited |
|---|---|---|---|---|---|---|---|---|
| single_shot | 10 | 90% | 3% | - | 2.38 | 3.58 | 0 | 37 |
| agent | 10 | 60% | 22% | - | 3.85 | 5.58 | 2.7 | 50 |

## 单题结果(按模式)

### mode = single_shot

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 0/3 | 0 | 2.44s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | pos | 0/2 | 0 | 1.75s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | pos | 1/3 | 0 | 2.38s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 0/3 | 0 | 3.58s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 0/3 | 0 | 2.54s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | mix | 0/3 | 0 | 1.95s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 0/3 | 0 | 2.56s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 0/3 | 0 | 2.15s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 0/3 | 0 | 2.98s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | pos | 0/3 | 0 | 1.94s |

### mode = agent

| ID | Game | Question | Expect | Got | KW | Sub | Time |
|---|---|---|---|---|---|---|---|
| 1 | Black Myth: Wukong | Is this game worth buying? | pos | pos | 1/3 | 3 | 4.17s |
| 2 | Black Myth: Wukong | How is the combat system? | pos | pos | 1/2 | 2 | 3.6s |
| 3 | Black Myth: Wukong | Are the boss fights well-desig... | pos | mix | 2/3 | 3 | 4.13s |
| 4 | Black Myth: Wukong | How is the story and plot? | pos | mix | 0/3 | 3 | 4.23s |
| 5 | Black Myth: Wukong | How is the optimization on PC? | mix | mix | 2/3 | 2 | 3.24s |
| 6 | Black Myth: Wukong | Is the game too difficult? | mix | pos | 0/3 | 3 | 5.58s |
| 7 | Black Myth: Wukong | Are there bugs and technical i... | mix | mix | 0/3 | 3 | 3.85s |
| 8 | Black Myth: Wukong | How long does it take to beat ... | pos | pos | 0/3 | 3 | 3.38s |
| 9 | Black Myth: Wukong | How is the graphics and visual... | pos | pos | 0/3 | 2 | 3.97s |
| 10 | Black Myth: Wukong | Is it good value for money? | pos | mix | 0/3 | 3 | 2.98s |

## 失败题(sentiment 错或 keyword 漏)

### single_shot (10 题)

- **Q1** Is this game worth buying?  → missed: ['worth', 'buy', 'money']
- **Q2** How is the combat system?  → missed: ['combat', 'boss']
- **Q3** Are the boss fights well-designed?  → missed: ['fight', 'design']
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['story', 'chapter', 'chinese']
- **Q5** How is the optimization on PC?  → missed: ['optimization', 'performance', 'fps']
- **Q6** Is the game too difficult?  → missed: ['difficult', 'hard', 'souls']
- **Q7** Are there bugs and technical issues?  → missed: ['bugs', 'crash', 'glitches']
- **Q8** How long does it take to beat the game?  → missed: ['hours', 'chapter', 'length']
- **Q9** How is the graphics and visuals?  → missed: ['graphics', 'visuals', 'beautiful']
- **Q10** Is it good value for money?  → missed: ['price', 'value', 'worth']

### agent (10 题)

- **Q1** Is this game worth buying?  → missed: ['buy', 'money']
- **Q2** How is the combat system?  → missed: ['combat']
- **Q3** Are the boss fights well-designed?  → sentiment: mixed != positive; missed: ['design']
- **Q4** How is the story and plot?  → sentiment: mixed != positive; missed: ['story', 'chapter', 'chinese']
- **Q5** How is the optimization on PC?  → missed: ['fps']
- **Q6** Is the game too difficult?  → sentiment: positive != mixed; missed: ['difficult', 'hard', 'souls']
- **Q7** Are there bugs and technical issues?  → missed: ['bugs', 'crash', 'glitches']
- **Q8** How long does it take to beat the game?  → missed: ['hours', 'chapter', 'length']
- **Q9** How is the graphics and visuals?  → missed: ['graphics', 'visuals', 'beautiful']
- **Q10** Is it good value for money?  → sentiment: mixed != positive; missed: ['price', 'value', 'worth']
