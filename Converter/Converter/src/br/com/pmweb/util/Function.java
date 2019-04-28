package br.com.pmweb.util;

import java.util.ArrayList;

/**
 *
 * @author Lucas Gianfrancesco
 * @author Pedro Morelatto
 */
public class Function extends Parameter {

    private ArrayList<Parameter> parameters;

    public Function() {
        parameters = new ArrayList();
    }

    public Function(String name) {
        super(name);
    }

    public ArrayList<Parameter> getParameters() {
        return parameters;
    }

    public void setParameters(ArrayList<Parameter> parameters) {
        this.parameters = parameters;
    }

    public void addParameter(Parameter p) {
        parameters.add(p);
    }

    @Override
    public String toString() {
        String line = "fnc:" + name + "(";
        for (int i = 0; i < parameters.size(); i++) {
            line += parameters.get(i).toString();
            if (i != parameters.size() - 1) {
                line += ", ";
            }
        }
        line += ")";
        return line;
    }

}
