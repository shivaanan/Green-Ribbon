package com.esd.project.location;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;


@SpringBootApplication
public class Location {

    public static void main(String[] args) {
        SpringApplication.run(Location.class, args);
    }

}

@RestController
class LocationController {

    @RequestMapping("/location")
    public String getLocation() {
        try {
            URL ipApiUrl = new URL("https://api.ipify.org");
            HttpURLConnection ipApiCon = (HttpURLConnection) ipApiUrl.openConnection();
            BufferedReader ipApiIn = new BufferedReader(new InputStreamReader(ipApiCon.getInputStream()));
            String ipAddress = ipApiIn.readLine();
            ipApiIn.close();

            String ipInfoUrl = "https://ipinfo.io/" + ipAddress + "/json?token=63daa13dc0940f"; // Replace YOUR_TOKEN_HERE with your actual API token

            URL ipInfoObj = new URL(ipInfoUrl);
            HttpURLConnection ipInfoCon = (HttpURLConnection) ipInfoObj.openConnection();

            BufferedReader ipInfoIn = new BufferedReader(new InputStreamReader(ipInfoCon.getInputStream()));
            String ipInfoInputLine;
            StringBuffer ipInfoResponse = new StringBuffer();

            while ((ipInfoInputLine = ipInfoIn.readLine()) != null) {
                ipInfoResponse.append(ipInfoInputLine);
            }
            ipInfoIn.close();

        
            JSONObject ipInfoJsonObj = new JSONObject(ipInfoResponse.toString());
            String latLng = ipInfoJsonObj.getString("loc");

            String url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latLng + "&key=AIzaSyCItPqAhCSJVc13yxvnZoHb7SyTajxJWJ8"; // Replace YOUR_API_KEY_HERE with your actual API key

            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

        
            JSONObject jsonObj = new JSONObject(response.toString());
            if (jsonObj.has("results")) {
                JSONArray results = jsonObj.getJSONArray("results");
                JSONObject location = results.getJSONObject(0).getJSONObject("geometry").getJSONObject("location");

                double lat = location.getDouble("lat");
                double lng = location.getDouble("lng");
                
                JSONObject latLngObj = new JSONObject();
                latLngObj.put("lat", lat);
                latLngObj.put("lng", lng);
            
                return latLngObj.toString();
            } else {
                return new JSONObject().put("error", "No results found.").toString();
            }
        } catch (Exception e) {
            e.printStackTrace();
            JSONObject errorObj = new JSONObject();
            errorObj.put("error", "Error occurred: " + e.getMessage());
            return errorObj.toString();
        }
    }

   
}
