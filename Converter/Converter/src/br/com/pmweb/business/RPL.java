package br.com.pmweb.business;

import br.com.pmweb.classes.Function;
import br.com.pmweb.classes.Parameter;
import java.util.ArrayList;

/**
 *
 * @author Lucas Gianfrancesco
 * @author Pedro Morelatto
 */
public class RPL {

    public static String convertToRPL(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "";

        for (Parameter parameter : parameters) {
            if (parameter.getClass() == Function.class) {
                convertToRPL((Function) parameter);
            }
        }

        switch (function.getName()) {
            case "lookup":
                functionRPL = lookup(function);
                break;
            case "gt":
                functionRPL = expressions(function);
                break;
            case "ge":
                functionRPL = expressions(function);
                break;
            case "lt":
                functionRPL = expressions(function);
                break;
            case "le":
                functionRPL = expressions(function);
                break;
            case "eq":
                functionRPL = expressions(function);
                break;
            case "ne":
                functionRPL = expressions(function);
                break;
            case "and":
                functionRPL = operations(function);
                break;
            case "or":
                functionRPL = operations(function);
                break;
            case "not":
                System.out.println("not() não implementado.");
                break;
            case "add":
                functionRPL = calculations(function);
                break;
            case "sub":
                functionRPL = calculations(function);
                break;
            case "mul":
                functionRPL = calculations(function);
                break;
            case "div":
                functionRPL = calculations(function);
                break;
            case "mod":
                System.out.println("mod() não implementado.");
                break;
            case "avg":
                functionRPL = calculations2(function);
                break;
            case "max":
                functionRPL = calculations2(function);
                break;
            case "min":
                functionRPL = calculations2(function);
                break;
            case "campaignid":
                functionRPL = campaign(function);
                break;
            case "campaignmarketingprogram":
                functionRPL = campaign(function);
                break;
            case "campaignmarketingstrategy":
                functionRPL = campaign(function);
                break;
            case "campaignname":
                functionRPL = campaign(function);
                break;
            case "uppercase":
                functionRPL = cases(function);
                break;
            case "lowercase":
                functionRPL = cases(function);
                break;
            case "leadingcapital":
                functionRPL = cases(function);
                break;
            case "capitalizewords":
                functionRPL = cases(function);
                break;
            case "replaceall":
                functionRPL = replaces(function);
                break;
            case "replacefirst":
                functionRPL = replaces(function);
                break;
            case "document":
                functionRPL = documents(function);
                break;
            case "endswith":
                functionRPL = strings(function);
                break;
            case "startswith":
                functionRPL = strings(function);
                break;
            case "indexof":
                functionRPL = strings(function);
                break;
            case "concat":
                functionRPL = strings(function);
                break;
            case "charat":
                functionRPL = strings(function);
                break;
            case "setvars":
                functionRPL = vars(function);
                break;
            case "setglobalvars":
                functionRPL = vars(function);
                break;
            default:
                System.out.println("Função não encontrada.");
        }

        return functionRPL;
    }

    private static String lookup(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "";
        if (parameters.size() > 1) {
            throw new Exception("Função lookup não pode ter mais que um parâmetro.");
        } else {
            functionRPL = "${" + parameters.get(0).getName() + "}";
        }
        return functionRPL;
    }

    private static String expressions(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "";

        if (parameters.size() != 2) {
            throw new Exception("Função " + function.getName() + "() não pode ter " + parameters.size() + " parâmetros.");
        } else {
            functionRPL = "<#if " + parameters.get(0).getName() + " " + function.getName() + " " + parameters.get(0).getName() + "><#else></#if>";
        }
        return functionRPL;
    }

    private static String operations(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "<#if ";
        String type;

        if (parameters.size() < 2) {
            throw new Exception("Função " + function.getName() + "() não pode ter " + parameters.size() + " parâmetros.");
        } else {
            switch (function.getName()) {
                case "and":
                    type = "&&";
                    break;
                case "or":
                    type = "||";
                    break;
                default:
                    throw new Exception("Expressão não encontrada.");
            }
            functionRPL = parameters.stream().map((parameter) -> parameter.getName().trim() + " " + type + " ").reduce(functionRPL, String::concat);
            functionRPL = functionRPL.substring(0, functionRPL.length() - 4) + "><#else></#if>";
        }
        return functionRPL;
    }

    private static String calculations(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "${";
        String type;

        if (parameters.size() < 2) {
            throw new Exception("Função " + function.getName() + "() não pode ter " + parameters.size() + " parâmetros.");
        } else {
            switch (function.getName()) {
                case "add":
                    type = "+";
                    break;
                case "sub":
                    type = "-";
                    break;
                case "mul":
                    type = "*";
                    break;
                case "div":
                    type = "/";
                    break;
                default:
                    throw new Exception("Expressão não encontrada.");
            }
            functionRPL = parameters.stream().map((parameter) -> parameter.getName().trim() + " " + type + " ").reduce(functionRPL, String::concat);
            functionRPL = functionRPL.substring(0, functionRPL.length() - 3) + "}";
        }
        return functionRPL;
    }

