package it3105;

import game2048.GameManager;
import game2048.Location;
import game2048.Tile;

import java.util.Map;

/**
 * Created by iver on 15/10/15.
 */
public class Board {

    public static void printBoard(long board) {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                long powerVal = board & 0xf;
                System.out.print(((powerVal == 0) ? 0 : 1 << powerVal) + " ");
                board >>= 4;
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        printBoard((long)Math.pow(2, 3) + (long)Math.pow(2,3));
    }

    public void boardToLong(GameManager gameManager) {
        Map<Location, Tile> gameGrid = gameManager.getGameGrid();
        if (gameGrid == null)
            System.out.println("grid is null");
        for (Map.Entry<Location, Tile> entry : gameGrid.entrySet()) {
            if (entry.getValue() != null) {
            }
        }
    }

}
