package it3105;

import game2048.Direction;

import java.util.ArrayList;
import java.util.List;

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
        ///directions.add(Direction.UP);
        //directions.add(Direction.DOWN);
        directions.add(Direction.LEFT);
        directions.add(Direction.RIGHT);
    }

    private List<Board> generateChildren() {
        List<Board> children = new ArrayList<>();

        // generate children of board based
        // on the four legal directions we can move

        for (Direction direction : directions) {
            children.add(
                    new Board(getNewGridFromDirection(direction), direction)
            );
        }
        printChildren(children);
        return children;
    }

    public Direction getMyDirection() {
        return myDirection;
    }

    private void printChildren(List<Board> children) {
        for (Board child : children) {
            System.out.println(child);
        }
    }

    public List<Board> getChildren() {
        return generateChildren();
    }

    public boolean isSolution() {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[i][j] == 2048) return true;
            }
        }
        return false;
    }

    private int calculateHeuristicValue() {
        int h = 0;
        int highestValue = 0;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[i][j] != 0) {
                    h++;
                    highestValue = (highestValue > grid[i][j]) ? highestValue : grid[i][j];
                }
            }
        }
        return -1 * (h + highestValue);
    }

    private int calcMergableTiles() {
        return 0;
    }

    public int getHeuristicValue() {
        return calculateHeuristicValue();
    }

    private int[][] getNewGridFromDirection(Direction direction) {
        int[][] newGrid = copyGrid(grid);
        switch (direction) {
            case UP:
                for (int row = 3; row >= 0; row--) {
                    int[] line = grid[row];
                    newGrid[row] = moveLine(line);
                }
                break;
            case DOWN:
                for (int row = 0; row < 4; row++) {
                    int[] line = grid[row];
                    newGrid[row] = moveLine(line);
                }
                break;
            case LEFT:
                for (int col = 0; col < 4; col++) {
                    int[] line = grid[col];
                    newGrid[col] = moveLine(line);
                }
                break;
            case RIGHT:
                for (int col = 3; col >= 0; col--) {
                    int[] line = grid[col];
                    newGrid[col] = moveLine(line);
                }
        }
        return newGrid;
    }

    // moves elements in line left to right
    private int[] moveLine(int[] line) {
        line = shiftEmptyCells(line);
        for (int i = 0; i < 3; i++) {
            if (line[i] == line[i+1]) {
                line[i+1] = line[i] * 2;
                if (i - 1 >= 0) line[i] = 0;
            }
        }
        line = shiftEmptyCells(line);
        return line;
    }

    // places all empty cells at the start of the line
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
        if (count != 3) {
            for (int i = 4-count; i < 4; i++) {
                tmp[i] = newLine[pos];
                pos++;
            }
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

    @Override
    public String toString() {
        String result = "";
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                result += grid[i][j] + " ";
            }
            result += "\n";
        }
        return result;
    }
}
