# AI_2048
AI playable CLI based 2048 game.

**Requirements**: pynput module
Install by this command:

    $ pip install pynput

**Run game**:

    $ python main.py <mode> <ai_level>   

#mode 0 : AI plays, mode 1: Manual Gameplay, ai_level in [1,10)

**Probability of 2048 score**

    On 2nd level AI: 20% +
    On 4th level AI: 50% +

![](https://github.com/vicrobot/AI_2048/blob/master/2048_4.gif)

![](https://github.com/vicrobot/AI_2048/blob/master/2048.gif)

**AI Stats: Month: Feb 2020**

For AI_level = 1

|    |   score |   time(in s) |
|---:|--------:|-------------:|
|  0 |     256 |     0.671742 |
|  1 |     256 |     0.587555 |
|  2 |     128 |     0.22611  |
|  3 |     256 |     0.505664 |
|  4 |     256 |     0.645824 |
|  5 |     256 |     0.560919 |


For AI_level = 2

|    |   score |   time(in s) |
|---:|--------:|-------------:|
|  0 |    1024 |      7.54256 |
|  1 |    1024 |      6.92184 |
|  2 |    2048 |     11.7421  |
|  3 |    1024 |      9.18748 |
|  4 |    2048 |     12.4448  |


For AI_level = 3

|    |   score |   time(in s) |
|---:|--------:|-------------:|
|  0 |    1024 |      37.2067 |
|  1 |    1024 |      32.8945 |
|  2 |    1024 |      34.6505 |
|  3 |    1024 |      37.568  |
|  4 |    1024 |      35.9973 |


For AI_level = 4


|    |   score |   time(in s) |
|---:|--------:|-------------:|
|  0 |    2048 |      266.027 |
|  1 |    1024 |      165.674 |
|  2 |    2048 |      237.149 |
|  3 |    1024 |      174.447 |
|  4 |    2048 |      237.1   |
