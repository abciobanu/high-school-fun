# abc-game-of-life

C++ implementation of Conway's Game of Life, for Linux. The Game of Life, also known simply as Life, is a cellular
automaton devised by the British mathematician John Horton Conway in 1970.

The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further
input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. 

# Rules
The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in
one of two possible states, alive or dead, (or populated and unpopulated, respectively). Every cell interacts with its
eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time,
the following transitions occur:

    1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These rules, which compare the behavior of the automaton to real life, can be condensed into the following:

    1. Any live cell with two or three neighbors survives.
    2. Any dead cell with three live neighbors becomes a live cell.
    3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules
simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this
happens is sometimes called a tick. The rules continue to be applied repeatedly to create further generations. 

# Dependencies
### CMake
* Debian or Debian-based distro (Ubuntu, Linux Mint etc.)

    `sudo apt install cmake`


* Arch or Arch-based distro (Manjaro, Antergos etc.)

    `sudo pacman -S cmake`


* Fedora

    `sudo dnf install cmake`

# Installation
    ./build.sh
    (execute 'chmod +x build.sh' if you cannot run the script)

# Synopsis
    ./abc-game-of-life --size [SIZE] --file [FILE]

    The [SIZE] argument is an integer and represents the size of the game board.
    The [FILE] argument is a string and represents the path to the initial configuration file.
    The initial configuration file is any text file that contains cell coordinates (two integers separated by a
    whitespace (' ') on each line).
