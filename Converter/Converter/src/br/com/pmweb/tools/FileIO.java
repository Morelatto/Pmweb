package br.com.pmweb.tools;

import br.com.pmweb.business.BuiltIn;
import br.com.pmweb.business.RPL;
import br.com.pmweb.classes.Function;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 *
 * @author Lucas Gianfrancesco
 * @author Pedro Morelatto
 */
public class FileIO {

    public static void readFile(String fileName) throws Exception {
        BufferedReader br = null;
        try {
            String sCurrentLine;
            br = new BufferedReader(new FileReader(fileName));
            while ((sCurrentLine = br.readLine()) != null) {
                if (sCurrentLine.length() > 0) {
                    while (sCurrentLine.contains("  ")) {
                        sCurrentLine = sCurrentLine.replace("  ", " ");
                    }
                    Function function = BuiltIn.getFunctionFromLine(sCurrentLine.toLowerCase());
                    if ("null".equals(function.getName())) {
                        writeFile(fileName, sCurrentLine);
                    } else {
                        String functionRPL = RPL.convertToRPL(function);
                        writeFile(fileName, functionRPL);
                    }
                } else {
                    writeFile(fileName, sCurrentLine);
                }
            }
        } catch (IOException e) {
            e.printStackTrace(System.err);
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace(System.err);
            }
        }
    }

    //fileName.substring(0, fileName.indexOf('.')) 
    //+ "_RPL_" 
    //+ new SimpleDateFormat("dd-MM-yyyy_HH-mm").format(new Date()) 
    //+ fileName.substring(fileName.indexOf('.'))
    public static void writeFile(String fileName, String data) {
        Writer writer = null;
        try {
            writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileName.substring(0, fileName.indexOf('.')) + "_RPL_" + new SimpleDateFormat("dd-MM-yyyy_HH-mm").format(new Date()) + fileName.substring(fileName.indexOf('.')), true), "UTF-8"));
            writer.write(data + "\n");
        } catch (IOException e) {
            e.printStackTrace(System.err);
        } finally {
            try {
                if (writer != null) {
                    writer.close();
                }
            } catch (Exception e) {
                e.printStackTrace(System.err);
            }
        }
    }
}
