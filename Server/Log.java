import java.io.*;
import java.text.*;
import java.util.*;

public class Log {
    private File logFile;
    private FileWriter fileWriter;
    private BufferedWriter bufferedWriter;

    public Log() {
        try {
            File directory = new File("logs");
            if (!directory.exists()) {
                directory.mkdir();
            }
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd_HHmmss");
            String currentTime = dateFormat.format(new Date());
            String fileName = "Server_Log_" + currentTime + ".csv";
            logFile = new File(directory, fileName);
            fileWriter = new FileWriter(logFile);
            bufferedWriter = new BufferedWriter(fileWriter);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void write(String[] rowData) {
        try {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String timestamp = dateFormat.format(new Date());
            StringBuilder rowBuilder = new StringBuilder(timestamp);
            for (String element : rowData) {
                rowBuilder.append(",").append(element);
            }
            bufferedWriter.write(rowBuilder.toString());
            bufferedWriter.newLine();
            bufferedWriter.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void close() {
        try {
            if (bufferedWriter != null) {
                bufferedWriter.close();
            }
            if (fileWriter != null) {
                fileWriter.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void rename(String newFileName) {
        try {
            File newFile = new File(logFile.getParent(), newFileName);
            if (logFile.renameTo(newFile)) {
                logFile = newFile;
            } else {
                System.out.println("Failed to rename the file.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void write(RuntimeException message) {
        try {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String timestamp = dateFormat.format(new Date());
            bufferedWriter.write(timestamp + "," + message);
            bufferedWriter.newLine();
            bufferedWriter.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void write(IOException message) {
        try {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String timestamp = dateFormat.format(new Date());
            bufferedWriter.write(timestamp + "," + message);
            bufferedWriter.newLine();
            bufferedWriter.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void write(String message) {
        try {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String timestamp = dateFormat.format(new Date());
            bufferedWriter.write(timestamp + "," + message);
            bufferedWriter.newLine();
            bufferedWriter.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
