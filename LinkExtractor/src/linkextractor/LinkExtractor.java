package linkextractor;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author Pedro Morelatto
 */
public class LinkExtractor {

    static String fileToString(String fileName) {
        StringBuilder contentBuilder = new StringBuilder();
        try {
            try (BufferedReader in = new BufferedReader(new FileReader(fileName))) {
                String str;
                while ((str = in.readLine()) != null) {
                    contentBuilder.append(str);
                }
            }
        } catch (IOException e) {
        }
        return contentBuilder.toString();
    }
    
    static ArrayList<String> getLinks(String html) {
        ArrayList<String> links = new ArrayList<>();
        String regex = "href=\"([^\"]*)\"";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(html);
        int index = 0;
        while (matcher.find(index)) {
            String url = matcher.group(1);
            links.add(url);
            index = matcher.end();
        }
        return links;
    }
}