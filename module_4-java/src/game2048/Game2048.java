package game2048;

import it3105.Expectimax;
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

/**
 * @author bruno.borges@oracle.com
 */
public class Game2048 extends Application {

    public static final String VERSION = "1.0.4";
    
    private GamePane root;
    private GameManager gameManager;
    private Ivermax ivermax;
    private Expectimax expectimax;

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
        expectimax = new Expectimax(gameManager);
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

    private void expectiMax() {
        gameManager.move(expectimax.nextDirection());
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