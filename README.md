# FinalProject

you're now reading my readme.md file 
So let me introduce my program 

First of all, my project is about a trading bot for crypto currencies because I really love this topic and creating a trading bot is a good way to rediscover this environment from a new perspective.

After looking for information regarding the trading bot and the different trading methods I understood the complexities of the project. In fact the difficulty of the programme lies in the trading strategy and the way we develop it. To do so we first need to create a program where we test our strategy. We call this program the backtest file. It’s only when our backtest program works correctly we have to implement our code and create the trading bot.  


After defining my strategy, I code it and try to find if it was profitable or not. As soon as my strategy became theoretically profitable I started to code it. Below, you can see the results of my strategy and you can compare it with “hold” strategy 

![Screenshot_Backtest](https://user-images.githubusercontent.com/113576613/206872520-9cf52277-a0cd-4c14-a312-5d59ead58ee0.png)

![Screenshot_Backtest_Analysis](https://user-images.githubusercontent.com/113576613/206872541-e0b59c3a-1fa7-4339-aecf-129c7f49d219.png)

So now let’s go deeper to the final project code itself. The program here automatically trades a pair of cryptocurrencies by following a predefined strategy and notify you on your device about the different position he takes . So you can buy/long and sell/short and be aware about what’s Happening. To do so I use the Bitget exchange because they provide documentation regarding their api and they give you a sub-account in order to let you try different strategies.


To run the bot there are different things to do before, First you need to generate your own api key from Bitget and implement it in the code.Then you need to calibrate correctly the values of the different indicators to get optimal trades(default settings are not optimal and can’t gives you the same results as me). Also, you have to generate your telegram bot to be notified about your position. Finally, you have to find a way to automatically run the code.
here an example of a message you may receive once you finish to calibrate the bot.

![Screenshot_Notification](https://user-images.githubusercontent.com/113576613/206872622-867946d3-75bb-4ec7-b993-085378a0b8c5.png)

There is no perfect program so here are some bugs that may happen:
-If you run the code several times in a short period of time the code may bug and not running
-you can receive the same message several times
-even if the code run, sometimes nothing happen (it might be normal because of Bitget but i’m not sure)


To conclude this readme I’d like to inform you about the way I learn how to do the bot. 
To do my backtest and my trading bot I was inspired by the code of the youtuber/programmer  “Crypto robot” who explains on the internet how to do a trading bot . 
