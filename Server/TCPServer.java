import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class TCPServer {
    private static ServerSocket serverSocket;
    private static int portNumber = 6969;
    private static String IP = get_IP();
    private static String key = "cs370!";
    private static Log log;

    public TCPServer() {}

    public static void main(String[] args) {
        log = new Log();  
        log.write("helllo from server!"); 
        server_com coms;  
        try {
            portNumber = Integer.parseInt(args[0]);

            try {
                serverSocket = new ServerSocket(portNumber);
                System.out.println("IP address " + IP);
                System.out.println("Server listening on port " + portNumber);
                System.out.println("Waiting for clients");
                while (true) {
                    Socket clientSocket = serverSocket.accept();
                    try {
                        DataInputStream dis = new DataInputStream(clientSocket.getInputStream());
                        if (dis.readUTF().equals(key)) {
                            coms = new server_com(clientSocket, log);
                            System.out.println("Key accepted. Establishing connection");
                            coms.transmit("100");
                            log.write("100");
                            coms.fileUpload("../Testing/test.java");
                            coms.heartBeat();
                        } else {
                            clientSocket.close();
                            log.write("bad key");
                        }
                        
                    } catch (IOException e) {
                        System.err.println("Error handling client: " + e.getMessage());
                        log.write(e);
                    }
                }
            } catch (IOException e) {
                System.err.println("Could not listen on port: " + portNumber);
                System.exit(1);
            }
        } catch (ArrayIndexOutOfBoundsException | NumberFormatException e) {
            System.err.println("Invalid arguments. Please provide a valid port number.");
            log.write(e);
        }
    }

    private static String get_IP() {
        try {
            InetAddress localhost = InetAddress.getLocalHost();
            return localhost.getHostAddress();
        } catch (UnknownHostException e) {
            e.printStackTrace();
            log.write(e);
            return null;
        }
    }
}
