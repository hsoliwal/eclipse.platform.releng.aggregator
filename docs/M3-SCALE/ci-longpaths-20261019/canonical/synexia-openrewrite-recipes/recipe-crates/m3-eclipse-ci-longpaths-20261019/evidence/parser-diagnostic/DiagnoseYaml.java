// SPDX-FileCopyrightText: 2026 Hitesh Soliwal and Contributors to the Synexia Project
// SPDX-License-Identifier: Apache-2.0
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.openrewrite.InMemoryExecutionContext;
import org.openrewrite.Parser;
import org.openrewrite.tree.ParseError;
import org.openrewrite.yaml.YamlParser;

class DiagnoseYaml {
    public static void main(String[] args) throws Exception {
        for (String arg : args) {
            String input = Files.readString(Path.of(arg));
            System.out.println("SOURCE=" + arg);
            var context = new InMemoryExecutionContext(Throwable::printStackTrace);
            var sources = YamlParser.builder().build().parseInputs(
                    List.of(Parser.Input.fromString(Path.of(".github/workflows/mavenBuild.yml"), input)),
                    null, context).toList();
            for (var source : sources) {
                System.out.println("RESULT=" + source.getClass().getName());
                if (source instanceof ParseError error) {
                    System.out.println("ERROR=" + error.toException().getMessage().split(" on:")[0]);
                    if (error.getErroneous() != null) {
                        System.out.println("PARSED=" + error.getErroneous().getClass().getName());
                        String printed = error.getErroneous().printAll();
                        int at = 0;
                        while (at < Math.min(input.length(), printed.length()) && input.charAt(at) == printed.charAt(at)) at++;
                        System.out.println("FIRST_DIFFERENCE=" + at + "; INPUT_BYTES=" + input.length() + "; PRINTED_BYTES=" + printed.length());
                        System.out.println("INPUT_WINDOW=" + input.substring(Math.max(0, at - 40), Math.min(input.length(), at + 80)).replace("\n", "\\n"));
                        System.out.println("PRINT_WINDOW=" + printed.substring(Math.max(0, at - 40), Math.min(printed.length(), at + 80)).replace("\n", "\\n"));
                        Files.writeString(Path.of(arg + ".diagnostic-printed"), printed);
                    }
                }
                else System.out.println("ROUNDTRIP=" + input.equals(source.printAll()));
            }
        }
    }
}
