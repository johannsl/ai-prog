package it3105;

import game2048.Direction;
import game2048.GameManager;
import game2048.Location;
import game2048.Tile;

import java.util.Map;

/**
 * Created by iver on 15/10/15.
 */
public class Expectimax {

    private GameManager gameManager;
    private int[][] grid;
    private Direction nextDirection;
    private Board nextBoard;

    public Expectimax(GameManager gameManager) {
        this.gameManager = gameManager;
        // TODO: set grid size dynamically
        this.grid = new int[4][4];
    }

    public Direction nextDirection() {
        System.out.println(miniMax(
                new Board(gameGridToArray(), null),
                1,
                true
        ));
        System.out.println(nextDirection);
        return nextDirection;
    }

    private int miniMax(Board node, int depth, boolean isMaximizingPlayer) {
        if (depth == 0 || node.isSolution()) return node.getHeuristicValue();
        if (isMaximizingPlayer) {
            int bestValue = Integer.MIN_VALUE;
            for (Board child : node.getChildren()) {
                int value = miniMax(child, depth - 1, false);
                if (bestValue < value) {
                    bestValue = value;
                    nextDirection = child.getMyDirection();
                    nextBoard = child;
                }
            }

            return bestValue;
        } else {
            int bestValue = Integer.MAX_VALUE;
            for (Board child : node.getChildren()) {
                int value = miniMax(child, depth - 1, true);
                if (bestValue > value) {
                    bestValue = value;
                }
            }
            return bestValue;
        }
    }

    public int[][] gameGridToArray() {
        int[][] myGrid = new int[4][4];
        Map<Location, Tile> gameGrid = gameManager.getGameGrid();
        if (gameGrid == null) System.out.println("grid is null");
        for (Map.Entry<Location, Tile> entry : gameGrid.entrySet()) {
            if (entry.getValue() != null) {
                myGrid[entry.getValue().getLocation().getX()][entry.getValue().getLocation().getY()] = entry.getValue().getValue();
            }
        }
        return myGrid;
    }

}
