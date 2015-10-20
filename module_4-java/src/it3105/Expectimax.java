package it3105;

import game2048.Direction;
import game2048.GameManager;

/**
 * Created by iver on 15/10/15.
 */
public class Expectimax {

    private GameManager gameManager;
    private int[][] grid;

    public Expectimax(GameManager gameManager) {
        this.gameManager = gameManager;
        // TODO: set grid size dynamically
        this.grid = new int[4][4];
    }

    public Direction nextDirection() {
        return null;
    }

}
