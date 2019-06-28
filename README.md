# Artificial Intelligence

![artwork1](https://user-images.githubusercontent.com/25236592/60368707-f20d2480-99c7-11e9-8f0e-c748fc9daad4.png)

This is a repository with some of the projects I developed throughout the Artificial Intelligence course at University of São Paulo. The course was subdivided into various modules, containing some of the following topics:
1. State space search: Breadth-first search, Depth-first search, Uniform cost search, A* search and expectimax search.
2. Probabilistic Reasoning: Hidden-markov chains, Bayesian networks and Value-Iteration (when dealing with reinforcement learning)
3. Machine Learning: Q-Learning and Supervised Learning (kNN, Decision Trees, Perceptron, Neural Networks)


### Project 1: Segmentation of Words using Uniform Cost Search
First part: Given a query, such as 'thisisnotarealword', find the proper places to insert whitespaces using uniform cost search, resulting in the proper readable string 'this is not a real word'. The second part is similar, given a phrase such as 'hll my nm s', return 'hello my name is'. The figure below is an illustration of the search in the state space.

<p align="center">
  <img src="https://user-images.githubusercontent.com/25236592/60368925-7cee1f00-99c8-11e9-9d73-d2995195d35b.png">
</p>

### Project 2: Developing planning agents
The objective is to develop a planning agent to play a game in a grid world, you're playing as a yellow taxi cab against a black taxi cab. Your car has to collect passengers without running out of fuel, some characters gives more points than others. (The characters within the game are the professor and TA's)
<p align="center">
  <img src="https://user-images.githubusercontent.com/25236592/60371198-f25cee00-99ce-11e9-8e74-63b32db3b5f5.gif">
</p>

### Project 3: Generalized blackjack
Modelling a blackjack game, with arbitrary card multiplicity, as a Markov Decision Process. Afterwards, learn how to play a blackjack in an optimal way using reinforcement learning, more specifically, using approximated Q-learning.

Each state can be represented as a tuple (total, index, deck), along with the set of possible actions: 'take', 'peek', 'leave'. Peeking gives you the possibility to look which card comes on top next turn, but taking this action will have a cost depending on the game setup. 

Let's say our deck is composed of three different type of cards, e.g 2,3,4 with multiplicty 2, so our deck is {2,2,3,3,4,4}. An example of state to represent a round for this setup is (3, None, (2,1,2)), where (2,1,2) represents the amount of cards available in the board, each index representing a type of card.
