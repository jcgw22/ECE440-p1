# ECE440-p1

## INTRODUCTION
Games of strategy in which two players alternate moves constitute an important area of Artificial Intelligence. Such games enlist a range of cognitive abilities, are well-defined and so amenable to computation, and yet are complicated enough to be challenging. Because games are competitive, game-playing programs allow direct comparisons of human and machine abilities.

## DESCRIPTION
Write a program that plays the game Othello (also called Reversi) against a human opponent and document the program in a paper (described below). All the programs will compete in a tournament to be held shortly after the due date.

Your program will play Othello interactively against a human opponent, with either the program or the opponent playing first. It will, after each move, display the current state of the game board, and it will employ a static evaluation function (SEF) to evaluate board configurations.

You may write the program in any programming language you choose. Your program may employ any of the algorithms for move selection --- minimax, alpha-beta pruning, forward pruning, etc. --- that we've described, and any modifications that you think are appropriate. Note that the major operations of the program --- and the major challenges --- are these:

Representing the game board and implementing moves on it;
Displaying the game board and interacting with the opponent;
Evaluating board configurations: the static evaluation function; and
Organizing the search of the game tree on which move selection is based.

## WHAT TO HAND IN
A progress report will describe the state of your program at the time the report is due. In particular, you should be able to report the language in which the program will be written and the program's major design features and overall structure. This report should be word-processed and no more than one page long.

`Due on October 12 is a paper that describes the motivation, design, and performance of the program. Do not hand in code.`

The paper should be written in the style of a conference paper. Use 10-point type in a two-column format with margins of one inch on all four sides. The ACM conference format, available here, is a good choice.

The paper must begin with a brief abstract that summarizes the paper, and must conclude with a list of the references mentioned in its text. It may be no longer than five pages, including the title, abstract, figures, and references.

Assume that the readers of your paper know in general as much as you do, but they don't know anything about this project. In particular, they have not read this page and they don't know about this project. Your paper must tell them what you did in the project, and why, and how.

Consider an organization like this for the paper:

* Abstract
* Introduction
* The game
* Design choices and features of the program
* Static evaluation function and game-tree search
* Using the program
* The program's performance
* Conclusion
* References

The abstract and the paper itself should be independent; neither can depend on material introduced in the other. (HINT: Write the abstract last.)

Be careful not to use any of the language in this posting or in any of your references, and to list all your references, including those found on the web. Print sources are in general more credible than material found on the web. If a paper is available both in print and on line, list its print reference, unless the on-line version is presented as definitive (Some journals do this).
