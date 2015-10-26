package it3105;

import game2048.Direction;

/**
 * Created by iver on 21/10/15.
 */

// This class holds result values
public class  Result {
    private int result;
    private Direction direction;

    public Result(int result, Direction direction) {
        this.result = result;
        this.direction = direction;
    }

    public int getResult() {
        return result;
    }

    public Direction getDirection() {
        return direction;
    }
}
