package uci.mondego.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.visitor.TreeVisitor;
import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import uci.mondego.CustomMethodVisitorForIC;
import uci.mondego.CustomVisitor;

public class BasicHttpServer {
    HttpServer server;

    public BasicHttpServer(String address, int port) throws IOException {
        this.server = HttpServer.create(new InetSocketAddress(address, port),
                0);
        this.server.createContext("/metrics", new HeaderHandler());
        server.setExecutor(null); // creates a default executor
        server.start();
    }

    static class MetricsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange he) throws IOException {
            // parse request
            Map<String, Object> parameters = new HashMap<String, Object>();
            InputStreamReader isr = new InputStreamReader(he.getRequestBody(),
                    "utf-8");
            BufferedReader br = new BufferedReader(isr);
            String query = br.readLine();
            parseQuery(query, parameters);
            String code = (String) parameters.get("codestring");
            System.out.println(code);
            String response = "";
            try {
                CompilationUnit cu = JavaParser.parse(code);
                List<String> results = new ArrayList<String>();
                TreeVisitor visitor = new CustomMethodVisitorForIC(results);
                visitor.visitPreOrder(cu);

                for (String result : results) {
                    response += result + "\n";
                }
                he.sendResponseHeaders(200,
                        response.getBytes(StandardCharsets.UTF_8).length);
            } catch (Exception e) {
                response += "internal server error\n";
                he.sendResponseHeaders(500,
                        response.getBytes(StandardCharsets.UTF_8).length);
            } finally {
                OutputStream os = he.getResponseBody();
                os.write(response.toString().getBytes());
                os.close();
            }
        }
    }

    public static void parseQuery(String query, Map<String, Object> parameters)
            throws UnsupportedEncodingException {

        if (query != null) {
            String pairs[] = query.split("[&]");
            for (String pair : pairs) {
                String param[] = pair.split("[=]");
                String key = null;
                String value = null;
                if (param.length > 0) {
                    key = URLDecoder.decode(param[0],
                            System.getProperty("file.encoding"));
                }

                if (param.length > 1) {
                    value = URLDecoder.decode(param[1],
                            System.getProperty("file.encoding"));
                }

                if (parameters.containsKey(key)) {
                    Object obj = parameters.get(key);
                    if (obj instanceof List<?>) {
                        List<String> values = (List<String>) obj;
                        values.add(value);

                    } else if (obj instanceof String) {
                        List<String> values = new ArrayList<String>();
                        values.add((String) obj);
                        values.add(value);
                        parameters.put(key, values);
                    }
                } else {
                    parameters.put(key, value);
                }
            }
        }
    }

    static class HeaderHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange he) throws IOException {
            Headers headers = he.getRequestHeaders();
            Set<Map.Entry<String, List<String>>> entries = headers.entrySet();
            String response = "";
            for (Map.Entry<String, List<String>> entry : entries)
                response += entry.toString() + "\n";
            he.sendResponseHeaders(200, response.length());
            OutputStream os = he.getResponseBody();
            os.write(response.toString().getBytes());
            os.close();
        }
    }

    public void stop() {
        this.server.stop(0);
    }

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer
                .create(new InetSocketAddress("localhost", 8001), 0);
        server.createContext("/metrics", new MetricsHandler());
        server.createContext("/header", new HeaderHandler());
        server.setExecutor(null); // creates a default executor
        server.start();
    }

    public static String breakpointParseClass(String name) {
        int dot = name.lastIndexOf('.');
        int colon = name.indexOf(':');
        if (dot != -1) {
            return name.substring(0, dot);
        } else if (dot == -1 && colon != -1) {
            return name.substring(0, colon);
        } else {
            return "";
        }
    }

}