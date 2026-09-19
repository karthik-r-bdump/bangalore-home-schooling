---
title: Computer Applications (Group III)
sidebar_position: 10
---
# Class 10 Computer Applications (Java / BlueJ - 100 Marks)

## Syllabus & Programming Concepts
1. Class as the Basis of All Computation (Objects, State, Behavior)\n2. User-Defined Methods: Method overloading, call by value vs. call by reference\n3. Constructors: Default, parameterized, constructor overloading\n4. Library Classes: Wrapper classes (Character, Integer, Double), Autoboxing/Unboxing\n5. Encapsulation & Access Specifiers\n6. Arrays: 1-D & 2-D Arrays (Searching: Linear & Binary; Sorting: Bubble & Selection)\n7. String Handling: String methods (charAt, substring, indexOf, toUpperCase, equals)\n8. Exceptions & Error Handling

## 💻 Sample Java Program (CISCE Specification)
```java
// ICSE Class 10 Specimen: Bubble Sort on 1-D Array
import java.util.Scanner;

public class BubbleSort {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int[] arr = new int[10];
        System.out.println("Enter 10 integers:");
        for (int i = 0; i < 10; i++) {
            arr[i] = in.nextInt();
        }

        // Bubble sort in ascending order
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }

        System.out.println("Sorted Array:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}
```
