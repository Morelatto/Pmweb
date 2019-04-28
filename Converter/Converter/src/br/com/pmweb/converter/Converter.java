package br.com.pmweb.converter;

import br.com.pmweb.business.BuiltIn;
import br.com.pmweb.business.RPL;
import br.com.pmweb.tools.FileIO;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Lucas Gianfrancesco
 * @author Pedro Morelatto
 */
public class Converter {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("1\tFilename\n2\tConsole\n3\tAllFunctions\n4\tExit\n");
        int opcao = Integer.parseInt(input.next());
        switch (opcao) {
            case 1:
                System.out.println("Filename:");
                String filename = input.next();
                try {
                    FileIO.readFile(filename);
                } catch (Exception e) {
                    e.printStackTrace(System.err);
                }
                break;
            case 2:
                System.out.println("Functions:");
                String function;
                do {
                    function = input.nextLine();
                } while (function.trim().isEmpty());
                String functionRPL = "";
                try {
                    functionRPL = RPL.convertToRPL(BuiltIn.getFunctionFromLine(function.toLowerCase()));
                } catch (Exception ex) {
                    Logger.getLogger(Converter.class.getName()).log(Level.SEVERE, null, ex);
                }
                System.out.println(functionRPL);
                break;
            case 3:
                try {
                    FileIO.readFile("data/allFunctions.txt");
                } catch (Exception e) {
                    e.printStackTrace(System.err);
                }
                break; 
            case 4:
                break;
            default:
                System.out.println("Invalid");
        }

    }

}
