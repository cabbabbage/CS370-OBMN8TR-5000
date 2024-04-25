import java.io.*;
import java.net.Socket;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.awt.*;
import javax.swing.*;

class server_com extends Thread {
    private Socket clientSocket;
    private DataOutputStream dos;
    private DataInputStream dis;
    private List<String[]> responses;
    private List<String[]> waiting_responses;
    private Log log;

    public server_com(Socket socket, Log log) {
        this.log = log;
        this.clientSocket = socket;
        this.responses = new ArrayList<>();
        this.waiting_responses = new ArrayList<>();
        try {
            dos = new DataOutputStream(clientSocket.getOutputStream());
            dis = new DataInputStream(clientSocket.getInputStream());
        } catch (IOException e) {
            System.err.println("Error handling client: " + e.getMessage());
            e.printStackTrace();
        }
    }


    /////transmit is the main way to send commands to the drone client. must match the scheema outlined
    public void transmit(String[] content) {
        String to_send = String.join("%", content);
        try {
            dos.writeUTF(to_send);
            dos.flush();
            if(content[2] == null){
                waiting_responses.add(content);
            }
            String[] logContent = new String[content.length + 1];
            System.arraycopy(content, 0, logContent, 0, content.length);
            logContent[content.length] = "Transmitted";
            log.write(logContent);
        } catch (IOException e) {
            e.printStackTrace();
            String[] logContent = new String[content.length + 2];
            System.arraycopy(content, 0, logContent, 0, content.length);
            logContent[content.length] = "Transmitted";
            logContent[content.length + 1] = e.toString();
            log.write(logContent);
        }
    }


    
//util for getting name of machine hosting this server
    public String getHostName() {
        try {
            InetAddress remoteAddress = clientSocket.getInetAddress();
            return remoteAddress.getHostName();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


//generates random id for requests
    public static String genId() {
        Random random = new Random();
        StringBuilder sb = new StringBuilder(15);
        for (int i = 0; i < 15; i++) {
            sb.append(random.nextInt(10));
        }
        return sb.toString();
    }







    /////////////////////////////////////////////////////////////////////////////////
    /////The Following is for handeling recived mesages/responses from the client ///
    ////////////////////////////////////////////////////////////////////////////////

////this is the async function the listens constantly for data from the server.
    public void listenForResponses() {
        Thread listenerThread = new Thread(() -> {
            try {
                while (true) {
                    String r = dis.readUTF();
                    String[] parts = r.split("%");
                    responses.add(parts);
                    for (String[] response : responses) {
                        String type = response[0];
                        if (type.equals("HB")) {
                            respondToHeartbeat(response);
                        }
                        if (type.equals("R")) {
                            validateResponse(response);
                        }
                        if (type.equals("FD")) {
                            handleFlightData(response);
                        }
                    }
                    String[] logContent = new String[parts.length + 1];
                    System.arraycopy(parts, 0, logContent, 0, parts.length);
                    logContent[parts.length] = "Received";
                    log.write(logContent);
                }
            } catch (IOException e) {
                e.printStackTrace();
                log.write(e);                
            }
        });
        listenerThread.start();
    }

//implement will talk about this
    public void handleFlightData(String[] r){

    }




//finds and returns the command message in waiting _response list
    public String[] findRequest(String id) {
        for (String[] message : waiting_responses) {
            if (id.equals(message[1])) {
                return message;
            }
        }
        return null;
    }

/////validates all responses removes from active request lists if validators are equivalent
    public void validateResponse(String[] response) {
        String[] sent = findRequest(response[1]);
        if (sent != null && !sent[2].equals(response[2])) {
            transmit(sent);
        }
        responses.remove(response);
        waiting_responses.remove(sent);
    }


///sends heartbeat response to client
    public void respondToHeartbeat(String[] response) {
        String[] content = {"R", response[1], null};
        transmit(content);
    }



    /////////////////////////////////////////////////////////////////////////////////
    /////The Following section is for sending commands or requests to the client ///
    ////////////////////////////////////////////////////////////////////////////////

/////the following 4 functions are for uploading files to the client and validating the upload
    public void fileUpload(String path) {
        Thread uploadThread = new Thread(() -> {
            String id = genId();
            String type = "FU";
            String validator = getFileSize(path);
            String urgent = "0";
            String[] contents = {type, id, validator, path, urgent};
            transmit(contents);
            sendFile(path);
        });
        uploadThread.start();
    }

    public void sendFile(String path) {
        try {
            File file = new File(path);
            FileInputStream fis = new FileInputStream(file);
            BufferedInputStream bis = new BufferedInputStream(fis);
            byte[] buffer = new byte[1024];
            int bytesRead;
            dos.writeUTF(file.getName());
            dos.writeLong(file.length());
            while ((bytesRead = bis.read(buffer)) != -1) {
                dos.write(buffer, 0, bytesRead);
            }
            dos.flush();
            
            bis.close();
            fis.close();
            System.out.println("File sent successfully.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //getFileSize returns val that is used a validator for "fileUpload" function
    public static String getFileSize(String path) {
        File file = new File(path);
        long fileSize = file.length();
        return String.valueOf(fileSize);
    }

    //This is used exclusivly for sending files to the client
    public void transmit(String content) {
        try {
            dos.writeUTF(content);
            dos.flush();
            String[] logContent = {content, "Transmitted"};
            log.write(logContent);
        } catch (IOException e) {
            e.printStackTrace();
            String[] logContent = {content, "Transmitted", e.toString()};
            log.write(logContent);
        }
    }

    public void heartBeat(){
        String id = genId();
        String type = "HB";
        String validator = "fuck yeah";
        String[] content = {type, id, validator};
        transmit(content);
    }


    //Extra functions
    public void land(){
        String id = genId();
        String type = "L";
        String validator = "coming home";
        String[] content = {type, id, validator};
        transmit(content);
    }

    public void setAlt(){
        String id = genId();
        String type = "SA";
        String validator = "is good";
        String[] content = {type, id, validator};
        transmit(content);
    }

    public void hold(){
        String id = genId();
        String type = "H";
        String validator = "hold up wait a minute";
        String[] content = {type, id, validator};
        transmit(content);
    }

    public void takeOff(){
        String id = genId();
        String type = "TO";
        String validator = "blasting";
        String[] content = {type, id, validator};
        transmit(content);
    }

    public void missionUpdate(){
        String id = genId();
        String type = "MU";
        String validator = "Sir, yes sir";
        String[] content = {type, id, validator};
        transmit(content);
    }

    public void arm(){
        String id = genId();
        String type = "AR";
        String validator = "heck yeah";
        String[] content = {type, id, validator};
        transmit(content);
    }

    public void Kill(){
        String id = genId();
        String type = "NO";
        String validator = "please don't do this man";
        String[] content = {type, id, validator};
        transmit(content);
    }

    //The GUI
    public void GUI(){
        JFrame frame = new JFrame("My First GUI");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300,300);

        FlowLayout layout = new FlowLayout();
        frame.setLayout(layout);

        JButton start = new JButton("Start");
        JButton land = new JButton("Land");
        JButton setAlt = new JButton("Set Alt");
        JButton hold = new JButton("Hold");
        JButton takeOff = new JButton("Take Off");
        JButton missionUpdate = new JButton("Mission Update");
        JButton arm = new JButton("Arm");
        JButton kill = new JButton("Kill");
        
        frame.getContentPane().add(start);
        frame.getContentPane().add(land);
        frame.getContentPane().add(setAlt);
        frame.getContentPane().add(hold);
        frame.getContentPane().add(takeOff);
        frame.getContentPane().add(missionUpdate);
        frame.getContentPane().add(arm);
        frame.getContentPane().add(kill);
        frame.setVisible(true);
    }
}
