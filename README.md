# Software Engineering-2016 Spring
We are team H, our team members are: [Yihuan Dong](https://github.com/YihuanDong), [Niki Gitinabard](https://github.com/nikign), [Linting Xue](https://github.com/lintingting), [Rui Zhi](https://github.com/boyzhirui).


##Git Helper
###Solution 1: Git Helper Search Engine
 [Git Helper](http://git-helper-2016.appspot.com/) search engine specifically for git error based on [stackover flow](http://stackoverflow.com/). We use [Google](https://www.google.com/) search [stackover flow](http://stackoverflow.com/) with git error, retuned linkes are sorted based machine learning methodolgy. Web content are tokenlized and evaluted by the tifidf value of error message of each webpage and stackoverflow votes. At the end [Git Helper](http://git-helper-2016.appspot.com/) will return top 10 best result.
###Solution 2: Git Helper Auto-reply System 
Auto-reply E-mail system to provide user the best solution with mail address: git_helper@yahoo.com. The best solution will be the top answswer from our own search engine. 
###Solution 3: Command Line Helper
An Command line helper based on decsion tree. It can detect git errors in real time and provide concrete step by step solutions to guide user. 

##March 1
      
  1. [Issues page](https://github.com/nikign/Git-Helper/issues)

  2. [Milestone page](https://github.com/nikign/Git-Helper/milestones)
  
  3. [Contributor's page](https://github.com/nikign/Git-Helper/graphs/contributors)
  
  4. [Weekly meeting notes](https://docs.google.com/document/d/1B0bfH9u6K8n0BKwULQ4N0RwhgxjLjaZ81rrlhxGOmp4/edit)
  
  5. [Sample log links (csv format)](https://github.com/nikign/Git-Helper/blob/master/git_helper/decision_tree/log.csv)
      
  6. [Evaluation plan](https://github.com/nikign/Git-Helper/issues/44)
  7. Report: http://bit.ly/1qaXc4a
  8. Presentation: http://bit.ly/1MiWfRH

We plan to evaluate our three solutions in March. Before conducting the experiment, we will continue improving our tools and do system testings.  During the first and second weeks of March, we plan to build a repository with three common git errors novice user may face (including conflict errors and merge errors). 

After that, we’ll conduct our experiment on NCSU undergraduate students in CSC-216 course (around 80 students in each session). For the experiment, we plan to come up with a list of basic git commands representing a sequence of actions that novice user might use in their daily work. When performing certain commands in the list, student will face errors. The participants will be asked to correct the error with the help of either one of our tools or the Google search engine. We will split the participants into four groups, with three experimental group and one control group. For the three experimental groups, each group will be assigned to one of our solution tools. And the control group are free to use google search engine or whatever they want to solve the git errors. A pre survey will be conducted to ask about student's skill level before the experiment and a post survey will be conducted asking about their experience using the tool.

For the experiment, we plan to come up with a list of basic git commands representing a sequence of actions that novice user might use in their daily work. When performing certain commands in the list, student will face errors. Students will be asked to use our tools to resolve the errors to keep on working. Data like the commands they performed, the timestamp, the error they're facing, etc will be recorded in a log file for further analysis. 

In the analysis part, we're considering using "time used to solve problem", "user satisfaction", etc to compare between the tools and determine which tool is better. A more detailed evaluation criterial will be designed before the deadline of the first milestone of March.
