package br.com.pmweb.business;

import br.com.pmweb.classes.Function;
import br.com.pmweb.classes.Parameter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author Lucas Gianfrancesco
 * @author Pedro Morelatto
 */
public class BuiltIn {

    private static final char L_PAREN = '(';
    private static final char R_PAREN = ')';
    private static final char COMMA = ',';

    public static Function getFunctionFromLine(String line) {
        String functionAux;
        final Pattern pattern = Pattern.compile("\\$(.+?)\\$");
        final Matcher matcher = pattern.matcher(line);
        Function function = new Function("null");

        if (matcher.find()) {
            functionAux = matcher.group(1);
            function = convertToObject(functionAux);
        }
        return function;
    }

    private static Function convertToObject(String line) {
        Function function = new Function();
        int lParen = line.indexOf(L_PAREN);
        int rParen = line.lastIndexOf(R_PAREN);
        if (lParen != -1) {
            String functionAux = line.substring(0, lParen);//Nome da Funcao
            function.setName(functionAux);
            //Parametros
            String parameters = line.substring(lParen + 1, rParen);
            String parameterAux;
            int parameterEnd;
            do {
                parameterEnd = parameters.indexOf(COMMA);//Acha fim do parametro
                if (parameterEnd == 0) {//se tiver virgula no comeco
                    parameters = parameters.substring(1);
                    parameterEnd = parameters.indexOf(COMMA);//Acha fim do parametro
                } else {
                }
                if (parameterEnd != -1) {//Se nao achar fim do parametro
                    parameterAux = parameters.substring(0, parameterEnd);//pega parametro
                } else {
                    parameterAux = parameters;
                }
                if (parameterAux.contains(L_PAREN + "")) {//verifica se o parametro é uma funcao
                    parameterEnd = getLastParenthesis(parameters);
                    parameterAux = parameters.substring(0, parameterEnd + 1);
                    function.addParameter(convertToObject(parameterAux));
                    parameterAux = null;
                }
                parameters = parameters.substring(parameterEnd + 1);
                if (parameterAux != null) {
                    Parameter parameter = new Parameter(parameterAux);
                    function.addParameter(parameter);
                }
            } while (parameterEnd != -1 && parameters.length() > 0);
        }
        return function;
    }

    //Acha o parentese que fecha a funcao
    private static int getLastParenthesis(String line) {
        int lParen = line.indexOf(L_PAREN), rParen = line.indexOf(R_PAREN);
        String lineAux = line.substring(lParen + 1, rParen);
        while (lineAux.contains(L_PAREN + "")) {
            rParen = line.indexOf(R_PAREN, rParen + 1);
            lParen = line.indexOf(L_PAREN, lParen + 1);
            if (rParen != -1 && lParen != -1) {
                lineAux = line.substring(lParen + 1, rParen);
            }
        }
        return rParen;
    }
}
