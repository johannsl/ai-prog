package it3105;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by iver on 18/11/15.
 */
public class History {

    private List<HistoryElement> history;

    public History() {
        this.history = new ArrayList<>();
    }

    public void add(HistoryElement element) {
        history.add(element);
    }

    public List<HistoryElement> getHistory() {
        return this.history;
    }

    public List<String> getHistoryAsString() {
        List<String> result = new ArrayList<>();
        for (HistoryElement element : this.history) {
            result.add(
                    element.getBoardAsString() + element.getDirectionAsString()
            );
        }
        return result;
    }
}
