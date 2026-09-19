---
title: Computer Applications (Group III)
sidebar_position: 10
---
# Class 9 Computer Applications (Java / BlueJ - 100 Marks)

## Syllabus & Programming Concepts
1. Introduction to OOP (Encapsulation, Inheritance, Polymorphism, Abstraction)\n2. Elementary Java: Data types, Variables, Literals, Operators (Arithmetic, Relational, Logical)\n3. Mathematical Library Functions (Math.sqrt, Math.pow, Math.max, Math.abs)\n4. Conditional Statements: if-else, switch-case\n5. Iterative Constructs: for, while, do-while loops, nested loops\n6. Basic Class and Object Creation with BlueJ

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
