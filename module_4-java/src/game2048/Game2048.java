package game2048;

import it3105.ExpectiMax;
import it3105.HistoryElement;
import it3105.Result;
import javafx.concurrent.Task;
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

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Calendar;
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
    private ExpectiMax expectiMax;
    private int runs = 0;
    private Map<Integer, Integer> score = new HashMap<>();
    private boolean isRunningAI = false;

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
        primaryStage.setTitle("8192FX");
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

    // This method handles hotkeys
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
                isRunningAI = !isRunningAI;
                runAI();
            }
        });
    }

    // This method prints statistics after a run has terminated.
    private void generateStatistics() {
        runs++;
        int highestTile = gameManager.getHighestTile();
        gameManager.resetHighestTile();
        score.put(runs, highestTile);
        int beaten2 = 0;
        int beaten4 = 0;
        int beaten8 = 0;
        int beaten16 = 0;
        int beaten32 = 0;
        int beaten64 = 0;
        int beaten128 = 0;
        int beaten256 = 0;
        int beaten512 = 0;
        int beaten1024 = 0;
        int beaten2048 = 0;
        int beaten4096 = 0;
        int beaten8192 = 0;
        int beaten16384 = 0;
        int beaten32768 = 0;
        System.out.println("#########################");
        for (Integer run : score.keySet()) {
            int value = score.get(run);
            System.out.println("# " + run + ", " + score.get(run));
            if (value >= 2) beaten2++;
            if (value >= 4) beaten4++;
            if (value >= 8) beaten8++;
            if (value >= 16) beaten16++;
            if (value >= 32) beaten32++;
            if (value >= 64) beaten64++;
            if (value >= 128) beaten128++;
            if (value >= 256) beaten256++;
            if (value >= 512) beaten512++;
            if (value >= 1024) beaten1024++;
            if (value >= 2048) beaten2048++;
            if (value >= 4096) beaten4096++;
            if (value >= 8192) beaten8192++;
            if (value >= 16384) beaten16384++;
            if (value >= 32768) beaten32768++;
        }
        System.out.println("Percent above 2: " + 100 * ((float) beaten2 / (float) runs));
        System.out.println("Percent above 4: " + 100 * ((float) beaten4 / (float) runs));
        System.out.println("Percent above 8: " + 100 * ((float) beaten8 / (float) runs));
        System.out.println("Percent above 16: " + 100 * ((float) beaten16 / (float) runs));
        System.out.println("Percent above 32: " + 100 * ((float) beaten32 / (float) runs));
        System.out.println("Percent above 64: " + 100 * ((float) beaten64 / (float) runs));
        System.out.println("Percent above 128: " + 100 * ((float) beaten128 / (float) runs));
        System.out.println("Percent above 256: " + 100 * ((float) beaten256 / (float) runs));
        System.out.println("Percent above 512: " + 100 * ((float) beaten512 / (float) runs));
        System.out.println("Percent above 1024: " + 100 * ((float) beaten1024 / (float) runs));
        System.out.println("Percent above 2048: " + 100 * ((float) beaten2048 / (float) runs));
        System.out.println("Percent above 4096: " + 100 * ((float) beaten4096 / (float) runs));
        System.out.println("Percent above 8192: " + 100 * ((float) beaten8192 / (float) runs));
        System.out.println("Percent above 16384: " + 100 * ((float) beaten16384 / (float) runs));
        System.out.println("Percent above 32768: " + 100 * ((float) beaten32768 / (float) runs));
    }

    private void printHistory() {

        for (String element : expectiMax.getHistory()) {
            System.out.println(element);
        }
    }

    private void writeHistoryToFile(String filename) {
        try {
            Writer writer = new BufferedWriter(new OutputStreamWriter(
                        new FileOutputStream(filename), "utf-8"));

            for (String element : expectiMax.getHistory()) {
                writer.write(element);
            }

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void generateHistory() {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
        writeHistoryToFile("../module_6/training_data/" + timeStamp + "-" + runs + ".dat");
    }

        // This method runs the expectimax algorithm from the expectimax class.
    private void expectiMax() {
        if (gameManager.isGameOver()) {
            generateStatistics();
            //printHistory();
            generateHistory();
            gameManager.tryAgain();
            runAI();
        }
        Direction direction = expectiMax.nextDirection();
        if (direction == null)
            gameManager.move(Direction.values()[new Random().nextInt(Direction.values().length - 1)]);
        else gameManager.move(direction);
    }

    // This method begins the expectimax loop.
    // It will keep running after termination to allow serial testing.
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
            //generateHistory();
            runAI();
        });
        if (!gameManager.isGameOver() && isRunningAI) new Thread(task).start();
    }

}
