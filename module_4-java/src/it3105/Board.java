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
        directions.add(Direction.UP);
        directions.add(Direction.DOWN);
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
        //printChildren(children);
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
        int boardScore = 0;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[i][j] == 0) {
                    h++;
                } else {
                    highestValue = (highestValue > grid[j][i]) ? highestValue : grid[j][i];
                    boardScore += grid[j][i];
                }
            }
        }
        //return -1 * (h + highestValue + totalValue);
        int score = (int) (boardScore+Math.log(boardScore) * findEmptyCells() + (16 - calcMergableTiles()));
        return Math.max(score, boardScore);
        //return (h + (highestValue/100) + calcMergableTiles());
        /* why not random?
        int min = 0;
        int max = 100;
        return new Random().nextInt((max - min) + 1) + min;
        */
    }

    private int findEmptyCells() {
        int empty = 0;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (grid[j][i] == 0) empty++;
            }
        }
        return empty;
    }

    private int calcMergableTiles() {
        int mergable = 0;


        for (int i = 0; i < 4; i++) {
            // y axis
            int[] lineY = grid[i];
            lineY = shiftEmptyCells(lineY);
            // x axis
            int[] lineX = new int[4];
            for (int j = 0; j < 4; j++) {
                lineX[j] = grid[j][i];
            }
            lineX = shiftEmptyCells(lineX);
            for (int j = 0; j < 3; j++) {
                if (lineY[j] == lineY[j + 1]) mergable++;
                if (lineX[j] == lineX[j + 1]) mergable++;
            }
        }
        return mergable;
    }

    public int getHeuristicValue() {
        return calculateHeuristicValue();
    }

    private int[][] getNewGridFromDirection(Direction direction) {
        int[][] newGrid = copyGrid(grid);
        switch (direction) {
            case RIGHT:
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
            case LEFT:
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
            case DOWN:
                for (int col = 0; col < 4; col++) {
                    int[] line = grid[col].clone();
                    line = moveLine(reverseLine(line));
                    line = reverseLine(line);
                    newGrid[col] = line;
                }
                break;
            case UP:
                for (int col = 0; col < 4; col++) {
                    int[] line = grid[col].clone();
                    newGrid[col] = moveLine(line);
                }
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
