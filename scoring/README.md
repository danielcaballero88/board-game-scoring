# Scoring App

## Models

### Games

Here games are "game classes". For instance the game "Agricola" is the game itself, not a particular instance or match being played or having been played.

Relatioinships:
- The main model is, of course, `Game`.
- A many to many relationship exists with the model `Genre`
- A one to many relationship exists with the model `ScoringCategory`
  - Each game has a number of scoring categories that belong to that game only and that are used to score at the end of the game.

### Players

The `Player` model represents a `User`. The difference is that `User` is the authentication model provided by the `accounts` app but the `Player` model holds
the data necessary for the `scoring` app to function properly.

### Table

This is an instance of a game being played or having been played.

- It has an `owner` which is a `Player`.
- It has a `winner` which is a `Player`.
- It has a `player_set` which is a set of `Player` at the table, besides the `owner`.
- It has a `score_set` which is a list of scores.
  - The score model is `Score` which represents a score for a single player, at a single table, for a single scoring category. Besides these relationships it has a single integer field: `value`.

TBD:
- Allow non-registered players so a user can create a table and send a link to friends and they can input their scores without the need to create an account.
  - A new model `OneTimePlayer` could be created, with a nickname alone would be enough.
  - A one to many relationship is needed only (one `Table` many `OneTimePlayer`) because these one time players would be only players for one specific table.
- Allow more than one winner for games that end in ties.
