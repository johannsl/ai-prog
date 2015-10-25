package it3105;

import game2048.Direction;
import game2048.GameManager;
import game2048.Location;
import game2048.Tile;

import java.util.Map;

/**
 * Created by iver on 15/10/15.
 */
public class ExpectiMax {

    private GameManager gameManager;
    private Direction nextDirection;
    private Board nextBoard;

    public ExpectiMax(GameManager gameManager) {
        this.gameManager = gameManager;
        // TODO: set grid size dynamically
    }

    public Direction nextDirection() {
        Result result = runExpectiMax(
                new Board(gameGridToArray(), null),
                3,
                true
        );
        System.out.println(result.getDirection());
        return result.getDirection();
    }

    private Result runExpectiMax(Board node, int depth, boolean isMaximizingPlayer) {
        if (depth == 0 || node.isSolution())
            return new Result(node.getHeuristicValue(), node.getMyDirection());

        if (isMaximizingPlayer) {
            int bestValue = 0;
            Direction direction = null;
            for (Board child : node.getChildren(isMaximizingPlayer)) {
                int value = runExpectiMax(child, depth - 1, false).getResult();

                System.out.println(value);
                if (bestValue < value) {
                    bestValue = value;
                    direction = child.getMyDirection();
                    nextBoard = child;
                }
            }
            System.out.println("MAX BESTVALUE: " + bestValue);
            System.out.println("MAX DIRECTION: " +direction);
            return new Result(bestValue, direction);

        } else {
            int bestValue = 0;
            for (Board child : node.getChildren(isMaximizingPlayer)) {
                int value = runExpectiMax(child, depth - 1, true).getResult();
                if (bestValue < value) {
                    bestValue = value;
                }
            }
            System.out.println("CHANCE BESTVALUE: " + bestValue);
            System.out.println("CHANCE DIRECTION: " + node.getMyDirection());
            return new Result(bestValue, node.getMyDirection());
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
