# AI_2048
AI playable CLI based 2048 game.

**Requirements**:
Install by this command:

    $ pip3 install -r requirements.txt

Game uses cython for speedups.

Setups:

**On Linux**

    $ python setup.py build_ext --inplace
or see [this](https://www.youtube.com/watch?v=SB9UgjJFFUk) video for linux.

**On Windows**

Read [this](https://github.com/cython/cython/wiki/InstallingOnWindows) guide and set cython in your system.
Installing cython is done by requirements.txt
Then run:

    $ python setup.py build_ext --inplace
-----------------------------------------------------
**Game command**; 

    $ python main.py <mode> <ai_level>

Here Mode is 1 for manual play, no need for AI level specification.
For AI, put mode on 0 and specify AI level > 1 and integer.

Ex; 
For AI level 200 gameplay

    $ python main.py 0 200 
 
For manual gameplay

    $ python main.py 1
