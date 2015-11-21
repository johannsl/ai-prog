package it3105;

import game2048.Direction;

/**
 * Created by iver on 18/11/15.
 */
public class HistoryElement {
    private int[][] board;
    private Direction direction;

    public HistoryElement(int[][] board, Direction direction) {
        this.board = board;
        this.direction = direction;
    }

    public int[][] getBoard() {
        return board;
    }

    public Direction getDirection() {
        return direction;
    }

    public String getBoardAsString() {
        String result = "";
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                result += this.board[i][j];
                if (j != 3) result += " ";
            }
            result += "\n";
        }
        return result;
    }

    public String getDirectionAsString() {
        if (this.direction == null) return "NONE";
        switch (this.direction) {
            case LEFT:
                return "0\n";
            case UP:
                return "1\n";
            case RIGHT:
                return "2\n";
            case DOWN:
                return "3\n";
            default:
                return "0\n";

        }
    }
}
