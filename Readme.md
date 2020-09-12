Directory structure    
    
    - emitter - a random generator of metrics simulating IoT reading
        - mqtt variant
        - rest api variant
    
    - collector - receives signals from emitters and pushes onto a queue
    
    - data mapper - transforms and enriches data collected by collector and returns record to the queuw
    
    - data persist - record data to the desired DB
         - Redis
         - InfluxDB
    
    - tests - unit tests
    
PreRequsites 

    Docker & docekr-compose is required


Notes:
    
    Kafka Docker setup from: https://github.com/wurstmeister/kafka-docker
    

Assumptions
 - you can run as many emmitters as required - they need to know the endpoint of the collector
 - collector should be placed behind load balancer so that it can be scaled and highly available
 