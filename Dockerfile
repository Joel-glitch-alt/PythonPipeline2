FROM python:3.10

# Install dependencies
RUN apt-get update && apt-get install -y unzip curl

# Install SonarScanner CLI
RUN curl -o /tmp/sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip && \
    unzip /tmp/sonar-scanner.zip -d /opt && \
    rm /tmp/sonar-scanner.zip

ENV PATH="/opt/sonar-scanner-4.8.0.2856-linux/bin:${PATH}"
