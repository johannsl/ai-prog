package it3105;

/**
 * Created by iver on 21/10/15.
 */
public class BoardTest {

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

        int[][] equalGrid = new int[][]{
                {2, 0, 0, 2},
                {0, 0, 0, 0},
                {0, 4, 0, 2},
                {0, 4, 2, 2}
        };

        Board board = new Board(grid, null);
        Board equalBoard = new Board(equalGrid, null);
        System.out.println("Equals? " + board.equals(equalBoard));

        System.out.println(board.getChildren());
    }
}
