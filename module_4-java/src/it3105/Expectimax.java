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
    private Direction nextDirection;
    private Board nextBoard;

    public Expectimax(GameManager gameManager) {
        this.gameManager = gameManager;
        // TODO: set grid size dynamically
    }

    public Direction nextDirection() {
        Result result = miniMax(
                new Board(gameGridToArray(), null),
                1,
                true
        );
        System.out.println(nextBoard);
        return result.getDirection();
    }

    private Result miniMax(Board node, int depth, boolean isMaximizingPlayer) {
        if (depth == 0 || node.isSolution())
            return new Result(node.getHeuristicValue(), node.getMyDirection());

        if (isMaximizingPlayer) {
            int bestValue = Integer.MIN_VALUE;
            Direction direction = null;
            for (Board child : node.getChildren()) {
                int value = miniMax(child, depth - 1, false).getResult();
                if (bestValue < value) {
                    bestValue = value;
                    direction = child.getMyDirection();
                    nextBoard = child;
                }
            }

            return new Result(bestValue, direction);
        } else {
            int bestValue = Integer.MAX_VALUE;
            for (Board child : node.getChildren()) {
                int value = miniMax(child, depth - 1, true).getResult();
                if (bestValue > value) {
                    bestValue = value;
                }
            }
            return new Result(bestValue, null);
        }
    }

    public int[][] gameGridToArray() {
        int[][] myGrid = new int[4][4];
        Map<Location, Tile> gameGrid = gameManager.getGameGrid();
        for (Map.Entry<Location, Tile> entry : gameGrid.entrySet()) {
            if (entry.getValue() != null) {
                myGrid[entry.getValue().getLocation().getY()][entry.getValue().getLocation().getX()] = entry.getValue().getValue();
            }
        }
        return myGrid;
    }

}
