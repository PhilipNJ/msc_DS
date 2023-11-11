  public class Orders {

        public static void main(String argsp[]) {
            String alphabet = "abc";
            ArrayList<String> list = new ArrayList<String>();
            int n = alphabet.length();

            Random rand = new Random();
            for (int i = 0; i < 10000; i++){
               char a = alphabet.charAt(rand.nextInt(n));
               char b = alphabet.charAt(rand.nextInt(n));
               char c = alphabet.charAt(rand.nextInt(n));

               String s = Character.toString(a) + Character.toString(b) + Character.toString(c); 

               if(list.indexOf(s) == -1){
                   list.add(s);
               }
            }
            System.out.println(list);
        }
