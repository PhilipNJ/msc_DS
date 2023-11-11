package lab1;

public class task2 {
	public static long computeFibonacci (int n) {
		 
		if (n<=1) {
			return n;
		}
		
		long fib1 = 0;
		long fib2 = 1;
		long fibonacci = 0;
		
		for (int i = 2;i<n+1;i++) {
			fibonacci = fib1+fib2;
			fib1 = fib2;
			fib2 = fibonacci;
					
		}
		return fibonacci;
	}
	public static void main(String[] args) {
		int n = 100;
		long result = computeFibonacci(n);
		System.out.println("The " + n + "th Fibonacci number is: " + result);
				
	}

}
