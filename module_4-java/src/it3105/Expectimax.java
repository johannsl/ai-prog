package it3105;

import game2048.Direction;
import game2048.GameManager;
import game2048.Location;
import game2048.Tile;

import java.util.Map;

/**
 * Created by iver on 14/10/15.
 */
public class Expectimax {

    private GameManager gameManager;
    boolean down = true;
    private int[][] grid;
    private int[][] oldGrid;

    public Expectimax(GameManager gameManager) {
        this.gameManager = gameManager;
        // TODO: set grid size dynamically
        this.grid = new int[4][4];
        this.oldGrid = gameGridToArray();
    }

    public Direction nextDirection() {
        if (down) {
            down = false;
            return  Direction.RIGHT;
        }
        down = true;
        return Direction.DOWN;
    }

    public int[][] gameGridToArray() {
        int[][] myGrid = new int[4][4];
        Map<Location, Tile> gameGrid = gameManager.getGameGrid();
        if (gameGrid == null) System.out.println("grid is null");
        for (Map.Entry<Location, Tile> entry : gameGrid.entrySet()) {
            if (entry.getValue() != null) {
                System.out.println(entry.getValue());
                myGrid[entry.getValue().getLocation().getX()][entry.getValue().getLocation().getY()] = entry.getValue().getValue();
            }
        }
        for (int i = 0; i < myGrid.length; i++) {
            for (int j = 0; j < myGrid.length; j++) {
                System.out.print(myGrid[i][j]);
            }
            System.out.println();
        }
        System.out.println("--------");
        return myGrid;
    }

    public boolean compareGridArrays(int[][] grid1, int[][] grid2) {
        for (int i = 0; i < grid1.length; i++) {
            for (int j = 0; j < grid1.length; j++) {
                if (grid1[i][j] != grid2[i][j]) return false;
            }
        }
        return true;
    }
}
