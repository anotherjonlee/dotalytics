# DOTA: Character Selections and Match Performances
## Table of Content
- [Introduction](#introduction)
- [EDA](#eda)
- [Hypothesis Testing](#hypothesis-testing)
- [Further Investigation](#further-investigation)
- [Conclusion](#conclusion)
- [Looking Forward](#future)
- [Side Note](#side-note)

## Introduction
The Defense of the Ancients (Dota) was released as a mod of a video game Warcraft III in 2003 and the sequel Dota 2 was released in 2013 as a standalone version by Valve. To this day the developer is pushing out multiple patches to maintain the balance of the gameplay and as a result, it continues to attract a significant number of players in spite of its age.

![image](img/dota_players_n.png)
<sup><sub>from [steamcharts](https://steamcharts.com/app/570) as of April 10, 2020</sub></sup>

Dota is a multiplyer online battle arena(moba) where 2 teams of up to 5 players will compete to destroy each other's main base, the Ancient. Throughout the match the players will be dueling each others and each kill they score would ultimately result in increase in the characters' attributes via leveling up and acquisition of superior items.


For this analysis I'll be investigating whether players' character selections and the game performance measured in the number of kills per match would have any relationships.

## EDA
The original dataset contains match results between March 2011 to March 2016, containing over 37 million rows representing a number of kills, deaths, and other information from professional to amateur players.

I knew from the start that my computer would not be able to handle the entire dataset and had to come up with a way to take a smaller sample from this dataset.

Luckily I used the following UNIX command to grab samller subset of this dataset so that I didn't have to try loading it first on Jupyter Notebook via Spark or Pandas.

`cat input.txt | awk 'BEGIN {srand()} !/^$/ { if (rand() <= insert_your_desired_percentage_in_decimal) print $0}' > sample.txt`

Upon sampling 3%, or 0.03 in decimal, from the original dataset, I ended up with a little over a million rows of data to work with. 

After loading the much smaller sample on Spark to run a number queries, exporting the queried data to Pandas, I recognized that around 15% of the sampled players finished the match playing as Pudge, Sniper, Drow Ranger, Riki and Phantom Assassin out of the pool of 111 playable charcters.
![img](/img/pie.png)

Hmm... These 5 characters must be offering an edge to players over other characters. I'm going to assume that no player is playing to lose, which means I can gauge the player performance by taking a look at the number of kills per match. Let's take a look at the distribution of kills per match by two groups: the aforementioned 5 character group (the top 5) and the rest (the rest):

![img](/img/init_dist.png)

The distribution of kills/match for both group definitely does not look normal, but they at least appear to have a similar distribution.

Let's take a deeper look into the distribution without the outliers just for the sake of gettig a rough idea of both groups' kills/match distribution.

![img](/img/box.png)

The variance for the top 5 is noticeably wider than the rest, but the distribution between the first and the third quartiles and the median are not too far apart. 

We will perform a hypothesis testing and see if choosing a character from the top 5 would give a player a statistically significant edge over other characters.

## Hypothesis Testing
Let's go ahead and set up our null and alternate hypotheses:

**Null Hypothesis**: Choosing one of the five most popular characters does not affect the number of kills per match.

**Alternate Hypothesis**: The number of kills per match we can expect from the top 5 is not equal to the number kills per match we can expect from the rest of the playable characters.

We know from the law of large numbers that the distribution of the sample mean would take a normal distribution and we have a fairly large sample, so I'll go ahead and apply a Welch's t-test. 

Why Welch's instead of the Student's? Well the Student's t-test assumes that the variance is the same, which in my case, it is not. 

```python
_, pval = stats.ttest_ind(df_top5['kills'],df_rest['kills'],equal_var=False)
print(f'The p-value from the Welch T test is: {pval}')
```
> The p-value from the Welch T test is: 0.0

Based on the p-value, we are going to reject the null hypothesis and conclude that there is a difference in kills/match when we choose a character in the top 5 group.

## Further Investigation
Hmm... Even though the distribution of the kills/match between the top-5 and the rest groups did not look drastically different at first sight, the Welch's t-test indicates that their difference is in fact statistically significant. 

I'll use the Central Limit Theorem (CLT) to explain what is going on. The CLT asserts that the larger the samples we have, the more the distribution of sample means become normally distributed. 

With over 140,000 data points for the top-5 and 860,000 for the rest, we can safely assume that the distribution of our sample means will be normally distributed. 

Let's go ahead and plot both of our sample mean distribution using the following formula:
```python
y = stats.norm(mean,std)/sqrt(n))
```
![img](/img/dist.png)

Because our sample size is so large, the standard error of the sample mean becomes extremely small to a point where both distributions do not overlap at all. 

Specifically, the 95% confidence interval for the top-5 group is 7.77 and 7.87, while the 95% confidence interval for the other group is 5.68 and 5.7, which means that it is extremely unlikely to observe top-5 characters scoring the same or less number of kills per match compared to the other group.

## Looking Forward
During the initial I noticed that Valve had assigned multiple roles to each of the game characters. The individual character attributes are calibrated to maximize the assigned roles and as such, we can somewhat predict players' actions based on the chosen characters' roles. For example, 4 out of the 5 most popular characters had a role of Carry and 3 out of 5 had the Disabler role as you can see below.


|Heroes|Roles|Popularity|
|---|---|---|
|Pudge|Disabler,Initiator, Durable, Nuker|1|
|Sniper|Carry,Nuker|2|
|Drow Ranger|Carry,Disabler,Pusher|3|
|Riki|Carry,Escape,Disabler|4|
|Phantom Assassin|Carry,Escape|5|


Unfortunately I did not have enough time to investigate the relationship between the roles, the character performance and character selections. This is something I would like to continue exploring, as players may be choosing a character over another because they perfer certain roles.

If you would like to learn more about the complete list of available roles and their attributes, check them out below:
* [Carry](https://dota2.gamepedia.com/Role#Carry)
* [Support](https://dota2.gamepedia.com/Role#Support)
* [Nuker](https://dota2.gamepedia.com/Role#Nuker)
* [Disabler](https://dota2.gamepedia.com/Role#Disabler)
* [Jungler](https://dota2.gamepedia.com/Role#Jungler)
* [Durable](https://dota2.gamepedia.com/Role#Durable)
* [Escape](https://dota2.gamepedia.com/Role#Escape)
* [Pusher](https://dota2.gamepedia.com/Role#Pusher)
* [Initiator](https://dota2.gamepedia.com/Role#Initiator)

## Side Note
I would like to thank [@odota](https://blog.opendota.com/2017/03/24/datadump2/) and [@waprin](https://github.com/waprin) for preparing and making the data freely available for this analysis. Without their efforts, I wouldn't have been able to collect the data.