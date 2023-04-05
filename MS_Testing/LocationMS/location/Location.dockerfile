FROM openjdk:11
ARG JAR_FILE=/LocationMS/location/.mvn/rapper/*.jar
COPY ${JAR_FILE} app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]