    private static String calculations2(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "${";

        if (parameters.size() < 2) {
            throw new Exception("Função " + function.getName() + "() não pode ter " + parameters.size() + " parâmetros.");
        } else {
            switch (function.getName()) {
                case "avg":
                    functionRPL += "avg(";
                    break;
                case "max":
                    functionRPL += "max(";
                    break;
                case "min":
                    functionRPL += "min(";
                    break;
                default:
                    throw new Exception("Expressão não encontrada.");
            }
            functionRPL = parameters.stream().map((parameter) -> parameter.getName().trim() + ", ").reduce(functionRPL, String::concat);
            functionRPL = functionRPL.substring(0, functionRPL.length() - 3) + "}";
        }
        return functionRPL;
    }

    private static String campaign(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "${";

        if (parameters.size() != 1 || !"".equals(parameters.get(0).getName().trim())) {
            throw new Exception("A função " + function.getName() + " não pode ter parâmetros.");
        } else {
            functionRPL += function.getName().replace("campaign", "campaign.");
        }

        functionRPL += "}";

        return functionRPL;
    }

    private static String cases(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "${";
        String type;

        if (parameters.size() != 1) {
            throw new Exception("A função " + function.getName() + " não pode ter mais que um parâmetro.");
        } else {
            switch (function.getName()) {
                case "uppercase":
                    type = "upper_case";
                    break;
                case "lowercase":
                    type = "lower_case";
                    break;
                case "leadingcapital":
                    type = "cap_first";
                    break;
                case "capitalizewords":
                    type = "capitalize";
                    break;
                default:
                    throw new Exception("Função não encontrada.");
            }
            functionRPL += parameters.get(0).getName() + "?" + type;
        }
        functionRPL += "}";

        return functionRPL;
    }

    private static String replaces(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "${";

        if (parameters.size() != 3) {
            throw new Exception("A função " + function.getName() + " precisa ter três parâmetros.");
        } else {
            functionRPL += parameters.get(0).getName().trim() + "?replace(" + parameters.get(1).getName().trim() + ", " + parameters.get(2).getName().trim();
            switch (function.getName()) {
                case "replaceall":
                    functionRPL += ")}";
                    break;
                case "replacefirst":
                    functionRPL += ", f)}";
                    break;
                default:
                    throw new Exception("Função não encontrada.");
            }
        }
        return functionRPL;
    }

    private static String documents(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "<#include ";

        if (parameters.size() < 1) {
            throw new Exception("A função " + function.getName() + " precisa ter mais que dois parâmetros.");
        } else {
            if (parameters.get(0).getName().startsWith("http")) {
                functionRPL += "\"" + parameters.get(0).getName() + "\"";
            } else {
                functionRPL += "\"cms://" + parameters.get(0).getName() + "/" + parameters.get(1).getName().trim() + "\"";
            }
        }
        functionRPL += ">";
        return functionRPL;
    }

    private static String strings(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "${";

        switch (function.getName()) {
            case "endswith":
                functionRPL += parameters.get(0).getName() + "?ends_with(" + parameters.get(1).getName().trim() + ")";
                break;
            case "startswith":
                functionRPL += parameters.get(0).getName() + "?starts_with(" + parameters.get(1).getName().trim() + ")";
                break;
            case "indexof":
                functionRPL += parameters.get(0).getName() + "?index_of(" + parameters.get(1).getName().trim();
                if (parameters.get(2) != null) {
                    functionRPL += ", " + parameters.get(2).getName();
                }
                functionRPL += ")";
                break;
            case "concat":
                functionRPL = parameters.stream().map((parameter) -> " + " + parameter.getName()).reduce(functionRPL, String::concat);
                functionRPL = functionRPL.replaceFirst("\\s\\+\\s", "");
                break;
            case "charat":
                functionRPL += parameters.get(0).getName() + "[" + parameters.get(1).getName().trim() + "]";
                break;
            default:
                throw new Exception("Função não encontrada.");
        }
        functionRPL += "}";
        return functionRPL;
    }

    private static String vars(Function function) throws Exception {
        ArrayList<Parameter> parameters = function.getParameters();
        String functionRPL = "<#";
        String type = "";

        switch (function.getName()) {
            case "setvars":
                functionRPL += "assign ";
                type = functionRPL;
                break;
            case "setglobalvars":
                functionRPL += "global ";
                type = functionRPL;
                break;
            default:
                throw new Exception("Função não encontrada.");
        }
        if (parameters.size() == 1) {
            functionRPL += parameters.get(0).getName() + ">";
        } else {
            try {
                for (int i = 0; i < parameters.size(); i += 2) {
                    functionRPL += parameters.get(i).getName().trim() + " = " + parameters.get(i + 1).getName().trim() + ">\n" + type;
                }
            } catch (IndexOutOfBoundsException e) {
                throw new Exception("Função " + function.getName() + " não pode ter " + parameters.size() + " parâmetros.");
            }
        }
        functionRPL = functionRPL.substring(0, functionRPL.lastIndexOf(type));

        return functionRPL;
    }

}
