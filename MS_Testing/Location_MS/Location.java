package com.is213.project;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import org.json.JSONArray;
import org.json.JSONObject;

public class Locationdist {
  public static void main(String[] args) {
    try {
      // Get the user's IP address
      URL ipApiUrl = new URL("https://api.ipify.org");
      HttpURLConnection ipApiCon = (HttpURLConnection) ipApiUrl.openConnection();
      BufferedReader ipApiIn = new BufferedReader(new InputStreamReader(ipApiCon.getInputStream()));
      String ipAddress = ipApiIn.readLine();
      ipApiIn.close();

      String ipInfoUrl = "https://ipinfo.io/" + ipAddress + "/json?token=63daa13dc0940f";

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

      // Use a geocoding API to get the user's location
      String geocodingUrl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latLng + "&key=AIzaSyCItPqAhCSJVc13yxvnZoHb7SyTajxJWJ8";

      URL geocodingObj = new URL(geocodingUrl);
      HttpURLConnection geocodingCon = (HttpURLConnection) geocodingObj.openConnection();

      BufferedReader geocodingIn = new BufferedReader(new InputStreamReader(geocodingCon.getInputStream()));
      String geocodingInputLine;
      StringBuffer geocodingResponse = new StringBuffer();

      while ((geocodingInputLine = geocodingIn.readLine()) != null) {
        geocodingResponse.append(geocodingInputLine);
      }
      geocodingIn.close();


      JSONObject geocodingJsonObj = new JSONObject(geocodingResponse.toString());
      if (geocodingJsonObj.has("results")) {
        JSONArray results = geocodingJsonObj.getJSONArray("results");
        JSONObject location = results.getJSONObject(0).getJSONObject("geometry").getJSONObject("location");

      
        double lat1 = location.getDouble("lat");
        double lng1 = location.getDouble("lng");

        // Get Destination address and convert to LatLng for calculation. Change this for dynamic checking of location distance
        String address = "2 Handy Rd, #01-21 The Assembly Ground, The Cathay (Dhoby Ghaut), The Cathay, Singapore 229233";

       
        String urlString = "https://maps.googleapis.com/maps/api/geocode/json?address=" + URLEncoder.encode(address, "UTF-8") + "&key=AIzaSyCItPqAhCSJVc13yxvnZoHb7SyTajxJWJ8";

   
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "application/json");
        BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));

     
        StringBuilder sb = new StringBuilder();
        String output;
        while ((output = br.readLine()) != null) {
            sb.append(output);
        }
        conn.disconnect();
        JSONObject response = new JSONObject(sb.toString());
        JSONArray results2 = response.getJSONArray("results");
        JSONObject result2 = results2.getJSONObject(0);
        JSONObject location2 = result2.getJSONObject("geometry").getJSONObject("location");
        double destLat = location2.getDouble("lat"); 
        double destLng = location2.getDouble("lng");
     
        String distanceUrl = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + lat1 + "," + lng1 + "&destinations=" + destLat + "," + destLng + "&mode=driving" + "&key=AIzaSyCItPqAhCSJVc13yxvnZoHb7SyTajxJWJ8"; 

        URL distanceObj = new URL(distanceUrl);
        HttpURLConnection distanceCon = (HttpURLConnection) distanceObj.openConnection();

        BufferedReader distanceIn = new BufferedReader(new InputStreamReader(distanceCon.getInputStream()));
        String distanceInputLine;
        StringBuffer distanceResponse = new StringBuffer();

        while ((distanceInputLine = distanceIn.readLine()) != null) {
            distanceResponse.append(distanceInputLine);
            System.out.println(distanceResponse.toString()); //prints the whole response 
        }
        distanceIn.close();

      
        JSONObject distanceJsonObj = new JSONObject(distanceResponse.toString());
        JSONArray distanceRows = distanceJsonObj.getJSONArray("rows");
        JSONObject distanceElements = distanceRows.getJSONObject(0).optJSONArray("elements").optJSONObject(0);
        if(distanceElements != null && distanceElements.has("distance")) {
            JSONObject distanceJsonObject = distanceElements.getJSONObject("distance");
            JSONObject durationJsonObject = distanceElements.getJSONObject("duration");
            if (distanceJsonObject.has("text")) {
                String distanceText = distanceJsonObject.getString("text");
                String durationText = durationJsonObject.getString("text");
                System.out.println("Distance: " + distanceText );
                System.out.println("Duration: " + durationText + " by driving");
            } else {
                System.out.println("Error: Failed to get distance value from JSON response.");
            }
        } else {
            System.out.println("Error: Failed to get distance value from JSON response.");
        }
        
    } else {
        System.out.println("No results found.");
    }
    }   catch (Exception e) {
        e.printStackTrace();
    }
}
}
