package game2048;

import it3105.ExpectiMax;
import it3105.Result;
import javafx.concurrent.Task;
import it3105.Ivermax;
import javafx.application.Application;
import javafx.application.ConditionalFeature;
import javafx.application.Platform;
import javafx.geometry.Bounds;
import javafx.geometry.Rectangle2D;
import javafx.scene.Cursor;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.stage.Screen;
import javafx.stage.Stage;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * @author bruno.borges@oracle.com
 */
public class Game2048 extends Application {

    public static final String VERSION = "1.0.4";
    
    private GamePane root;
    private GameManager gameManager;
    private Ivermax ivermax;
    private ExpectiMax expectiMax;
    private int runs = 0;
    private Map<Integer, Integer> score = new HashMap<>();

    @Override
    public void start(Stage primaryStage) {
        root = new GamePane();
        gameManager = root.getGameManager();

        Scene scene = new Scene(root);
        scene.getStylesheets().add("game2048/game.css");

        if (isARMDevice()) {
            primaryStage.setFullScreen(true);
            primaryStage.setFullScreenExitHint("");
        }

        if (Platform.isSupported(ConditionalFeature.INPUT_TOUCH)) {
            scene.setCursor(Cursor.NONE);
        }

        Bounds gameBounds = root.getGameManager().getLayoutBounds();
        int MARGIN = GamePane.getMargin();
        Rectangle2D visualBounds = Screen.getPrimary().getVisualBounds();
        double factor = Math.min(visualBounds.getWidth() / (gameBounds.getWidth() + MARGIN),
                visualBounds.getHeight() / (gameBounds.getHeight() + MARGIN));
        primaryStage.setTitle("2048FX");
        primaryStage.setScene(scene);
        primaryStage.setMinWidth(gameBounds.getWidth() / 2d);
        primaryStage.setMinHeight(gameBounds.getHeight() / 2d);
        primaryStage.setWidth((gameBounds.getWidth() + MARGIN) * factor);
        primaryStage.setHeight((gameBounds.getHeight() + MARGIN) * factor);
        
        primaryStage.setOnCloseRequest(t->{
            t.consume();
            root.getGameManager().quitGame();
        });
        primaryStage.show();
        addKeyHandler(scene);
        ivermax = new Ivermax(gameManager);
        expectiMax = new ExpectiMax(gameManager);
    }

    private boolean isARMDevice() {
        return System.getProperty("os.arch").toUpperCase().contains("ARM");
    }

    public GamePane getGamePane() {
        return root;
    }

    @Override
    public void stop() {
        root.getGameManager().saveRecord();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        launch(args);
    }

    private void addKeyHandler(Scene scene) {
        scene.setOnKeyPressed(key -> {
            KeyCode keyCode = key.getCode();

            if (keyCode.equals(KeyCode.P)) {
                gameManager.pauseGame();
                return;
            }
            if (keyCode.equals(KeyCode.Q) || keyCode.equals(KeyCode.ESCAPE)) {
                gameManager.quitGame();
                return;
            }
            if (keyCode.isArrowKey()) {
                Direction direction = Direction.valueFor(keyCode);
                gameManager.move(direction);
            }
            if(keyCode.equals(KeyCode.I)){
                expectiMax();
            }
            if(keyCode.equals(KeyCode.M)){
                runAI();
            }
        });
    }

    private void generateStatistics() {
        runs++;
        int highestTile = gameManager.getHighestTile();
        gameManager.resetHighestTile();
        score.put(runs, highestTile);
        int beaten2048 = 0;
        int beaten4096 = 0;
        int beaten8192 = 0;
        System.out.println("#########################");
        for (Integer run : score.keySet()) {
            int value = score.get(run);
            System.out.println("# " + run + ", " + score.get(run));
            if (value > 2048) beaten2048++;
            if (value > 4096) beaten4096++;
            if (value > 8192) beaten8192++;
        }
        System.out.println("Percent above 2048: " + (float) beaten2048 / runs);
        System.out.println("Percent above 4096: " + (float) beaten4096 / runs);
        System.out.println("Percent above 8192: " + (float) beaten8192 / runs);

    }

    private void expectiMax() {
        if (gameManager.isGameOver()) {
            generateStatistics();
            gameManager.tryAgain();
        }
        Direction direction = expectiMax.nextDirection();
        if (direction == null)
            gameManager.move(Direction.values()[new Random().nextInt(Direction.values().length - 1)]);
        else gameManager.move(direction);
    }

    private void iverMax() {
        int[][] oldGrid = ivermax.gameGridToArray().clone();
        gameManager.move(ivermax.nextDirection());
        if (ivermax.compareGridArrays(ivermax.gameGridToArray(), oldGrid) && !ivermax.canMoveDown(ivermax.gameGridToArray()))
            gameManager.move(Direction.LEFT);
        else
            gameManager.move(Direction.DOWN);
    }

    private void runAI() {

        Task task = new Task<Void>() {

            @Override
            protected Void call() throws Exception {
                while(gameManager.isMovingTiles());
                return null;
            }
        };
        task.setOnSucceeded(event -> {
            expectiMax();
            runAI();
        });
        new Thread(task).start();
    }

}
