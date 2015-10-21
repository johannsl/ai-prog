package it3105;

/**
 * Created by iver on 21/10/15.
 */
public class BoardMain {

    public static void main(String[] args) {

        /* old structure (tilted grid)
        int[][] grid = new int[][]{
                {2, 0, 0, 0},
                {0, 0, 4, 4},
                {0, 4, 0, 2},
                {2, 0, 2, 2}
        };
        */
        int[][] grid = new int[][]{
                {2, 0, 0, 2},
                {0, 0, 0, 0},
                {0, 4, 0, 2},
                {0, 4, 2, 2}
        };

        Board board = new Board(grid, null);

        System.out.println(board.getChildren());
    }
}
