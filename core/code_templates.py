OPS = {
    "addition": "+",
    "subtraction": "-",
    "multiplication": "*",
    "division": "/",
}
PROGRAMS = {
    "python": "a = @T@(input())\nb = @T@(input())\nprint(a @OP@ b)",
    "c": '#include <stdio.h>\nint main() {\n    @T@ a, b;\n    scanf("@F@ @F@", &a, &b);\n    printf("@F@", a @OP@ b);\n    return 0;\n}',
    "c++": '#include <iostream>\nusing namespace std;\nint main() {\n    @T@ a, b;\n    cin >> a >> b;\n    cout << a @OP@ b;\n    return 0;\n}',
    "java": 'import java.util.Scanner;\npublic class Main {\n    public static void main(String[] args) {\n        Scanner s = new Scanner(System.in);\n        @T@ a = s.next@FN@(), b = s.next@FN@();\n        System.out.println(a @OP@ b);\n    }\n}',
}
def get_code(operation, language):
    if operation not in OPS or language not in PROGRAMS:
        return "Not available yet"
    is_division = operation == "division"
    code = PROGRAMS[language]
    code = code.replace("@OP@", OPS[operation])
    code = code.replace("@T@", "float" if is_division else "int")
    code = code.replace("@F@", "%f" if is_division else "%d")
    code = code.replace("@FN@", "Float" if is_division else "Int")
    return code