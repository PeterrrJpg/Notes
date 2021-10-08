import java.io.*;
import java.net.*;
import java.util.*;
import java.lang.*;

/*
 * Used PingServer.java as template code
 */

public class PingClient
{
   private static final double NUM_PING_REQUESTS = 15.0;
   private static final int MAX_WAITING_TIME = 600;  // milliseconds

   public static void main(String[] args) throws Exception
   {
      // Get command line argument.
      if (args.length != 2) {
         System.out.println("Required arguments: host port");
         return;
      }
      InetAddress host = InetAddress.getByName(args[0]);
      int port = Integer.parseInt(args[1]);

      int seqNum = 3331;
      int reqNum = 0;

      long minRTT = 0;
      long maxRTT = 0;
      double avgRTT = 0;
      int totalRTT = 0;
      int numSuccess = 0;

      // Create a datagram socket for receiving and sending UDP packets
      // through the port specified on the command line.
      DatagramSocket socket = new DatagramSocket();
      socket.connect(host, port);

      // Processing loop.
      while (reqNum < NUM_PING_REQUESTS) {
         // time when the client sent the message
         long timeSent = System.currentTimeMillis();

         // create message to send
         String msg = "Ping: " + "seq = " + seqNum + ", time = " + timeSent + " \r\n";
         byte[] byteArr = new byte[1024];
         byteArr = msg.getBytes();

         // Create a datagram packet to hold incomming UDP packet.
         DatagramPacket request = new DatagramPacket(byteArr, byteArr.length, host, port);

         // send request
			socket.send(request);

			try {
				socket.setSoTimeout(MAX_WAITING_TIME);

				DatagramPacket response = new DatagramPacket(new byte[1024], 1024);
				socket.receive(response);

				long timeReceived = System.currentTimeMillis();
	
				printData(response, timeReceived - timeSent);

            // max RTT
            if (timeReceived - timeSent > maxRTT) {
               maxRTT = timeReceived - timeSent;
            }

            // min RTT
            if (minRTT == 0) {
               minRTT = timeReceived - timeSent;
            } else if (timeReceived - timeSent < minRTT) {
               minRTT = timeReceived - timeSent;
            }

            // avg RTT
            totalRTT += (timeReceived - timeSent);

            seqNum++;
            numSuccess++;
			} catch (IOException e) {
				System.out.println("time out");
			}

         reqNum++;
      }
      System.out.println(numSuccess + " successful packets, " + String.format("%.2f", ((NUM_PING_REQUESTS - numSuccess) / NUM_PING_REQUESTS * 100)) + "% packet loss");
      System.out.println("Min RTT: " + minRTT);
      System.out.println("Max RTT: " + maxRTT);
      System.out.println("Avg RTT: " + String.format("%.2f", ((double)totalRTT / numSuccess)));
   }

   /* 
    * Print ping data to the standard output stream.
    */
   private static void printData(DatagramPacket request, long timeDelay) throws Exception
   {
      // Obtain references to the packet's array of bytes.
      byte[] buf = request.getData();

      // Wrap the bytes in a byte array input stream,
      // so that you can read the data as a stream of bytes.
      ByteArrayInputStream bais = new ByteArrayInputStream(buf);

      // Wrap the byte array output stream in an input stream reader,
      // so you can read the data as a stream of characters.
      InputStreamReader isr = new InputStreamReader(bais);

      // Wrap the input stream reader in a bufferred reader,
      // so you can read the character data a line at a time.
      // (A line is a sequence of chars terminated by any combination of \r and \n.) 
      BufferedReader br = new BufferedReader(isr);

      // The message data is contained in a single line, so read this line.
      String line = br.readLine();

      // Print host address and data received from it.
      System.out.println(
         new String(line) + "\b, rtt = " + timeDelay + " ms" );
   }
}