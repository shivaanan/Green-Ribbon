package com.is213.project;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import org.json.JSONArray;
import org.json.JSONObject;

public class GetLocation {
  public static void main(String[] args) {
    try {
        // Get the user's IP address
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

        // Parse the JSON response to get the latitude and longitude values
        JSONObject ipInfoJsonObj = new JSONObject(ipInfoResponse.toString());
        String latLng = ipInfoJsonObj.getString("loc");

        
        // Use a geocoding API to get the user's location
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

        // Parse the JSON response
        JSONObject jsonObj = new JSONObject(response.toString());
        System.out.println(jsonObj);
        if (jsonObj.has("results")) {
            JSONArray results = jsonObj.getJSONArray("results");
            JSONObject location = results.getJSONObject(0).getJSONObject("geometry").getJSONObject("location");

            // Get the latitude and longitude values
            double lat = location.getDouble("lat");
            double lng = location.getDouble("lng");

            // Print the latitude and longitude values
            System.out.println("Latitude: " + lat);
            System.out.println("Longitude: " + lng);
        } else {
            System.out.println("No results found.");
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
  }
}

