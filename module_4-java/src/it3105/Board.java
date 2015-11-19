package it3105;

import game2048.Direction;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Created by iver on 20/10/15.
 */
public class Board {

    private int[][] grid;
    private List<Direction> directions;
    private Direction myDirection;

    public Board(int[][] grid, Direction direction) {
        this.grid = grid;
        this.myDirection = direction;
        directions = new ArrayList<>();
        for (Direction dir : Direction.values()) {
            directions.add(dir);
        }
    }

    // Board generating
    private List<Board> generateChildren(boolean max) {
        List<Board> children = new ArrayList<>();

        if (max) {
            // generate children of board based
            // on the four legal directions we can move
            // (skip boards that are equal to our state)

            for (Direction direction : directions) {
                Board child = new Board(getNewGridFromDirection(direction), direction);
                if (!this.equals(child)) children.add(child);
            }
            return children;
        }
        else {
            for (int tile=0; tile<getEmptyTiles(); tile++) {
                Board child = new Board(getNewExpectGrid(tile), null);
                children.add(child);
            }
            return children;
        }
    }

    // Breaks the grid into lines that should be read left to right
    private int[][] getNewGridFromDirection(Direction direction) {
        int[][] newGrid = copyGrid(grid);
        switch (direction) {
            case DOWN:
                int[][] rightGrid = copyGrid(grid);
                for (int i = 0; i < 4; i++) {
                    int[] line = new int[4];
                    for (int j = 0; j < 4; j++) {
                        line[j] = rightGrid[j][i];
                    }
                    line = moveLine(line);
                    for (int j = 0; j < 4; j++) {
                        newGrid[j][i] = line[j];
                    }
                }
                break;
            case UP:
                int[][] leftGrid = copyGrid(grid);
                for (int i = 0; i < 4; i++) {
                    int[] line = new int[4];
                    for (int j = 0; j < 4; j++) {
                        line[j] = leftGrid[j][i];
                    }
                    line = reverseLine(line);
                    line = moveLine(line);
                    line = reverseLine(line);
                    for (int j = 0; j < 4; j++) {
                        newGrid[j][i] = line[j];
                    }
                }
                break;
            case LEFT:
                for (int row = 0; row < 4; row++) {
                    int[] line = grid[row].clone();
                    line = moveLine(reverseLine(line));
                    line = reverseLine(line);
                    newGrid[row] = line;
                }
                break;
            case RIGHT:
                for (int row = 0; row < 4; row++) {
                    int[] line = grid[row].clone();
                    newGrid[row] = moveLine(line);
                }
                break;
        }
        return newGrid;
    }

    private int[] reverseLine(int[] line) {
        for(int i = 0; i < line.length / 2; i++)
        {
            int temp = line[i];
            line[i] = line[line.length - i - 1];
            line[line.length - i - 1] = temp;
        }
        return line;
    }

    // Moves elements in line left to right
    private int[] moveLine(int[] line) {
        line = shiftEmptyCells(line);
        int changedPos = -1;
        for (int i = 3; i > 0; i--) {
            if (line[i] == line[i-1] && i+1 != changedPos) {
                changedPos = i;
                line[i-1] *= 2;
                line[i] = 0;
            }
        }
        line = shiftEmptyCells(line);
        return line;
    }

    // Places all empty cells at the start of the line
    private int[] shiftEmptyCells(int[] line) {
        int[] newLine = new int[4];
        int count = 0;
        for (int i = 0; i < 4; i++) {
            if (line[i] != 0) {
                newLine[count] = line[i];
                count++;
            }
        }
        int[] tmp = new int[4];
        int pos = 0;
        for (int i = 4-count; i < 4; i++) {
            tmp[i] = newLine[pos];
            pos++;
        }
        return tmp;
    }

    private int[][] copyGrid(int[][] grid) {
        int[][] copy = new int[4][4];
        for (int i = 0; i < 4; i++) {
            copy[i] = grid[i].clone();
        }
        return copy;
    }

    // Creates and returns one possible chance grid
    private int[][] getNewExpectGrid(int fillTile) {
        int tileCount = 0;
        int[][] expectGrid = copyGrid(grid);
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[i][j] == 0) {
                    if (tileCount == fillTile) {
                        expectGrid[i][j] = 2;
                        return expectGrid;
                    }
                    tileCount++;
                }
            }
        }
        System.out.println("ERROR!");
        return null;
    }

    @Override
    public String toString() {
        String result = "\n";
        result += this.getMyDirection() + "\n";
        result += "Mergable tiles: " + this.getMergableTiles() + "\n";
        result += "Empty tiles: " + this.getEmptyTiles() + "\n";
        result += "Heuristic: " + this.getHeuristicValue() + "\n";
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                result += grid[i][j] + " ";
            }
            result += "\n";
        }
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == null) return false;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (this.grid[i][j] != ((Board) other).getGrid()[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

    private void printChildren(List<Board> children) {
        for (Board child : children) {
            System.out.println(child);
        }
    }

    public Direction getMyDirection() {
        return myDirection;
    }

    public int[][] getGrid() {
        return grid;
    }
    public List<Board> getChildren(boolean max) {
        return generateChildren(max);
    }

    // board is a solution if it contains a 2048 tile
    public boolean isSolution() {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[i][j] == 2048) return true;
            }
        }
        return false;
    }

    // This is our heuristics method, it calculates how good a grid is.
    private int calculateHeuristicValue() {
        int snakeScore = 0;
        int[][] weights = {{65563, 32768, 16384, 8192},
                {256, 512, 2048, 2048},
                {128, 64, 32, 16},
                {1, 2, 4, 8}};

        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                snakeScore += grid[j][i] * weights[j][i];
            }
        }

        /*
        // why not random? http://pastebin.com/NdNARNxY
        int min = 0;
        int max = 100;
        return new Random().nextInt((max - min) + 1) + min;
        */
        return snakeScore;
    }

    // Counts empty tiles
    private int findEmptyTiles() {
        int empty = 0;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[i][j] == 0) empty++;
            }
        }
        return empty;
    }

    private int calcMergableTiles() {
        int mergable = 0;
        int[][] copy = copyGrid(grid);

        for (int i = 0; i < 4; i++) {
            // y axis
            int[] lineY = copy[i];
            lineY = shiftEmptyCells(lineY);
            // x axis
            int[] lineX = new int[4];
            for (int j = 0; j < 4; j++) {
                lineX[j] = copy[j][i];
            }
            lineX = shiftEmptyCells(lineX);
            for (int j = 0; j < 3; j++) {
                if (lineY[j] != 0 && lineY[j] == lineY[j + 1]) mergable++;
                if (lineX[j] != 0 && lineX[j] == lineX[j + 1]) mergable++;
            }
        }
        return mergable;
    }

    public int getEmptyTiles() {
        return findEmptyTiles();
    }

    public int getMergableTiles() {
        return calcMergableTiles();
    }

    public int getHeuristicValue() {
        return calculateHeuristicValue();
    }

}
