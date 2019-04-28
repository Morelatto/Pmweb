package linkextractor;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.ArrayList;
import javax.swing.*;

/**
 *
 * @author Pedro Morelatto
 */
public class GUI {

    public static void main(String[] args) {
        final JFrame frame = new JFrame("Link Extractor");
        final JFileChooser fc = new JFileChooser();

        fc.setMultiSelectionEnabled(true);

        JButton btn = new JButton("Escolher Arquivo");
        btn.addActionListener((ActionEvent e) -> {
            int retVal = fc.showOpenDialog(frame);
            if (retVal == JFileChooser.APPROVE_OPTION) {
                File[] selectedfiles = fc.getSelectedFiles();
                StringBuilder sb = new StringBuilder();
                for (File selectedfile : selectedfiles) {
                    ArrayList<String> links = LinkExtractor.getLinks(LinkExtractor.fileToString(selectedfile.getAbsolutePath()));
                    for (String link : links) {
                        sb.append(link).append("\n");
                    }
                }
                JTextArea jta = new JTextArea(sb.toString());
                jta.setEditable(false);
                JScrollPane jsp = new JScrollPane(jta) {
                    @Override
                    public Dimension getPreferredSize() {
                        return new Dimension(480, 320);
                    }
                };
                JOptionPane.showMessageDialog(null, jsp, "Links", JOptionPane.INFORMATION_MESSAGE);
            }
        });

        Container pane = frame.getContentPane();
        pane.add(btn);

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(200, 200);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}
