package br.com.pmweb.util;

/**
 *
 * @author Lucas Gianfrancesco
 * @author Pedro Morelatto
 */
public class Parameter {

    protected String name;

    public Parameter() {
    }

    public Parameter(String value) {
        this.name = value;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "p:" + name;
    }

}
