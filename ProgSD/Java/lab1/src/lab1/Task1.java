package lab1;
import java.util.Scanner;

public class Task1 {
	public static void printPrimes(int max){
		boolean[] isPrime = new boolean[max];
				
		for (int i=2;i<max;i++) {
			isPrime[i] = true;
		}
		
		for (int i=2;i*i<max;i++) {
			if (isPrime[i]) {
				for (int j=i*i;j<max;j+=i) {
					isPrime[j]=false;
				}
			}
		}
		
		for (int i=2;i<max;i++) {
			if (isPrime[i]) {
				System.out.println(i);
			}
		}
	}
	public static void main(String[] args) {
		Scanner myObj = new Scanner(System.in); 
		System.out.println("Enter the max number");
        int max = myObj.nextInt() ;
        System.out.println("Here are the prime numbers");
        printPrimes(max);
    }

}