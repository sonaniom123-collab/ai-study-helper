import re
PROGRAMS = {
    "factorial": {
        "python": '''n = int(input("Enter a number: "))
fact = 1
for i in range(1, n + 1):
    fact *= i
print("Factorial:", fact)''',
        "c": '''#include <stdio.h>
int main() {
    int n;
    long long fact = 1;
    printf("Enter a number: ");
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        fact *= i;
    }
    printf("Factorial: %lld\\n", fact);
    return 0;
}''',
        "c++": '''#include <iostream>
using namespace std;
int main() {
    int n;
    long long fact = 1;
    cout << "Enter a number: ";
    cin >> n;
    for (int i = 1; i <= n; i++) {
        fact *= i;
    }
    cout << "Factorial: " << fact << endl;
    return 0;
}''',
        "java": '''import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int n = sc.nextInt();
        long fact = 1;
        for (int i = 1; i <= n; i++) {
            fact *= i;
        }
        System.out.println("Factorial: " + fact);
    }
}''',
    },
    "prime": {
        "python": '''n = int(input("Enter a number: "))
is_prime = n > 1
for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        is_prime = False
        break
print("Prime" if is_prime else "Not prime")''',
        "c": '''#include <stdio.h>
int main() {
    int n, isPrime = 1;
    printf("Enter a number: ");
    scanf("%d", &n);
    if (n <= 1) isPrime = 0;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            isPrime = 0;
            break;
        }
    }
    printf(isPrime ? "Prime\\n" : "Not prime\\n");
    return 0;
}''',
        "c++": '''#include <iostream>
using namespace std;
int main() {
    int n;
    bool isPrime = true;
    cout << "Enter a number: ";
    cin >> n;
    if (n <= 1) isPrime = false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            isPrime = false;
            break;
        }
    }
    cout << (isPrime ? "Prime" : "Not prime") << endl;
    return 0;
}''',
        "java": '''import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int n = sc.nextInt();
        boolean isPrime = n > 1;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                isPrime = false;
                break;
            }
        }
        System.out.println(isPrime ? "Prime" : "Not prime");
    }
}''',
    },
    "even_odd": {
        "python": '''n = int(input("Enter a number: "))
if n % 2 == 0:
    print("Even")
else:
    print("Odd")''',
        "c": '''#include <stdio.h>
int main() {
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    if (n % 2 == 0) {
        printf("Even\\n");
    } else {
        printf("Odd\\n");
    }
    return 0;
}''',
        "c++": '''#include <iostream>
using namespace std;
int main() {
    int n;
    cout << "Enter a number: ";
    cin >> n;
    if (n % 2 == 0) {
        cout << "Even" << endl;
    } else {
        cout << "Odd" << endl;
    }
    return 0;
}''',
        "java": '''import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int n = sc.nextInt();
        if (n % 2 == 0) {
            System.out.println("Even");
        } else {
            System.out.println("Odd");
        }
    }
}''',
    },
    "fibonacci": {
        "python": '''n = int(input("How many terms? "))
a, b = 0, 1
for _ in range(n):
    print(a, end=" ")
    a, b = b, a + b
print()''',
        "c": '''#include <stdio.h>
int main() {
    int n;
    long long a = 0, b = 1, next;
    printf("How many terms? ");
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("%lld ", a);
        next = a + b;
        a = b;
        b = next;
    }
    printf("\\n");
    return 0;
}''',
        "c++": '''#include <iostream>
using namespace std;
int main() {
    int n;
    long long a = 0, b = 1, next;
    cout << "How many terms? ";
    cin >> n;
    for (int i = 0; i < n; i++) {
        cout << a << " ";
        next = a + b;
        a = b;
        b = next;
    }
    cout << endl;
    return 0;
}''',
        "java": '''import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("How many terms? ");
        int n = sc.nextInt();
        long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            System.out.print(a + " ");
            long next = a + b;
            a = b;
            b = next;
        }
        System.out.println();
    }
}''',
    },
    "pattern": {
        "python": '''n = int(input("Enter number of rows: "))
for i in range(1, n + 1):
    print("*" * i)''',
        "c": '''#include <stdio.h>
int main() {
    int n;
    printf("Enter number of rows: ");
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            printf("*");
        }
        printf("\\n");
    }
    return 0;
}''',
        "c++": '''#include <iostream>
using namespace std;
int main() {
    int n;
    cout << "Enter number of rows: ";
    cin >> n;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cout << "*";
        }
        cout << endl;
    }
    return 0;
}''',
        "java": '''import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter number of rows: ");
        int n = sc.nextInt();
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}''',
    },
}
ENGLISH_WORDS = {
    "factorial": {"factorial"},
    "fibonacci": {"fibonacci", "fibonaci"},
    "prime": {"prime", "primes"},
    "even_odd": {"even", "odd"},
    "pattern": {"pattern", "patterns", "pyramid", "star", "stars", "triangle"},
}
OTHER_SCRIPT = {
    "factorial": ["ફેક્ટોરિયલ", "ફેક્ટોરીયલ", "फैक्टोरियल", "फैक्टोरियल", "अपवर्त्य"],
    "fibonacci": ["ફિબોનાકી", "फिबोनाची", "फिबोनैचि", "फिबोनाक्सी"],
    "prime": ["અવિભાજ્ય", "પ્રાઇમ", "अभाज्य", "प्राइम"],
    "even_odd": ["બેકી", "એકી", "विषम", "सम संख्या", "सम या"],
    "pattern": ["પેટર્ન", "પિરામિડ", "पैटर्न", "पिरामिड"],
}
ORDER = ["factorial", "fibonacci", "prime", "even_odd", "pattern"]
MATH_ONLY = {"area", "perimeter", "circumference"}
def find_program(text):
    t = text.lower()
    words = set(re.findall(r"[a-z]+", t))
    if words & MATH_ONLY:
        return None
    for name in ORDER:
        if words & ENGLISH_WORDS[name]:
            return name
        if any(k in t for k in OTHER_SCRIPT[name]):
            return name
    return None
def get_program(name, language):
    return PROGRAMS.get(name, {}).get(language, "Not available yet")