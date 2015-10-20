package it3105;

import game2048.Direction;
import game2048.GameManager;
import game2048.Location;
import game2048.Tile;

import java.util.Map;

/**
 * Created by iver on 14/10/15.
 */
public class Ivermax {

    private GameManager gameManager;
    boolean down = true;
    private int[][] grid;
    private int[][] oldGrid;

    public Ivermax(GameManager gameManager) {
        this.gameManager = gameManager;
        // TODO: set grid size dynamically
        this.grid = new int[4][4];
        this.oldGrid = gameGridToArray();
    }

    public Direction nextDirection() {
        int[][] grid = gameGridToArray();
        if (hDown(grid) > hRight(grid)) return Direction.DOWN;
        return Direction.RIGHT;
        /*
        if (down) {
            down = false;
            return  Direction.RIGHT;
        }
        down = true;
        return Direction.DOWN;
        */
    }

    public int heuristic(int[][] grid) {
        int h = 0;
        h = mergableMoves(grid);
        System.out.println("Heuristic: " + h);
        System.out.println(gameManager.mergesAvailable());
        return h;
    }

    public int mergableMoves(int[][] grid) {
        int result = 0;
        for (int y = 0; y < grid.length; y++) {
            for (int x = 0; x < grid.length - 1; x++) {
                if (grid[x][y] == 0) continue;
                if (grid[x][y] == grid[x + 1][y]) result++;
            }
        }

        for (int x = 0; x < grid.length; x++) {
            for (int y = 0; y < grid.length - 1; y++) {
                if (grid[x][y] == 0) continue;
                if (grid[x][y] == grid[x][y + 1]) result++;
            }
        }

        return result;
    }

    private int hDown(int[][] grid) {
        int result = 0;
        for (int x = 0; x < grid.length; x++) {
            for (int y = 0; y < grid.length - 1; y++) {
                if (grid[x][y] == 0) continue;
                if (grid[x][y] == grid[x][y + 1]) result += grid[x][y] * 2;
            }
        }
        return result;
    }

    private int hRight(int[][] grid) {
        int result = 0;
        for (int y = 0; y < grid.length; y++) {
            for (int x = 0; x < grid.length - 1; x++) {
                if (grid[x][y] == 0) continue;
                if (grid[x][y] == grid[x + 1][y]) result += grid[x][y] * 2;
            }
        }
        return result;
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
        /*
        for (int i = 0; i < myGrid.length; i++) {
            for (int j = 0; j < myGrid.length; j++) {
                System.out.print(myGrid[j][i]);
            }
            System.out.println();
        }
        System.out.println("--------");
        */
        return myGrid;
    }

    public boolean canMoveDown(int[][] grid) {
        for (int x = 0; x < grid.length; x++) {
            for (int y = 0; y < grid.length - 1; y++) {
                int i = grid[x][y];
                if (i == 0) continue;
                for (int j = y; j < 4; j++) {
                    if (grid[x][j] == 0) return true;
                }
            }
        }
        return false;
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
