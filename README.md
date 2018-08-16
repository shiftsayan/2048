# Python 2048

This is [2048](https://github.com/gabrielecirulli/2048) clone built in Python using `tkinter` for the GUI. The game has a single-player *play* mode and zero-player *simulate* mode, which you can choose between when you run the app.

### Dependencies

You will need the following packages installed for Python 2.7:

* `tkinter`
* `random`
* `anytree`

### Use

You can play the game by running `python play.py` and then choose between [P]lay or [S]imulate.

### AI

The game's AI was largely inspired from [this](https://stackoverflow.com/a/23853848/4982987) phenomenal StackOverflow answer. It tries to optimize for:
1. Largest Tile on the Board
2. Smoothness of the Board (i.e. tiles of the same order should be closer together on the board)
3. Monotonicity of the Board (i.e. tiles in a row or a column should be increasing or decreasing)
4. Number of Empty Tiles on the Board

It isn't perfect, but it usually gets to a high 1024 tile or wins with `DEPTH = 5`, in my limited testing. You can fork this repository and try tuning the calculation metrics and weights to optimize the evaluation function.
